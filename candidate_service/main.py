from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from typing import Dict, List
import litellm
from arize.otel import register
from openinference.instrumentation.litellm import LiteLLMInstrumentor
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Candidate Service")

# Setup OTel via Arize convenience function
tracer_provider = register(
    space_id=os.getenv("ARIZE_SPACE_ID", "your-space-id"),
    api_key=os.getenv("ARIZE_API_KEY", "your-api-key"),
    project_name="find-candidate"
)

# Instrument LiteLLM
LiteLLMInstrumentor().instrument(tracer_provider=tracer_provider)

class SearchRequest(BaseModel):
    search_query: str

# Load profiles directly
def load_profiles() -> List[str]:
    profiles = []
    for file in ['db/p1.json', 'db/p2.json']:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                profiles.append(data['data']['person']['profile_summary'])
        except Exception as e:
            print(f"Error loading profile {file}: {str(e)}")
            profiles.append("")
    return profiles

# Load profiles at module level
PROFILES = load_profiles()

@app.post("/find-candidate")
async def find_best_candidate(request: SearchRequest) -> Dict:
    """
    Find the best candidate by comparing search criteria against profile summaries using AI
    """
    # Verify profiles are loaded
    if not all(PROFILES):
        raise HTTPException(
            status_code=500,
            detail="Profile data not properly loaded. Please check the profile JSON files."
        )

    try:
        # Prepare the comparison prompt
        prompt = f"""Given the following job search criteria and two candidate profiles, determine which candidate is the better match.
        
Search Criteria:
{request.search_query}

Candidate 1 Profile:
{PROFILES[0]}

Candidate 2 Profile:
{PROFILES[1]}

Please analyze both candidates against the search criteria and:
1. Determine which candidate is a better match
2. Provide a brief explanation of why they are the better match
3. List the key matching points

Format your response as:
SELECTED: [Candidate 1 or Candidate 2]
REASON: [Your explanation]
MATCHING POINTS: [Bullet points of matching criteria]"""

        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are an expert recruiter AI that analyzes candidate profiles against job requirements to find the best matches."
            },
            {
                "role": "user",
                "content": prompt
            }]
        )

        # Extract the AI's analysis
        analysis = response.choices[0].message.content

        return {
            "status": "success",
            "analysis": analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7624) 