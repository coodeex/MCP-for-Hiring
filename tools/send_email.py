import os
from dotenv import load_dotenv
from arcadepy import Arcade 

load_dotenv()


API_KEY = os.getenv("ARCADE_API_KEY")
USER_ID = os.getenv("ARCADE_USER_ID")

client = Arcade()

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

result = client.tools.execute(
    tool_name="Google.SendEmail@1.2.1",
    input={
        "subject": "Hello",
        "body": "Testt",
        "recipient": "miles.jo.parker@gmail.com"
    },
    user_id=USER_ID,
)

print(result)