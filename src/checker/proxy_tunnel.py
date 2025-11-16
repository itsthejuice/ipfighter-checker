"""
SOCKS5 to HTTP proxy tunnel for Playwright
"""

import socket
import threading
import socks
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import select
from typing import Optional
import logging
from ..models.proxy import ProxyInfo

logger = logging.getLogger(__name__)


class SOCKS5TunnelHandler(BaseHTTPRequestHandler):
    """HTTP proxy handler that tunnels through SOCKS5"""
    
    def __init__(self, *args, socks_proxy: ProxyInfo = None, **kwargs):
        self.socks_proxy = socks_proxy
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """Log tunnel requests"""
        logger.debug(f"[TUNNEL REQUEST] {format % args}")
        print(f"[TUNNEL REQUEST] {format % args}")
    
    def do_CONNECT(self):
        """Handle CONNECT method for HTTPS"""
        try:
            logger.info(f"[TUNNEL] CONNECT request to {self.path}")
            print(f"[TUNNEL] CONNECT to {self.path}")
            
            # Parse target host and port
            host, port = self.path.split(':')
            port = int(port)
            
            # Create SOCKS5 connection
            sock = socks.socksocket()
            sock.set_proxy(
                socks.SOCKS5,
                self.socks_proxy.host,
                self.socks_proxy.port,
                username=self.socks_proxy.username,
                password=self.socks_proxy.password
            )
            
            logger.info(f"[TUNNEL] Connecting to {host}:{port} via SOCKS5...")
            # Connect to target through SOCKS5 with timeout
            sock.settimeout(30)  # 30 second connection timeout
            sock.connect((host, port))
            sock.settimeout(None)  # Remove timeout after connection
            logger.info(f"[TUNNEL] Connected to {host}:{port}")
            
            # Send success response
            self.send_response(200, 'Connection Established')
            self.end_headers()
            
            # Start bidirectional forwarding
            self._forward_data(self.connection, sock)
            
        except Exception as e:
            logger.error(f"[TUNNEL] CONNECT error: {e}")
            print(f"[TUNNEL] ✗ CONNECT error: {e}")
            self.send_error(500, f"Tunnel error: {str(e)}")
    
    def do_GET(self):
        """Handle GET requests"""
        self._handle_request('GET')
    
    def do_POST(self):
        """Handle POST requests"""
        self._handle_request('POST')
    
    def do_HEAD(self):
        """Handle HEAD requests"""
        self._handle_request('HEAD')
    
    def _handle_request(self, method):
        """Handle HTTP requests through SOCKS5"""
        try:
            # Parse URL
            url = self.path
            if url.startswith('http://'):
                url = url[7:]
            
            host_port = url.split('/')[0]
            if ':' in host_port:
                host, port = host_port.split(':')
                port = int(port)
            else:
                host = host_port
                port = 80
            
            # Create SOCKS5 connection
            sock = socks.socksocket()
            sock.set_proxy(
                socks.SOCKS5,
                self.socks_proxy.host,
                self.socks_proxy.port,
                username=self.socks_proxy.username,
                password=self.socks_proxy.password
            )
            sock.connect((host, port))
            
            # Forward request
            request_line = f"{method} {self.path} HTTP/1.1\r\n"
            sock.sendall(request_line.encode())
            
            # Forward headers
            for header, value in self.headers.items():
                sock.sendall(f"{header}: {value}\r\n".encode())
            sock.sendall(b"\r\n")
            
            # Forward body if POST
            if method == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    body = self.rfile.read(content_length)
                    sock.sendall(body)
            
            # Receive response
            response = b''
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                if len(chunk) < 4096:
                    break
            
            # Send response to client
            self.wfile.write(response)
            
            sock.close()
            
        except Exception as e:
            self.send_error(500, f"Request error: {str(e)}")
    
    def _forward_data(self, source, destination):
        """Forward data bidirectionally"""
        sockets = [source, destination]
        timeout = 120  # Increased timeout to 120 seconds
        
        while True:
            try:
                ready_sockets, _, _ = select.select(sockets, [], [], timeout)
                
                if not ready_sockets:
                    break
                
                for sock in ready_sockets:
                    try:
                        data = sock.recv(8192)  # Increased buffer size
                        if not data:
                            return
                        
                        if sock is source:
                            destination.sendall(data)
                        else:
                            source.sendall(data)
                    except Exception as e:
                        logger.debug(f"[TUNNEL] Socket error during forwarding: {e}")
                        return
            except Exception as e:
                logger.debug(f"[TUNNEL] Select error: {e}")
                return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """HTTPServer that handles each request in a separate thread"""
    daemon_threads = True
    allow_reuse_address = True


class ProxyTunnel:
    """SOCKS5 to HTTP proxy tunnel server"""
    
    def __init__(self, socks_proxy: ProxyInfo, local_port: Optional[int] = None):
        """
        Initialize proxy tunnel
        
        Args:
            socks_proxy: SOCKS5 proxy information
            local_port: Local port to bind to (random if None)
        """
        self.socks_proxy = socks_proxy
        self.local_port = local_port or self._find_free_port()
        self.server = None
        self.thread = None
        self.running = False
    
    def _find_free_port(self) -> int:
        """Find a free port"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]
    
    def start(self):
        """Start the tunnel server"""
        logger.info(f"Starting tunnel server on port {self.local_port}")
        print(f"[TUNNEL] Starting server on localhost:{self.local_port}")
        
        def handler_factory(*args, **kwargs):
            return SOCKS5TunnelHandler(*args, socks_proxy=self.socks_proxy, **kwargs)
        
        # Use ThreadedHTTPServer to handle multiple concurrent requests
        self.server = ThreadedHTTPServer(('127.0.0.1', self.local_port), handler_factory)
        self.running = True
        
        def run_server():
            logger.info("Tunnel server thread started")
            try:
                # Use serve_forever which is more robust than handle_request loop
                self.server.serve_forever()
            except Exception as e:
                if self.running:
                    logger.error(f"Tunnel server error: {e}")
                    print(f"[TUNNEL] Server error: {e}")
        
        self.thread = threading.Thread(target=run_server, daemon=True)
        self.thread.start()
        logger.info("Tunnel server running")
        print(f"[TUNNEL] Server running on localhost:{self.local_port}")
    
    def stop(self):
        """Stop the tunnel server"""
        logger.info("Stopping tunnel server...")
        print("[TUNNEL] Stopping server...")
        self.running = False
        if self.server:
            try:
                # Shutdown the server properly
                self.server.shutdown()
                self.server.server_close()
                logger.info("Tunnel server stopped")
                print("[TUNNEL] Server stopped")
            except Exception as e:
                logger.warning(f"Error stopping tunnel: {e}")
                print(f"[TUNNEL] Warning during stop: {e}")
    
    def get_http_proxy_url(self) -> str:
        """Get the HTTP proxy URL for this tunnel"""
        return f"http://127.0.0.1:{self.local_port}"
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

