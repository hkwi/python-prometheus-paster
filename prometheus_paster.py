import functools
from prometheus_client import make_wsgi_app, Summary
from prometheus_client.context_managers import Timer

def factory(global_config, **local_conf):
	return make_wsgi_app()

def filter_factory(global_config, **local_conf):
	metric = local_conf.get("name", "wsgi_call")
	s = Summary(metric, "WSGI milliseconds", ["method", "status"])
	
	def middleware(application):
		@functools.wraps(application)
		def wsgiapp(environ, start_response):
			extra = { "method": environ["REQUEST_METHOD"] }
			
			@functools.wraps(start_response)
			def sr_proxy(status, resp_headers, exc_info=None):
				try:
					code, msg = status.split(None, 1)
				except ValueError:
					code, msg = status, ""
				
				extra["status"] = code
				return start_response(status, resp_headers, exc_info)
			
			cb = lambda v: s.labels(**extra).observe(v)
			with Timer(cb):
				return application(environ, sr_proxy)
		
		return wsgiapp
	
	return middleware
