from flask import Flask
from flask import request
from flask import render_template
from flask.ext.pymongo import PyMongo
import ListOfProcs
import GetProcedure

app = Flask(__name__)

#connect to mongo db
mongo = PyMongo(app)
from pymongo import Connection
connection = Connection()
db = connection.documentation
collection = db.documents


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

@app.route('/dependency.html')
def add_new():
	return render_template('dependency.html')

@app.route('/shutdownAdmin')
def shutdown():
	shutdown_server()
	return 'Server shutting down...'
 


@app.route('/getFileNames')
def getFileNames():
  list_of_objects =  ListOfProcs.main('config.txt')
  collection.remove()
  counter = 0
  return_string = "{\"data\":["
  for object in list_of_objects:
  	  insert_string = {'key' :  counter , 'name' :  object.getName() , 'path' : object.getPath()  }
  	  #print insert_string
   	  id = collection.insert(insert_string)
   	  return_string = return_string + " { \"id\" : " + str(counter) + " , \"name\" : \"" + object.getName() + "\" } ," 
   	  counter = counter + 1
  return_string = return_string.rstrip(",") + " ]}"
  return return_string

@app.route('/getProcedure/<id>')
def getTomDoc(id):
 return_string = ""
 for document in collection.find({'key':int(id)}):
		return_string =  GetProcedure.show_tomdoc(document['path'])
 

 return return_string.replace("\n","<br/>")


@app.route('/getDependency/<fileId>')
def getDependencyTemp(fileId):
  output_path = ""
  output_name = ""
  dependency_objects = []
  output_json = ""
  for document in collection.find({'key':int(fileId)}):
    return_string =  GetProcedure.show_tomdoc(document['path'])
    output_path = document['path']
    output_name = document['name']
 
  dependency_objects = ListOfProcs.getDependency(output_path,1)
 
  output_json = "{ \"name\":\""+output_name+"\",\"children\":[ "
  
  for obj in dependency_objects:
    if len(dependency_objects) > 0 :
      for obj_inner in obj:
        output_json = output_json + "{ \"name\" : \""+obj_inner+"\"},"
    else :  
      output_json = output_json + "}"

  output_json = output_json.replace('SENTINEL.','')
  output_json = output_json.rstrip(',') + "] }"
  return str(output_json)




  
if __name__ == '__main__':
    app.run(host='0.0.0.0')