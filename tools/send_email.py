import os
from dotenv import load_dotenv
from arcadepy import Arcade 

load_dotenv()

# Global variables for authorization
API_KEY = os.getenv("ARCADE_API_KEY")
USER_ID = os.getenv("ARCADE_USER_ID")
client = Arcade()

def initialize_email_auth():
    """Initialize and verify email authorization"""
    # Authorize the tool
    auth_response = client.tools.authorize(
        tool_name="Google.SendEmail@1.2.1",
        user_id=USER_ID,
    )

    # Check if authorization is completed
    if auth_response.status != "completed":
        print(f"Click this link to authorize: {auth_response.url}")

    # Wait for the authorization to complete
    auth_response = client.auth.wait_for_completion(auth_response)

    if auth_response.status != "completed":
        raise Exception("Authorization failed")

    print("🚀 Authorization successful!")

def process_send_email(subject: str, body: str, recipient: str) -> dict:
    """
    Process and send an email using Google's email service through Arcade.
    
    Args:
        subject: Email subject line
        body: Email body content
        recipient: Email address of the recipient
        
    Returns:
        Dictionary containing the status of the email sending operation
    """
    try:
        # Ensure authorization is complete
        initialize_email_auth()
        
        # Send the email
        result = client.tools.execute(
            tool_name="Google.SendEmail@1.2.1",
            input={
                "subject": subject,
                "body": body,
                "recipient": recipient
            },
            user_id=USER_ID,
        )
        
        return {
            "status": "success",
            "message": "Email sent successfully",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send email: {str(e)}"
        }

if __name__ == "__main__":
    # Example usage
    result = process_send_email(
        subject="Hello",
        body="Test email",
        recipient="miles.jo.parker@gmail.com"
    )
    print(result)