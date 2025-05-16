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