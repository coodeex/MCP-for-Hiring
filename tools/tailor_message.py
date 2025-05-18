import httpx
from dotenv import load_dotenv

load_dotenv()

TAILOR_MESSAGE_SERVICE_URL = "http://localhost:6773/tailor-message"

def process_tailor_message(company_name: str, job_title: str, salary: str, candidate_name: str, candidate_email: str, description: str) -> dict:
    """
    Process a request to create a personalized outreach message by calling the tailor message service.
    
    Args:
        company_name: Name of the company
        job_title: Title of the position
        salary: Salary information
        candidate_name: Name of the candidate
        candidate_email: Email of the candidate
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
            response_data = response.json()
            # Add the candidate email to the response
            response_data["candidate_email"] = candidate_email
            return response_data
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
        "candidate_email": "alex.johnson@example.com",
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
        print("\nCandidate Email:", result["candidate_email"])
    else:
        print("Error:", result["error"]) 