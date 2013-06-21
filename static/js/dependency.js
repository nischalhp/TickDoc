(function(){

	$.ajax({
		type: "GET",
		url: "/getFileNames"
	}).done(function(o){
		var json = JSON.parse(o);
		$.each(json.data,function(key,value){
    	//console.log(value.id,value.name);
    	val = value.name.replace('SENTINEL.','');
    	$("#Procedures").append("<li id="+value.id+"><a href=\"#\" onclick=\"activate(this)\">"+val+"</a></li>")
    });
	});
}());


var previous;
function activate(obj){
	if(typeof(previous)!='undefined'){	
		var parent = previous.parentNode;
		parent.className = '';
	}
	var parentNow = obj.parentNode;
	parentNow.className = 'active';
	previous = obj;	
	updateTree("/getDependency/"+parentNow.getAttribute('id'));
}

