import webbrowser
import httpx

CANDIDATE_SERVICE_URL = "http://localhost:7624/find-candidate"

def find_best_candidate(search_query: str) -> dict:
    """
    Find the best candidate by calling the candidate service.
    
    Args:
        search_query: The search criteria for finding candidates
        
    Returns:
        Dictionary containing the best matching candidate info
    """
    try:
        with httpx.Client() as client:
            response = client.post(
                CANDIDATE_SERVICE_URL,
                json={
                    "search_query": search_query
                }
            )
            response.raise_for_status()
            result = response.json()
            
            # If we have a candidate link, open it in the browser
            if "candidate_link" in result:
                webbrowser.open(result["candidate_link"])
                
            return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to find candidate: {str(e)}"
        }

if __name__ == "__main__":
    # Example search query
    search_query = """Looking for a software engineer with:
    - Strong experience in Python development
    - Background in machine learning or AI
    - Good communication skills
    - Experience with cloud platforms"""
    
    # Call the function and print results
    result = find_best_candidate(search_query)
    print("\nSearch Result:")
    print(result)
    
    # Print candidate details if available
    if "candidate_details" in result:
        print("\nCandidate Details:")
        print(result["candidate_details"]) 