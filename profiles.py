from dataclasses import dataclass
from typing import List

@dataclass
class Profile:
    name: str
    title: str
    skills: List[str]
    experience_years: int
    department: str

# Sample profiles database
PROFILES = [
    Profile(
        name="John",
        title="Software Developer",
        skills=["Python", "JavaScript", "React", "Docker", "Git"],
        experience_years=5,
        department="Engineering"
    ),
    Profile(
        name="Anna",
        title="Marketing Specialist",
        skills=["Content Marketing", "Social Media", "SEO", "Analytics", "Campaign Management"],
        experience_years=3,
        department="Marketing"
    )
]

def find_best_candidate(department: str, required_skills: List[str]) -> Profile | None:
    """
    Find the best candidate based on department and required skills
    Returns None if no suitable candidate is found
    """
    best_match = None
    best_match_score = 0
    
    for profile in PROFILES:
        if profile.department.lower() != department.lower():
            continue
            
        # Calculate match score based on required skills
        skill_match_score = sum(1 for skill in required_skills 
                              if any(s.lower() == skill.lower() for s in profile.skills))
        
        if skill_match_score > best_match_score:
            best_match_score = skill_match_score
            best_match = profile
    
    return best_match 