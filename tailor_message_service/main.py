from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from arize.otel import register
from openinference.instrumentation.litellm import LiteLLMInstrumentor
import litellm
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Setup OTel via Arize convenience function
tracer_provider = register(
    space_id=os.getenv("ARIZE_SPACE_ID", "your-space-id"),
    api_key=os.getenv("ARIZE_API_KEY", "your-api-key"),
    project_name="mcp-for-hiring"
)

# Instrument LiteLLM
LiteLLMInstrumentor().instrument(tracer_provider=tracer_provider)

app = FastAPI(title="Tailor Message Service")

class TailorMessageRequest(BaseModel):
    company_name: str
    job_title: str
    salary: str
    candidate_name: str
    description: str

class TailorMessageResponse(BaseModel):
    status: str
    subject: str | None = None
    message: str | None = None
    error: str | None = None

@app.post("/tailor-message", response_model=TailorMessageResponse)
async def tailor_message(request: TailorMessageRequest) -> Dict:
    """
    Process a request to create a personalized outreach message using LiteLLM.
    """
    try:
        prompt = f"""Create a professional and engaging outreach message to a potential job candidate with the following details:
        
Company: {request.company_name}
Position: {request.job_title}
Salary: {request.salary}
Candidate: {request.candidate_name}
Job Description: {request.description}

The message should:
1. Be warm and professional
2. Highlight the opportunity
3. Mention the company name and role
4. Include the salary information tastefully
5. Reference the job description key points
6. End with a clear call to action

Please format this as a complete email with subject line and body."""

        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a professional recruiter crafting personalized outreach messages to potential candidates."
            },
            {
                "role": "user",
                "content": prompt
            }]
        )

        # Extract the generated message
        generated_text = response.choices[0].message.content

        # Split into subject and body (assuming the model formats it with a subject line)
        parts = generated_text.split("\n", 1)
        subject = parts[0].replace("Subject:", "").strip()
        body = parts[1].strip()

        return TailorMessageResponse(
            status="success",
            subject=subject,
            message=body
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6773) 