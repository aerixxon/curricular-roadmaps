// console.log("Hello World!")

var http = require("http");

http.createServer(function (request, response) {

   // Send the HTTP header 
   // HTTP Status: 200 : OK
   // Content Type: text/plain
   response.writeHead(200, {'Content-Type': 'text/plain'});
   
   // Send the response body as "Hello World"
   response.end('Hello World\n');
}).listen(8081);

// Console will print the message
console.log('Server running at http://127.0.0.1:8081/');

// figure out how ot import JSON

var TERMS = [20088, 20094, 20098, 20104, 20108, 20114, 20118, 20124,
20128, 20134, 20138, 20144, 20148, 20154, 20158, 20164]

var MAJORS = ["6-P3", "6-P2", "6-P1", "6-P7", "6-7", "6-3A", "6-2", "6-3", "6-1"]

var joint_map = {
   '1.203': '6.281',
   '2.038': '6.055',
   '2.096': '6.336',
   '2.097': '6.339',
   '2.110': '6.050',
   '2.372': '6.777',
   '2.374': '6.717',
   '2.391': '6.781',
   '2.791': '6.021',
   '2.792': '6.022',
   '2.793': '6.023',
   '2.794': '6.521',
   '2.795': '6.561',
   '2.796': '6.522',
   '2.797': '6.024',
   '2.798': '6.524',
   '2.830': '6.780',
   '3.433': '6.720',
   '3.053': '6.024',
   '3.155': '6.152',
   '3.971': '6.524',
   '7.33': '6.049',
   '8.277': '6.608',
   '8.371': '6.443',
   '8.431': '6.634',
   '8.351': '6.946',
   '8.613': '6.651',
   '8.614': '6.652',
   '9.66': '6.804',
   '9.611': '6.863',
   '10.53': '6.524',
   '10.539': '6.561',
   '12.620': '6.946',
   '14.15': '6.207',
   '15.032': '6.695',
   '15.070': '6.265',
   '15.072': '6.264',
   '15.073': '6.281',
   '15.081': '6.251',
   '15.082': '6.855',
   '15.083': '6.859',
   '15.084': '6.252',
   '15.085': '6.436',
   '15.093': '6.255',
   '15.377': '6.932',
   '16.37': '6.263',
   '16.76': '6.281',
   '16.338': '6.241',
   '16.391': '6.434',
   '16.405': '6.141',
   '16.406': '6.142',
   '16.412': '6.834',
   '16.456': '6.555',
   '16.910': '6.336',
   '16.920': '6.339',
   '18.062': '6.042',
   '18.335': '6.337',
   '18.336': '6.335',
   '18.337': '6.338',
   '18.400': '6.045',
   '18.404': '6.840',
   '18.405': '6.841',
   '18.410': '6.046',
   '18.415': '6.854',
   '18.416': '6.856',
   '18.425': '6.875',
   '18.426': '6.876',
   '18.436': '6.443',
   '18.437': '6.852',
   '20.305': '6.580',
   '20.310': '6.024',
   '20.330': '6.023',
   '20.345': '6.123',
   '20.370': '6.021',
   '20.371': '6.022',
   '20.410': '6.524',
   '20.430': '6.561',
   '20.470': '6.521',
   '20.471': '6.522',
   '20.482': '6.581',
   '22.071': '6.071',
   '22.611': '6.651',
   '22.612': '6.652',
   '24.966': '6.542',
   '24.968': '6.541',
   'CMS.611': '6.073',
   'EC.110': '6.072',
   'EC.120': '6.070',
   'ESD.63': '6.780',
   'ESD.051': '6.902',
   'ESD.78': '6.855',
   'ESD.162': '6.695',
   'ESD.216': '6.281',
   'HST.457': '6.502',
   'HST.506': '6.874',
   'HST.507': '6.878',
   'HST.541': '6.470',
   'HST.542': '6.022',
   'HST.544': '6.561',
   'HST.557': '6.582',
   'HST.580': '6.556',
   'HST.582': '6.555',
   'HST.710': '6.541',
   'HST.712': '6.542',
   'HST.714': '6.551',
   'HST.716': '6.552',
   'HST.728': '6.345',
   'HST.949': '6.877',
   'HST.950': '6.872',
   'MAS.731': '6.868',
}

var clean_data_years_and_majors = function(unrefined, MAJORS, TERMS){
   var students = unrefined.splice()

   for (var s=0; s<unrefined.length; s++){
      var first_grade_term = 20202;
      var last_grade_term = 0;

      if (!(students[s][0] in MAJORS)){
         students.splice(s,1);
         continue;
      }
      if ("P" in students[s][0]){
         students[s][0] = students[s][0].replace("P", "");
      }
      if ("A" in students[s][0]){
         students[s][0] = students[s][0].replace("P", "");
      }
      var courses = students[s].slice(1);

      for (var c=0; c<courses.length; c++){
         if (courses[c][1]<first_grade_term && (courses[c][1]%10 in (4,8))){
            first_grade_term = courses[c][1];
         }
         if (courses[c][1]>last_grade_term && (courses[c][1]%10 in (4,8))){
            last_grade_term = courses[c][1];
         }
         if (courses[c][1]%10 == 6){
            courses[c][1] = 329;
         }
         if (courses[c][1]%10 == 2){
            courses[c][1] = 406;
         }
      }

      try{
         var beginning = TERMS.index(first_grade_term);
      } catch(err){
         students.splice(s,1);
         continue;
      }
      for (var c=0; c<courses.length; c++){
         for (var semester=0; semester<16; semester++){
            try{
               if (courses[c][1] == TERMS[beginning+semester]){
                  courses[c][1] = semester+1;
               }
            } catch(err){
               break;
            }
         }
      }
   }
   return students;
}

var filter_students_by_major = function(students, major){
	for (var s=0; s<students.length; s++) {
		if (students[s][0] != major) {
			students.splice(s,1);
		}
	}
	return students;
}

var course_popularity_dictionary = function(students){
   
}

var make_joints_just_course6 = function(dictionary, joint_map){

	
}