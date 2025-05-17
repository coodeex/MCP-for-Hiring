import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from arcadepy import Arcade

app = FastAPI()
load_dotenv()

# Global variables for authorization
API_KEY = os.getenv("ARCADE_API_KEY")
USER_ID = os.getenv("ARCADE_USER_ID")
client = Arcade()

class EmailRequest(BaseModel):
    subject: str
    body: str
    recipient: str

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

@app.post("/send-email")
async def send_email(email_request: EmailRequest):
    """
    Send an email using Google's email service through Arcade.
    """
    try:
        # Ensure authorization is complete
        initialize_email_auth()
        
        # Send the email
        result = client.tools.execute(
            tool_name="Google.SendEmail@1.2.1",
            input={
                "subject": email_request.subject,
                "body": email_request.body,
                "recipient": email_request.recipient
            },
            user_id=USER_ID,
        )
        
        return {
            "status": "success",
            "message": "Email sent successfully",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=7253) 