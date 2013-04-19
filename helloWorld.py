from flask import Flask
from flask import request
from flask import render_template
import ListOfProcs

app = Flask(__name__)


def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')#returns a function that needs to be called
	if func is None:
		raise RuntimeError('Not running ')
	#print func()
	func()


@app.route('/')
def initial_load():
    return render_template('index.html')

@app.route('/index.html')
def documentation():
  	return render_template('index.html')

@app.route('/new.html')
def add_new():
	return render_template('new.html')

@app.route('/shutdown')
def shutdown():
	shutdown_server()
	return 'Server shutting down...'

@app.route('/getFileNames')
def getFileNames():
  return ListOfProcs.main('config.txt')
  
if __name__ == '__main__':
    app.run()