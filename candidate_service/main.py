from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from typing import Dict
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

# Global variables to store profile summaries
p1_summary: str = ""
p2_summary: str = ""

def load_profile_summary(json_file: str) -> str:
    """
    Load and parse a profile summary from a JSON file.
    
    Args:
        json_file: Path to the JSON file containing profile data
        
    Returns:
        Profile summary string
        
    Raises:
        FileNotFoundError: If the JSON file doesn't exist
        json.JSONDecodeError: If the JSON file is invalid
        KeyError: If the required fields are missing in the JSON
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            return data['data']['person']['profile_summary']
    except FileNotFoundError:
        raise Exception(f"Profile file not found: {json_file}")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON in profile file: {json_file}")
    except KeyError as e:
        raise Exception(f"Missing required field in profile file {json_file}: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """
    Load profile data during application startup.
    This ensures profiles are loaded before handling any requests.
    """
    global p1_summary, p2_summary
    try:
        p1_summary = load_profile_summary('db/p1.json')
        p2_summary = load_profile_summary('db/p2.json')
    except Exception as e:
        # Log the error but don't prevent startup
        print(f"Error loading profiles during startup: {str(e)}")
        # Initialize with empty strings to prevent None errors
        p1_summary = ""
        p2_summary = ""

@app.post("/find-candidate")
async def find_best_candidate(request: SearchRequest) -> Dict:
    """
    Find the best candidate by comparing search criteria against profile summaries using AI
    """
    # Verify profiles are loaded
    if not p1_summary or not p2_summary:
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
{p1_summary}

Candidate 2 Profile:
{p2_summary}

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