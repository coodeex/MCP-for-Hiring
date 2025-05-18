from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from typing import Dict, List
from groq import Groq
from arize.otel import register
from openinference.instrumentation.groq import GroqInstrumentor
from dotenv import load_dotenv
import glob
import re

load_dotenv()

app = FastAPI(title="Candidate Service")

# Setup OTel via Arize convenience function
tracer_provider = register(
    space_id=os.getenv("ARIZE_SPACE_ID", "your-space-id"),
    api_key=os.getenv("ARIZE_API_KEY", "your-api-key"),
    project_name="find-candidate"
)

# Instrument Groq
GroqInstrumentor().instrument(tracer_provider=tracer_provider)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
            profiles.append({})
    return profiles

# Load profiles at module level
PROFILES = load_profiles()

@app.post("/find-candidate")
async def find_best_candidate(request: SearchRequest) -> Dict:
    """
    Find the best candidate by comparing search criteria against profile summaries using AI
    """
    print(f"Received search request: {request.search_query}")
    
    # Verify profiles are loaded
    print(f"Checking profiles. Total profiles available: {len(PROFILES)}")
    if len(PROFILES) < 2:  # Ensure we have at least 2 profiles for comparison
        print("Error: Insufficient profiles loaded")
        raise HTTPException(
            status_code=500,
            detail="At least two profile files are required for comparison. Please check the profile JSON files."
        )
    if not all(PROFILES):
        print("Error: Some profiles are empty")
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
        prompt = f"""Compare these candidate profiles against the job search criteria and determine the best match:

Search Criteria:
{request.search_query}

{candidates_text}

Analyze the candidates and provide:
1. The best matching candidate ID
2. Brief explanation of why they are the best fit
3. Key matching qualifications
4. Any potential gaps to be aware of

Format your response as:
SELECTED: [ID number]
CANDIDATE LINK: http://localhost:3000/candidate/[ID number]
REASON: [Brief explanation]
MATCHING POINTS: [Key qualifications]
GAPS: [Areas for consideration]"""

        print("Making API call to Groq...")
        response = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "You are an expert recruiter AI that identifies the best matching candidate based on the given criteria."
            },
            {
                "role": "user",
                "content": prompt
            }],
            model="llama3-70b-8192"
        )

        # Extract the AI's analysis
        analysis = response.choices[0].message.content

        # Extract the selected candidate ID from the analysis
        selected_id_match = re.search(r'SELECTED:\s*(\d+)', analysis)
        selected_id = selected_id_match.group(1) if selected_id_match else PROFILES[0]['id']  # Default to first candidate if no match found

        return {
            "status": "success",
            "analysis": analysis,
            "candidate_link": f"http://localhost:3000/candidate/{selected_id}"
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting the FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=7624) 