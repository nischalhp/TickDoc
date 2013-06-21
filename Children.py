import ListOfProcs

class node:
  name = ""
  children = []

  def __init__(self):
   return

  def get_name(self,collection,id):
    cursor = collection.find({'key':id})
    path = ""
    if len(curson) > 0:
    	for document in cursor:
    		self.name = document['name']
    		path = document['path']

    children = get_children(collection,path)		


  def get_children(self,path):
  	results = ""
  	outputList = ListOfProcs.getDependency(path,1)
  	while outputList != None: 
  		for obj in outputList:
  			for obj
  	return results
