from arize.otel import register
from openinference.instrumentation.litellm import LiteLLMInstrumentor
import litellm
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

# Setup OTel via Arize convenience function
tracer_provider = register(
    space_id=os.getenv("ARIZE_SPACE_ID", "your-space-id"),
    api_key=os.getenv("ARIZE_API_KEY", "your-api-key"),
    project_name="mcp-for-hiring"
)

# Instrument LiteLLM
LiteLLMInstrumentor().instrument(tracer_provider=tracer_provider)

TAILOR_MESSAGE_SERVICE_URL = "http://localhost:6773/tailor-message"

def process_tailor_message(company_name: str, job_title: str, salary: str, candidate_name: str, description: str) -> dict:
    """
    Process a request to create a personalized outreach message by calling the tailor message service.
    
    Args:
        company_name: Name of the company
        job_title: Title of the position
        salary: Salary information
        candidate_name: Name of the candidate
        description: Job description
        
    Returns:
        Dictionary containing the status and generated message
    """
    try:
        with httpx.Client() as client:
            response = client.post(
                TAILOR_MESSAGE_SERVICE_URL,
                json={
                    "company_name": company_name,
                    "job_title": job_title,
                    "salary": salary,
                    "candidate_name": candidate_name,
                    "description": description
                }
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to generate message: {str(e)}"
        }

if __name__ == "__main__":
    # Test data
    test_data = {
        "company_name": "TechCorp Solutions",
        "job_title": "Senior Software Engineer",
        "salary": "$120,000 - $150,000 annually",
        "candidate_name": "Alex Johnson",
        "description": "We're looking for an experienced software engineer to join our cloud infrastructure team. The role involves designing and implementing scalable solutions, mentoring junior developers, and contributing to our microservices architecture."
    }
    
    print("Testing process_tailor_message with sample data...")
    print("\nInput parameters:")
    for key, value in test_data.items():
        print(f"{key}: {value}")
    
    print("\nGenerating message...")
    result = process_tailor_message(**test_data)
    
    print("\nResult:")
    if result["status"] == "success":
        print("\nSubject:", result["subject"])
        print("\nMessage:", result["message"])
    else:
        print("Error:", result["error"]) 