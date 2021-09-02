from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys

hostName = "localhost"
serverPort = 8080
KEYWORD = "$~"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        fileToOpen = self.path
        print("---->", self.path)
        if self.path == "/":
            fileToOpen = "/index.html"
        if self.path != "/favicon.ico":
            with open(r"" + f"{os.path.dirname(sys.argv[0])}" + fileToOpen, "r") as fp:
                result = self.read_HTML(fp)
                self.wfile.write(bytes(result, "utf-8"))
        #except:
            #self.wfile.write(bytes("<html><head><title>FILE NOT FOUND</title></head>", "utf-8"))
            
    def read_HTML(self, fp):
        final_text = ""
        for line in fp:
            HTML_LINE = line
            HTML_LINE = self.check_additional_files(HTML_LINE, "css", "<style>", "</style>")
            HTML_LINE = self.check_additional_files(HTML_LINE, "js", "<script>", "</script>")
            final_text += HTML_LINE
        return final_text
    
    def check_additional_files(self, line, expected, tag, ender):
        HTML_LINE = line
        exp = KEYWORD + expected + " "
        if (HTML_LINE.find(exp) != -1):
            HTML_LINE = HTML_LINE.replace(exp, "")
            HTML_LINE = HTML_LINE.strip()
            try:
                with open(r"" + HTML_LINE + "." + expected, "r") as xp:
                    HTML_LINE = tag
                    for x in xp:
                        HTML_LINE += x
                    HTML_LINE += ender                       
            except:
                print("File Import Failed ->", HTML_LINE)
                HTML_LINE = "<i>Failed to load either CSS or JS (Server's Fault)</i>"
        return HTML_LINE
        

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
