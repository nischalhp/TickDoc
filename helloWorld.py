from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')#returns a function that needs to be called
	if func is None:
		raise RuntimeError('Not running ')
	#print func()
	func()


@app.route('/')
def hello_world():
	#return "hello"
    return render_template('BootStrap101.html')

@app.route('/new.html')
def add_new():
	return render_template('new.html')

@app.route('/shutdown')
def shutdown():
	shutdown_server()
	return 'Server shutting down...'



if __name__ == '__main__':
    app.run()