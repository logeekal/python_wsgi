from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import os 

curr_path = os.getcwd()
main_path =  os.path.join(curr_path, 'main.html')

index_html = """
<html>
<body>
	<form method="get" action="/login">
		<p>
			Name: <input type=text name="name">
		</p>
		
		<p>
			Hobbies :
			<input name="hobbies" type="checkbox" value ="Software"> Software
			<input name="hobbies" type="checkbox"> Hardware
		</p>
		
		<p>
			<input type=Submit value="Submit">
		</p>
	</form>
</body>
</html>
"""

login_html = """
<html>
<head> <title> Welcome %s </title> </head>
<body>
%s, You are now correctly logged in
</body>
</html>
"""

def application(environ, start_response):
	

	d = parse_qs(environ['QUERY_STRING'])
	
	name = d.get('name',[''])[0]
	
	if environ['PATH_INFO'] == '/':
		response_body = index_html 
	elif environ['PATH_INFO'] == '/login':
		response_body = login_html % (name,name)	

	status = '200 OK'
	
	response_headers = [
						('Content-Type','text/html'),
						('Content-Length', str(len(response_body)))
						]
	start_response(status, response_headers)
	
	return [response_body]	
	
httpd =  make_server('localhost',8052,application)
httpd.serve_forever()