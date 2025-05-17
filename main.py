# server.py
from mcp.server.fastmcp import FastMCP
from typing import Dict, List
from profiles import find_best_candidate, Profile

# Create an MCP server for hiring
mcp = FastMCP("Hiring-MCP")


@mcp.tool()
def find_candidate(department: str, required_skills: List[str]) -> Dict[str, str]:
    """
    Find the best candidate for a position based on department and required skills.
    
    Args:
        department: The department name (e.g., "Engineering", "Marketing")
        required_skills: List of required skills for the position
        
    Returns:
        Dictionary containing candidate name and title if found, or error message if not found
    """
    best_match = find_best_candidate(department, required_skills)
    
    if best_match:
        return {
            "status": "success",
            "candidate_name": best_match.name,
            "candidate_title": best_match.title
        }
    else:
        return {
            "status": "not_found",
            "message": f"No suitable candidate found for {department} department with required skills: {', '.join(required_skills)}"
        }


@mcp.resource("departments://list")
def list_departments() -> List[str]:
    """Get a list of available departments with candidates"""
    return ["Engineering", "Marketing"]


@mcp.resource("candidate://{name}")
def get_candidate_details(name: str) -> Dict[str, any]:
    """Get detailed information about a specific candidate"""
    from profiles import PROFILES
    
    candidate = next((p for p in PROFILES if p.name.lower() == name.lower()), None)
    if not candidate:
        return {"error": f"Candidate {name} not found"}
        
    return {
        "name": candidate.name,
        "title": candidate.title,
        "department": candidate.department,
        "experience_years": candidate.experience_years,
        "skills": candidate.skills
    }


@mcp.tool()
def tailor_message(job_details: Dict[str, str], organization: Dict[str, str], candidate_profile: Dict[str, any]) -> Dict[str, str]:
    """
    Create a personalized outreach message for a candidate based on job details, organization info, and candidate profile.
    
    Args:
        job_details: Dictionary containing job information like:
            - title: Job title
            - description: Job description
            - requirements: Key requirements
            - benefits: Job benefits
        organization: Dictionary containing organization details like:
            - name: Company name
            - description: Company description
            - culture: Company culture highlights
            - values: Company values
        candidate_profile: Dictionary containing candidate information like:
            - name: Candidate's name
            - experience: Relevant experience
            - skills: Key skills
            - current_role: Current position
            
    Returns:
        Dictionary containing the tailored message and subject line
    """
    # Extract key information
    candidate_name = candidate_profile.get("name", "").split()[0]  # First name
    job_title = job_details.get("title", "the role")
    company_name = organization.get("name", "our company")
    
    # Create personalized message
    message = f"""Hi {candidate_name},

I hope this message finds you well. I came across your profile and was particularly impressed by your experience in {candidate_profile.get('current_role', 'your current role')} and your expertise in {', '.join(candidate_profile.get('skills', [])[:3])}.

We're looking for a {job_title} at {company_name}, and your background caught my attention. {organization.get('description', '')}

What particularly stood out to me was:
- Your experience in {candidate_profile.get('experience', 'relevant areas')}
- Your strong background in {', '.join(candidate_profile.get('skills', [])[:2])}
- The alignment between your work and our {organization.get('values', 'values')}

{job_details.get('description', '')}

Some highlights about working with us:
{job_details.get('benefits', 'We offer competitive benefits and a great work environment.')}

Would you be interested in having a conversation about this opportunity? I'd love to share more details about the role and learn more about your career aspirations.

Looking forward to your response!

Best regards,
[Your name]
{organization.get('name', '')}"""

    subject = f"Exciting {job_title} Opportunity at {company_name}"
    
    return {
        "status": "success",
        "subject": subject,
        "message": message
    }