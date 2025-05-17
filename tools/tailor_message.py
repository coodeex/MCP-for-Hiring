from arize.otel import register
from openinference.instrumentation.litellm import LiteLLMInstrumentor
import litellm
import os
from dotenv import load_dotenv
load_dotenv()

# Setup OTel via Arize convenience function
tracer_provider = register(
    space_id=os.getenv("ARIZE_SPACE_ID", "your-space-id"),
    api_key=os.getenv("ARIZE_API_KEY", "your-api-key"),
    project_name="mcp-for-hiring"
)

# Instrument LiteLLM
LiteLLMInstrumentor().instrument(tracer_provider=tracer_provider)

def process_tailor_message(company_name: str, job_title: str, salary: str, candidate_name: str, description: str) -> dict:
    """
    Process a request to create a personalized outreach message using LiteLLM.
    
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
        prompt = f"""Create a professional and engaging outreach message to a potential job candidate with the following details:
        
Company: {company_name}
Position: {job_title}
Salary: {salary}
Candidate: {candidate_name}
Job Description: {description}

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

        return {
            "status": "success",
            "subject": subject,
            "message": body
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
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