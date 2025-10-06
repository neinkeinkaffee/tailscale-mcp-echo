from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request
from urllib.parse import unquote
import json

mcp = FastMCP(name="Tailscale Identity Echo Server")


@mcp.tool()
async def greet() -> str:
    """Reads the identity request headers passed in from Tailscale Serve and returns a greeting.

    Returns:
        str: A greeting containing the user's name, login (typically an email or Github handle),
        and profile picture URL.
    """

    request: Request = get_http_request()

    user_login = request.headers.get("Tailscale-User-Login", "Unknown")
    user_name = request.headers.get("Tailscale-User-Name", "Unknown")
    user_profile_picture = request.headers.get("Tailscale-User-Profile-Pic", "Unknown")

    user_capabilities_encoded = request.headers.get("Tailscale-User-Capabilities", "")
    # Decode the URL (Percent) encoding.
    # This converts strings like '%7B%22role...%22%7D' back to '{"role...":"..."}'.
    user_capabilities_decoded = unquote(user_capabilities_encoded)
    data = json.loads(user_capabilities_decoded)
    print(f"Successfully decoded capability header. Found is: {data}")

    role = data.get("example.com/cap/greet", [{}])[0].get("role")

    return f"""Hello, {user_name}!
You're logged in to Tailscale as {user_login}.
With a profile picture at this URL: {user_profile_picture}.
Your role is {role}."""

@mcp.tool()
async def tellJoke() -> str:
    """Reads the identity request headers passed in from Tailscale Serve and returns a joke.

    Returns:
        str: Based on the role of the user for this app, the joke will be ok or very good.
    """

    request: Request = get_http_request()

    user_login = request.headers.get("Tailscale-User-Login", "Unknown")
    user_name = request.headers.get("Tailscale-User-Name", "Unknown")
    user_profile_picture = request.headers.get("Tailscale-User-Profile-Pic", "Unknown")

    user_capabilities_encoded = request.headers.get("Tailscale-User-Capabilities", "")
    # Decode the URL (Percent) encoding.
    # This converts strings like '%7B%22role...%22%7D' back to '{"role...":"..."}'.
    user_capabilities_decoded = unquote(user_capabilities_encoded)
    data = json.loads(user_capabilities_decoded)
    print(f"Successfully decoded capability header. Found is: {data}")

    role = data.get("example.com/cap/greet", [{}])[0].get("role")

    if role == "👑":
        return f"""This user has access to very good jokes due to their role {role}. Here comes one.
        
        The East Frisians and the Bavarians are playing football. 
        Suddenly a train goes past nearby and whistles. The East Frisians think the game has ended and go home! 
        (pause) Half an hour later the Bavarians score the first goal!"""
    else:
        return """This user only has access to ok jokes. Here comes one.
        
        Why does the tide ebb and flow? – 
        Because when the sea saw the East Frisians, it got such a shock that it ran away. 
        Now it returns twice a day to see if they're still there!"""
