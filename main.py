# server.py
from mcp.server.fastmcp import FastMCP
from typing import Dict, List
from tools.find_candidate import find_best_candidate
from tools.send_email import process_send_email
# Create an MCP server for hiring
mcp = FastMCP("Hiring-MCP")


@mcp.tool()
def find_candidate(search_query: str) -> Dict[str, str]:
    """
    Find the best candidate based on the hiring manager's search query.
    
    Args:
        search_query: The search criteria provided by the hiring manager (e.g., "Looking for a senior software engineer with 5+ years of Python experience")
        
    Returns:
        The analysis of the best candidate and the link to the candidate's profile. Proceed by drafting a tailored message to the candidate.
    """
    result = find_best_candidate(search_query)
    return result



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
            - salary: Salary information
        organization: Dictionary containing organization details like:
            - name: Company name
            - description: Company description
        candidate_profile: Dictionary containing candidate information like:
            - name: Candidate's name
            - email: Candidate's email
            
    Returns:
        Show the tailored message and subject line. Proceed by sending the email.
    """
    from tools.tailor_message import process_tailor_message
    
    return process_tailor_message(
        company_name=organization.get("name", ""),
        job_title=job_details.get("title", ""),
        salary=job_details.get("salary", "Competitive"),
        candidate_name=candidate_profile.get("name", ""),
        candidate_email=candidate_profile.get("email", ""),
        description=job_details.get("description", "")
    )



@mcp.tool()
def send_email(subject: str, body: str, recipient: str) -> dict:
    """
    Send an email using Google's email service through Arcade.
    
    Args:
        subject: Email subject line
        body: Email body content
        recipient: Email address of the recipient
        
    Returns:
        Dictionary containing the status of the email sending operation
    """
    return process_send_email(subject, body, recipient)