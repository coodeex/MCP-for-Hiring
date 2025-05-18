from dataclasses import dataclass
from typing import List
import httpx

@dataclass
class Profile:
    name: str
    title: str
    skills: List[str]
    experience_years: int
    department: str

TOOLHOUSE_URL = "https://agents.toolhouse.ai/500de86f-63aa-4a56-800a-1eef2e4257c1"
TOOLHOUSE_AUTH = "Bearer th-db1eXm0Nl2qf9_oAPTKJAWRFA8HrhOUAHhF-FK-11-A"

def find_best_candidate(search_query: str) -> str:
    """
    Find the best candidate by querying the Toolhouse API
    Returns the formatted response text from Toolhouse
    """
    headers = {
        "Authorization": TOOLHOUSE_AUTH
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                TOOLHOUSE_URL,
                headers=headers,
                json={"criteria": search_query}
            )
            response.raise_for_status()
            return response.text
    except httpx.HTTPError as e:
        return f"Error contacting Toolhouse API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}" 