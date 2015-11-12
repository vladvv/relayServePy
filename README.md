Server info:
Runs on Raspberry Pi, with direct access to the GPIO ports which drive relays.
Using SimpleHTTPServer Python library, server knows how to do three things:
1) Respond to GET request with index.html
2) Respond to GET to "status" to respond with light status (ex: on/on/off/on)
3) Receive a POST request to update light status

Client currently polls server every 2 seconds, this is crap and should be changed if this is to be used by multiple people.
