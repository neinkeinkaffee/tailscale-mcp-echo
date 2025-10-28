import json

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
from email.header import decode_header
from starlette.requests import Request

TS_USER_CAPABILITIES_HEADER = "Tailscale-App-Capabilities"
TS_USER_LOGIN_HEADER = "Tailscale-User-Login"
TS_USER_NAME_HEADER = "Tailscale-User-Name"
TS_USER_PROFILE_PIC_HEADER = "Tailscale-User-Profile-Pic"

mcp = FastMCP(name="Tailscale Identity Echo Server")


@mcp.tool()
async def greet() -> str:
    """Reads the identity request headers passed in from Tailscale Serve and returns a greeting.

    Returns:
        str: A greeting containing the user's name, login (typically an email or Github handle),
        and profile picture URL.
    """

    request: Request = get_http_request()

    user_login = request.headers.get(TS_USER_LOGIN_HEADER, "Unknown")
    print(f"Got Tailscale user login header: {user_login}")
    user_name = request.headers.get(TS_USER_NAME_HEADER, "Unknown")
    user_profile_picture = request.headers.get(TS_USER_PROFILE_PIC_HEADER, "Unknown")

    user_capabilities_encoded = request.headers.get('Tailscale-App-Capabilities')
    print(f"Got Tailscale user capability header: {user_capabilities_encoded}")
    user_capabilities_decoded = decode_mime_header(user_capabilities_encoded)
    print(f"Got Tailscale user capability header: {user_capabilities_decoded}")
    data = json.loads(user_capabilities_decoded)
    print(f"Successfully decoded capability header. Found: {user_capabilities_decoded}")

    role = data.get("example.com/cap/echo", [{}])[0].get("role")

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

    request = get_http_request()
    user_capabilities_encoded = request.headers.get(TS_USER_CAPABILITIES_HEADER, "")
    print(f"Got Tailscale user capability header: {user_capabilities_encoded}")
    user_capabilities_decoded = decode_mime_header(user_capabilities_encoded)
    print(f"Successfully decoded capability header: {user_capabilities_decoded}")
    user_capabilities_parsed = json.loads(user_capabilities_decoded)

    role = user_capabilities_parsed.get("example.com/cap/echo", [{}])[0].get("role", "")

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


def decode_mime_header(encoded_string: str) -> str:
    """
    Decodes a MIME-encoded header string (RFC 2047) into a readable string.

    Handles both Q-encoding and Base64 encoding.
    """
    decoded_parts = []
    for decoded_bytes, charset in decode_header(encoded_string):
        # If a charset is specified, use it. Otherwise, default to 'ascii'.
        if isinstance(decoded_bytes, bytes):
            if charset:
                decoded_parts.append(decoded_bytes.decode(charset))
            else:
                decoded_parts.append(decoded_bytes.decode('ascii'))
        else:
            decoded_parts.append(decoded_bytes)
    return "".join(decoded_parts)
