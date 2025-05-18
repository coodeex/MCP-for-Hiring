from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from typing import Dict, List
import litellm
from arize.otel import register
from openinference.instrumentation.litellm import LiteLLMInstrumentor
from dotenv import load_dotenv
import glob

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
def load_profiles() -> List[Dict]:
    profiles = []
    # Get all JSON files from the db directory
    json_files = glob.glob('../client/db/*.json')
    
    for file in json_files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                profiles.append(data['data']['person'])  # Store all person data
        except Exception as e:
            print(f"Error loading profile {file}: {str(e)}")
            profiles.append({})
    return profiles

# Load profiles at module level
PROFILES = load_profiles()

@app.post("/find-candidate")
async def find_best_candidate(request: SearchRequest) -> Dict:
    """
    Find the best candidate by comparing search criteria against profile summaries using AI
    """
    # Verify profiles are loaded
    if len(PROFILES) < 2:  # Ensure we have at least 2 profiles for comparison
        raise HTTPException(
            status_code=500,
            detail="At least two profile files are required for comparison. Please check the profile JSON files."
        )
    if not all(PROFILES):
        raise HTTPException(
            status_code=500,
            detail="Profile data not properly loaded. Please check the profile JSON files."
        )

    try:
        # Prepare the comparison prompt with candidate IDs
        candidates_text = "\n\n".join([
            f"ID {profile.get('id', 'N/A')}:\n{profile.get('profile_summary', '')}" 
            for i, profile in enumerate(PROFILES[:2])
        ])
        
        prompt = f"""Given the following job search criteria and two candidate profiles, determine which candidate is the better match.
        
Search Criteria:
{request.search_query}

{candidates_text}

Please analyze both candidates against the search criteria and:
1. Determine which candidate is a better match (reference them by their ID)
2. Provide a brief explanation of why they are the better match
3. List the key matching points

Format your response as:
SELECTED: [ID number]
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