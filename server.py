import SimpleHTTPServer
import SocketServer
from urlparse import parse_qs, urlparse
import cgi
import RPi.GPIO as GPIO
import json

port1 = 32
port2 = 36
port3 = 38
port4 = 40

state = [False, False, False, False]

PORT = 8000

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme
GPIO.setup(port1, GPIO.OUT) # LED pin set as output
GPIO.setup(port2, GPIO.OUT) # PWM pin set as output
GPIO.setup(port3, GPIO.OUT) # LED pin set as output
GPIO.setup(port4, GPIO.OUT) # PWM pin set as output


GPIO.output(port1, False)
GPIO.output(port2, True)

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_POST(self):
		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={"REQUEST_METHOD": "POST"}
		)
		handleStateChange(form)
		self.send_response(200)
	def do_GET(self):
		if 'status' in self.path:
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(json.dumps(state))
		else:
			SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


Handler = MyRequestHandler

def handleStateChange(form):
	state[0] = form['btn1'].value == 'true'
	state[1] = form['btn2'].value == 'true'
	state[2] = form['btn3'].value == 'true'
	state[3] = form['btn4'].value == 'true'

	GPIO.output(port1, state[0])
	GPIO.output(port2, state[1])
	GPIO.output(port3, state[2])
	GPIO.output(port4, state[3])

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()