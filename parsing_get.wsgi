from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
from Cookie import SimpleCookie
import socket
import os 

curr_path = os.getcwd()
main_path =  os.path.join(curr_path, 'main.html')

HOST = socket.gethostname()

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



def index(environ, start_response):
	
	response_body = index_html
	
	status = '200 OK'
	
	response_headers = [
						('Content-Type','text/html'),
						('Content-Length', str(len(response_body)))
						]
						
	start_response(status, response_headers)
	
	return [response_body]


def login(environ, start_response):
	
	d = parse_qs(environ['QUERY_STRING'])
	
	name = d.get('name',[''])[0]
	
	cookie_headers = ""
	
	if 'HTTP_COOKIE' in environ:
		get_cookie = SimpleCookies(environ['HTTP_COOKIE']
		if HOST not in get_cookie:
			new_cookie = SimpleCookie()
			new_cookie[HOST]['comment']	= {'name' : name}
			cookie_headers = ('Set-Cookie',new_cookie[HOST].OutputString())
		else:
			name =  get_cookie[HOST]['comment']['name']
	else:
		new_cookie = SimpleCookie()
		new_cookie[HOST]['comment']	= {'name' : name}
		cookie_headers = ('Set-Cookie',new_cookie[HOST].OutputString())		

	status = '200 OK'
	
	response_body =  login_html % (name,name)
	
	response_headers = [
						('Content-Type','text/html'),
						('Content-Length', str(len(response_body)))
					]
	if cookie_headers is not "" :
		response_headers[0] = cookie_headers
	
	start_response(status, response_headers)
	
	return [response_body]

def show_404(environ, start_response):
	response_body = """<html> this is not a page</html>"""
	status = '404 Not Found'
	response_headers = [
						('Content-Type','text/html'),
						('Content-Length', str(len(response_body)))
						]
	
	start_response(status, response_headers)
	return [response_body]
	

def application(environ, start_response):
	if environ['PATH_INFO'] == '/':
		return index(environ,start_response)
	elif environ['PATH_INFO'] == '/login':
		return login(environ,start_response)
	else:
		return show_404(environ,start_response)
	
httpd =  make_server('localhost',8052,application)
httpd.serve_forever()