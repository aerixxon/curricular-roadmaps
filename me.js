var me = function(){
	var students;
	var all;
	var user_input;

	// $.each()

	$(function() {
    var update = function() {
    	user_input = $('form').serializeArray();
    	// parameters = adjust_params(user_input);
        // $('#serializearray').text(        
        //     JSON.stringify(user_input));
    //  
    update();
    $('form').change(update);
}});
	function setup(){
		$.ajax('all.json', {
			dataType: "json",
			success: function(data){
				students = data;
				// $("#data").text(JSON.stringify(students))
			},
			error: function(){
				alert("oops!");
			}
		})
	}
	return {setup: setup}
}();

$(document).ready(function(){
	me.setup();
});
