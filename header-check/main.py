import time
from email.header import decode_header
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = 8080

class EchoHeadersHandler(BaseHTTPRequestHandler):
    def decode_mime_header(self, encoded_string: str) -> str:
        """
        Decodes a MIME-encoded header string (RFC 2047) into a readable string.

        This handles both Q-encoding and Base64 encoding.
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

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        encoded_header_value = self.headers.get('Tailscale-User-Capabilities')
        print("Encoded header value:", encoded_header_value)
        try:
            decoded_header_value = self.decode_mime_header(encoded_header_value)
            print("Decoded header value:", decoded_header_value)
            self.wfile.write(decoded_header_value.encode("utf-8"))
        except Exception as e:
            print(f"Failed to decode header value: {e}")


def run(server_class=HTTPServer, handler_class=EchoHeadersHandler, port=PORT_NUMBER):
    server_address = (HOST_NAME, port)
    httpd = server_class(server_address, handler_class)

    print(f"[{time.asctime()}] Server starting up...")
    print(f"[{time.asctime()}] Listening on http://{HOST_NAME}:{port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[{time.asctime()}] Server is shutting down.")
        httpd.server_close()

    print(f"[{time.asctime()}] Server stopped successfully.")

if __name__ == "__main__":
    run()
