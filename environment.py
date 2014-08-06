from wsgiref.simple_server import make_server

def application(environ, callback_func):
	
	response_body =  ['%s : %s' % (key, value) for key, value in sorted(environ.items())]
	
	response_body = '\n'.join(response_body)
	
	status = '200 OK'
	
	response_headers = [ 
						('Content-Type' , 'text/plain'),
						('Content-Length' , str(len(response_body)))
					]
					
	callback_func(status,response_headers)
	
	return response_body

httpd = make_server('localhost',8051,application)

httpd.handle_request()	