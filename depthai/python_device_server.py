import time
import socket
import fcntl
import struct
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import mimetypes
import json
import threading

PORT = _PORT_NUMBER
STREAMS = ['color', 'left', 'right']
BOUNDARY = 'jpgboundary-dc0ecf0e4db185d41450'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        -1071617759,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode())
    )[20:24])

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

# Threads reading the latest frame
latestFrame = {}
frameThread = {}
def readFrameThread(stream):
    global latestFrame
    while True:
        latestFrame[stream] = node.io[stream].get()
for stream in STREAMS:
    node.info(f"Starting thread for '{stream}' messages")
    frameThread[stream] = threading.Thread(target=readFrameThread, args=(stream, ))
    frameThread[stream].start()

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:

            # Custom paths first
            if self.path.startswith('/stream/'):
                stream = self.path.split('/stream/')[1]
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', f'multipart/x-mixed-replace; boundary={BOUNDARY}')
                self.end_headers()
                fpsCounter = 0
                timeCounter = time.time()
                prevSequenceNum = -1

                try:
                    while True:
                        global latestFrame
                        if stream not in latestFrame:
                            time.sleep(1)
                            continue
                        if latestFrame[stream].getSequenceNum() == prevSequenceNum:
                            time.sleep(0.01)
                            continue
                        # Reference the latest image
                        jpegImage = latestFrame[stream]
                        prevSequenceNum = jpegImage.getSequenceNum()
                        self.wfile.write(f'--{BOUNDARY}\r\n'.encode())
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', str(len(jpegImage.getData())))
                        self.end_headers()
                        self.wfile.write(jpegImage.getData())
                        self.wfile.write(b'\r\n')

                        fpsCounter = fpsCounter + 1
                        if time.time() - timeCounter > 1:
                            node.info(f'FPS: {fpsCounter}')
                            fpsCounter = 0
                            timeCounter = time.time()
                except Exception as ex:
                    node.info(f"Streaming '{stream}' stopped")

            elif self.path == '/api/fw_version':
                version = {
                    'fw_version': __version__
                }
                versionJson = json.dumps(version)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', len(versionJson))
                self.end_headers()
                self.wfile.write(versionJson.encode())

            elif self.path == '/api/device_id':
                deviceId = {
                    'device_id': __device_id__
                }
                deviceIdJson = json.dumps(deviceId)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', len(deviceIdJson))
                self.end_headers()
                self.wfile.write(deviceIdJson.encode())
            elif self.path == '/api/stats':
                msg = node.io['sys'].get()
                stats = {
                    'cpu_css_percent': msg.leonCssCpuUsage.average,
                    'cpu_mss_percent': msg.leonMssCpuUsage.average,

                    'mem_css_used': msg.leonCssMemoryUsage.used,
                    'mem_css_total': msg.leonCssMemoryUsage.total,
                    'mem_mss_used': msg.leonMssMemoryUsage.used,
                    'mem_mss_total': msg.leonMssMemoryUsage.total,

                    'mem_ddr_used': msg.ddrMemoryUsage.used,
                    'mem_ddr_total': msg.ddrMemoryUsage.total,
                    'mem_cmx_used': msg.cmxMemoryUsage.used,
                    'mem_cmx_total': msg.cmxMemoryUsage.total,

                    'temp_css': msg.chipTemperature.css,
                    'temp_mss': msg.chipTemperature.mss,
                    'temp_upa': msg.chipTemperature.upa,
                    'temp_dss': msg.chipTemperature.dss,
                    'temp_average': msg.chipTemperature.average,
                }
                statsJson = json.dumps(stats)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', len(statsJson))
                self.end_headers()
                self.wfile.write(statsJson.encode())

            else:
                # Asset paths second

                # Respond with index.html by default
                if self.path == '/':
                    self.path = '/index.html'
                # Remove leading slash
                path = self.path[1:]
                # node.info(f'About to serve: {self.path} as asset: {path}')
                # Fetch from assets
                asset = pipeline.getAsset(path)
                if asset is not None:
                    node.info(f'Served OK: {path}')
                    self.send_response(200)
                    self.send_header('Content-Type', mimetypes.guess_type(path)[0])
                    self.send_header('Content-Length', len(asset))
                    self.end_headers()
                    self.wfile.write(asset)
                else:
                    node.error(f'Served 404: {path}')
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'<h1>404!</h1>')

        except Exception as ex:
            node.info(f'Exception: {str(ex)}')

with ThreadingSimpleServer(("", PORT), HTTPHandler) as httpd:
    node.info(f"Serving at {get_ip_address('re0')}:{PORT}")
    httpd.serve_forever()

for stream in STREAMS:
    node.info(f"Joining thread for '{stream}' messages")
    frameThread[stream].join()