import httpx

EMAIL_SERVICE_URL = "http://localhost:7253/send-email"

def process_send_email(subject: str, body: str, recipient: str) -> dict:
    """
    Send an email by calling the email service.
    
    Args:
        subject: Email subject line
        body: Email body content
        recipient: Email address of the recipient
        
    Returns:
        Dictionary containing the status of the email sending operation
    """
    try:
        with httpx.Client() as client:
            response = client.post(
                EMAIL_SERVICE_URL,
                json={
                    "subject": subject,
                    "body": body,
                    "recipient": recipient
                }
            )
            response.raise_for_status()
            return response.json()
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