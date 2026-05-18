from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code=200, data=None):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if data:
            self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def do_GET(self):
        if self.path == '/':
            self._send_response(data={"message": "Game AI Agent API", "version": "1.0.0"})
        elif self.path == '/health':
            self._send_response(data={"status": "healthy"})
        elif self.path == '/api/v1/collaboration/agents/list':
            agents = [
                {"key": "designer", "name": "游戏设计师", "avatar": "👩‍🎨"},
                {"key": "coder", "name": "代码专家", "avatar": "🧑‍💻"},
                {"key": "perf", "name": "性能专家", "avatar": "🚀"},
                {"key": "tester", "name": "测试专家", "avatar": "🔬"}
            ]
            self._send_response(data={"agents": agents})
        else:
            self._send_response(404, {"error": "Not found"})
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        if self.path == '/api/v1/chat/conversations':
            self._send_response(data={"conversation_id": "test-conv-123", "title": "新对话"})
        elif self.path == '/api/v1/chat/conversations/test-conv-123/messages':
            try:
                data = json.loads(body)
                response = {
                    "message_id": "msg-123",
                    "role": "assistant",
                    "content": "这是一个测试回复！您的问题已收到。"
                }
                self._send_response(data=response)
            except:
                self._send_response(500, {"error": "Invalid JSON"})
        else:
            self._send_response(404, {"error": "Not found"})

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"🚀 服务已启动！")
    print(f"地址: http://localhost:{port}")
    print(f"健康检查: http://localhost:{port}/health")
    print(f"Agent列表: http://localhost:{port}/api/v1/collaboration/agents/list")
    print("按 Ctrl+C 停止服务")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
