from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class WebhookHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        print("\nWebhook received:")
        print(json.loads(body))

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            b'{"message":"Webhook received successfully"}'
        )


server = HTTPServer(("127.0.0.1", 9000), WebhookHandler)

print("Webhook receiver running on http://127.0.0.1:9000")

server.serve_forever()
