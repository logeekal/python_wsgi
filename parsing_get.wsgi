from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import os 

curr_path = os.getcwd()
main_path =  os.path.join(curr_path, 'main.html')

html = """
<html>
<body>
	<form method="get" action="login.wsgi">
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

def application(environ, start_response):
	
	"""d = parse_qs(environ["QUERY_STRING"])
	
	age =  d.get('age', [''])[0]
	hobbies =  d.get('hobbies',[])
	
	age = escape(age)
	hobbies = [escape(hobby) for hobby in hobbies]"""
	
	response_body = html #% (age or 'Empty', ', '.join(hobbies) or 'No Hobbies')
	
	status = '200 OK'
	
	response_headers = [
						('Content-Type','text/html'),
						('Content-Length', str(len(response_body)))
						]
	start_response(status, response_headers)
	
	return [response_body]
	
httpd =  make_server('localhost',8052,application)
httpd.serve_forever()