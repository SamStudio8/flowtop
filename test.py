from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import json



PROCESSES = {}
class MyServer(BaseHTTPRequestHandler):
        
    def do_POST(self):
        content_type = self.headers.get('content-type')
        
        # refuse to receive non-json content
        if content_type != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        #print(json.dumps(message, indent=4, sort_keys=True))

        event = message.get("event")
        if not event:
            self.send_response(400)
            self.end_headers()
            return
        if event == "process_completed":
            print(message["trace"]["process"], event)

            p = message["trace"]["process"]
            if p not in PROCESSES:
                PROCESSES[p] = {
                    "count": 0,
                    "last_seen": None,
                }
            PROCESSES[p]["count"] += 1
            PROCESSES[p]["last_seen"] = datetime.datetime.now()
            print(PROCESSES[p])
            #print(json.dumps(message, indent=4, sort_keys=True))
 
        

        
httpd = HTTPServer(('localhost', 9008), MyServer)
httpd.serve_forever()
