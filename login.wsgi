from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

html ="""
<html>
<head> <title> Welcome %s </title> </head>
<body>
%s, You are now correctly logged in
</body>
</html>
"""

def application(environ, start_response) :
	
	#Now parsing the GET requests
	d = parse_qs(environ['QUERY_STRING'])
	
	name = d.get('name',[''])[0]
	
	response_body =  html % (name, name)
	
	#Setting the response type as HTML
	response_header = [
						('Content-Type','text/html'),
						('Content-Length' , str(len(response_body)))
						]

	status = '200 OK'
	
	start_response(status, response_header)
	return [response_body]		