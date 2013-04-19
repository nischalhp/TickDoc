(function(){

/*$.ajax({
  type: "GET",
  url: "/getFileNames"
 }).done(function( o ) {
    //console.log(o);
    $.each(o.data,function(key,value){
    	console.log(value);
    })

});*/


$.getJSON("/getFileNames",function(json){
	$.each(json.data,function(key,value){
    	//console.log(value);
    	value = value.replace('SENTINEL.','');
    	$("#Procedures").append("<li><a href=\"javascript:void(0)\" onclick=\"activate(this)\">"+value+"</a></li>")
    })	
})


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
	console.log(obj.innerHTML)
}

