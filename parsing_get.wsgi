from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
from Cookie import SimpleCookie
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import socket
import os 

curr_path = os.getcwd()
main_path =  os.path.join(curr_path, 'main.html')

HOST = socket.gethostname()

layout_html = """<html><a href='/logout'> Logout <br/><br/></a> </html>"""

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
			<a href='/env_det'> Click </a> here to list environment details
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

def display_env(environ,start_response):
	env_list = ['%s : %s' % (key, value) for key, value in sorted(environ.items())]
	
	response_body =  '\n'.join(env_list) 
	
	status = '200 OK'
	
	response_headers = [
						('Content-Type','text/plain'),
						('Content-Length', str(len(response_body)))
						]
						
	start_response(status, response_headers)
	
	return [response_body]


def index(environ, start_response):
	
	if 'HTTP_COOKIE' in environ:
		get_cookie = SimpleCookie(environ['HTTP_COOKIE'])
		if HOST in get_cookie:
			return login(environ, start_response)
		
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
	
	client = MongoClient('localhost',27017)
	db = client.chatbox
	coll = db.usr_session

	if 'HTTP_COOKIE' in environ:
		get_cookie = SimpleCookie(environ['HTTP_COOKIE'])
		if HOST not in get_cookie and name != '':
			print "Host not in HTTP. creating new cookie"
			insert_stmt = {'host' : HOST,'name' : name , 'expiry_date' : datetime.now() + timedelta(hours=2)}
			session_id = coll.insert(insert_stmt)
			new_cookie = SimpleCookie()
			new_cookie[HOST] = session_id
			cookie_headers = ('Set-Cookie',new_cookie[HOST].OutputString())
		elif HOST in get_cookie:
			print "Host in HTTP. getting new cookie"
			session_id = get_cookie[HOST].value
			print '--------' + str(session_id)
			if session_id != '':
				query_stmt = {'_id' : ObjectId(session_id)}
				result = coll.find(query_stmt)
				for doc in result:
					name = doc['name']
					print 'name = ' + name
				cookie_headers = ('Set-Cookie',get_cookie[HOST].OutputString())
			else:
				return index(environ,start_response)
		else:
			return index(environ,start_response)
	else:
		print "2-Host not in HTTP. creating new cookie"
		coll = db.usr_session
		insert_stmt = {'name' : name , 'expiry_date' : datetime.now() + timedelta(hours=2)}
		session_id = coll.insert(insert_stmt)
		new_cookie = SimpleCookie()
		new_cookie[HOST] = session_id
		cookie_headers = ('Set-Cookie',new_cookie[HOST].OutputString())
		
					
	#name =  get_cookie[HOST]['comment']['name']
	"""elif name != '':
		new_cookie = SimpleCookie()
		new_cookie[HOST] = HOST
		new_cookie[HOST]['comment']	= {'name' : name}
		cookie_headers = ('Set-Cookie',new_cookie[HOST].OutputString())		
	else:
		environ['PATH_INFO'] = '/'
		return index(environ, start_response)"""
	
	status = '200 OK'
	
	print "+++++++++++ %s " % name
	
	response_body =  layout_html + login_html % (str(name),str(name))
	
	print response_body
	
	response_headers = [
						('Content-Type','text/html'),
						('Content-Length', str(len(response_body)))
					]
					
	
		
	if cookie_headers is not "" :
		response_headers.reverse()
		response_headers.append(cookie_headers)
		response_headers.reverse()
	print response_headers
	
	start_response(status, response_headers)
	
	return [response_body]

def logout(environ,start_response):
	#environ.pop('HTTP_COOKIE')
	get_cookie = SimpleCookie(environ['HTTP_COOKIE'])
	get_cookie.clear()
	print get_cookie
	return login(environ,start_response)

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
	elif environ['PATH_INFO'] == '/env_det':
		return display_env(environ,start_response)
	elif environ['PATH_INFO'] == '/logout':
		return logout(environ,start_response)
	else:
		return show_404(environ,start_response)
	
httpd =  make_server('localhost',8052,application)
httpd.serve_forever()