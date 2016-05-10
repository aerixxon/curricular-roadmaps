import json
import operator

with open('subjects.json') as json_data:
    students_unrefined = json.load(json_data)
    json_data.close()

#only including students who began MIT in 2008 or later
TERMS = [20088, 20094, 20098, 20104, 20108, 20114, 20118, 20124,
20128, 20134, 20138, 20144, 20148, 20154, 20158, 20164]

#currently only including Undergrads (ie no Masters or Doctoral)
MAJORS = ["6-P3", "6-P2", "6-P1", "6-P7", "6-7", "6-3A", "6-2", "6-3", "6-1"]

joint_map = {
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

# Refines original data from JSON file
# Removes old majors and students who started before Fall 2008
# Reconfigures semester labelling to 1,2,3,... scale instead of calendar

# Input: unrefined: list of students w/ course number as first entry
#        and list pairs for each course he took
#        MAJORS: list of valid majors
#        TERMS: list of valid terms
# Output: list of valid students with refined semester numbering
# 406 --> IAP
# 329 --> Summer
def clean_data_years_and_majors(unrefined, MAJORS, TERMS):
	students = unrefined[:]

	for student in unrefined:
		first_grade_term = 20202
		last_grade_term = 0
		#first looped through to find the first and last semesters
		#made IAP and summer irrelevant now, but might consider
		#making them useful later

		#removing irrelevant majors
		if student[0] not in MAJORS:
			students.remove(student)
			continue
		if "P" in student[0]:
			student[0] = student[0].replace("P", "")
		if "A" in student[0]:
			student[0] = student[0].replace("A", "")

		for course in student[1:]:
			if course[0] in joint_map: course[0] = joint_map[course[0]]
			if course[1] < first_grade_term and course[1]%10 in (4,8): first_grade_term = course[1]
			if course[1] > last_grade_term and course[1]%10 in (4,8): last_grade_term = course[1]
			if course[1]%10 == 6: course[1] = 329
			if course[1]%10 == 2: course[1] = 406
		
		#remove students who did not begin after 20088
		try:
			beginning = TERMS.index(first_grade_term)
		except ValueError:
			students.remove(student)
			continue
		
		#think about a roadmap
		#TODO: create a set for each student and then the terms would correlate
		for course in student[1:]:
			for semester in xrange(16):
				try:
					#edge cases I dont handle..
					#taking a semester off
					#taking more than 8 semesters to graduate
					if course[1] == TERMS[beginning + semester]:
						course[1] = semester + 1
				#for current students because they haven't finished all semesters
				except IndexError:
					break
	return students

students = clean_data_years_and_majors(students_unrefined, MAJORS, TERMS)

# with open('subjects2.json', 'w') as outfile:
#     json.dump(students, outfile)

# filters students so that only students of a particular major are left
# Input: students: list of students
#        major: str of desired major
# Output: list of students
def filter_students_by_major(students, major):
   s = students[:]
   for student in students:
      if student[0] != major:
         s.remove(student)
   return s

# creates a dictionary mapping all courses to total enrollment
# Input: students: list of students
# Output: dictionary of course enrollment
def course_popularity_dictionary(students):
	dictionary = {}
	for student in students:
		for course in student[1:]:
			if course[1] < 15:
				if course[0] in dictionary:
					dictionary[course[0]] += 1
				else:
					dictionary[course[0]] = 1
	return dictionary


# filters jointly registered classes and makes them the course 6 version
# Input: dictionary: mapping course numbers to enrollment
#        joint_map: dictionary mapping non-course 6 number to course 6 #
# Output: dictionary of filtered courses
def make_joints_just_course6(dictionary, joint_map):
	d = dictionary.copy()
	for course in dictionary:
		if course in joint_map:
			# print course, "is a jointly listed course with", dictionary[course]
			if joint_map[course] in dictionary:
				d[joint_map[course]] += dictionary[course]
				# print d[joint_map[course]], "sohuld be the both the joint classes combined", joint_map[course]
				del d[course]
			else:
				d[joint_map[course]] = dictionary[course]
				# print d[joint_map[course]], "wasn't in original dictionary...", joint_map[course]
				del d[course]
	return d


# filters classes with a specific prefix/major and collects into 1 entry
# ie all course 14 classes merge
# Input: dictionary: mapping course numbers to enrollment
#        prefix: str of desired prefix or course number
# Output: dictionary of courses that includes condensed prefix
def filter_out_courses_given_prefix(dictionary, prefix):
	count = 0
	d = dictionary.copy()
	for item in dictionary:
		if item[0:len(prefix)] == prefix:
			count += dictionary[item]
			del d[item]
	d[prefix] = count
	return d


# filters out classes if they are not in the specific prefix
# ie remove all non course 6 classes
# Input: dictionary: mapping course numbers to enrollment
#        prefix: str of desired prefix or course number
# Output: dictionary that courses of only a specific prefix
def filter_in_courses_given_prefix(dictionary, prefix):
	d = {}
	for item in dictionary:
		if item[0:len(prefix)] == prefix:
			d[item] = dictionary[item]
	return d


#I can pass in a slective course dictionary or a subset of students
#ie filtering happens before this function is called
def course_by_semester_enrollment(dictionary, students):
	d = {}
	for student in students:
		for course in student[1:]:
			if course[0] not in dictionary:
				continue
			else:
				if (course[0], course[1]) in d:
					d[(course[0], course[1])] += 1
				else:
					d[(course[0], course[1])] = 1
	return d

#create dictionary --> semester #: list of top 5 courses that semester
# pass in a filtered dictionary so that I don't deal with that hear
# dict --> (course, semester int): int enrollment
def popular_courses_by_semester(dictionary):
   d = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 329:[], 406:[]}
   for key in dictionary:
      d[key[1]].append((key[0], dictionary[key]))

   for k in d:
      temp = sorted(d[k], key=operator.itemgetter(1))[-7:]
      temp.reverse()
      d[k] = temp

   return d

def check_previous(courses, previous, semester):
   count = 0
   for c in courses:
      if c[0] in previous and c[1]<= semester:
         count+=1
   if count == len(previous): return True
   else: return False

def filter_students_based_on_previous_courses(students, previous, semester = 406):
   s = students[:]
   for student in students:
      if not check_previous(student[1:], previous, semester):
         s.remove(student)
   return s

"there are 348 students who did not graduate in 8 semesters"

c = course_popularity_dictionary(students)
courses = make_joints_just_course6(c, joint_map)
print
print len(courses)
print

six1 = filter_students_by_major(students, "6-1")
six2 = filter_students_by_major(students, "6-2")
six3 = filter_students_by_major(students, "6-3")

six = filter_in_courses_given_prefix(courses, "6")
print len(six)
fourteen = filter_in_courses_given_prefix(courses, "14")
fifteen = filter_in_courses_given_prefix(courses, "15")

#creating course semester enrollment dictionaries
enrollmentAll = course_by_semester_enrollment(courses, students)
enrollmentAll61 = course_by_semester_enrollment(courses, six1)
enrollmentAll62 = course_by_semester_enrollment(courses, six2)
enrollmentAll63 = course_by_semester_enrollment(courses, six3)

popularAll = popular_courses_by_semester(enrollmentAll)
popularAll61 = popular_courses_by_semester(enrollmentAll61)
popularAll62 = popular_courses_by_semester(enrollmentAll62)
popularAll63 = popular_courses_by_semester(enrollmentAll63)


allie = filter_students_based_on_previous_courses(six3, ["6.004", "6.006"], 4)
alekhya = filter_students_based_on_previous_courses(six2, ["8.02", "18.02", "7.012", "6.01"], 3)
jenny = filter_students_based_on_previous_courses(six3, ["6.003", "6.172"])

popularAllie = popular_courses_by_semester(course_by_semester_enrollment(courses, allie))
popularAlekhya = popular_courses_by_semester(course_by_semester_enrollment(courses, alekhya))
popularJenny = popular_courses_by_semester(course_by_semester_enrollment(courses, jenny))

print "all courses, all students", len(students)
for k, v in popularAll.items():
	print (k, '-->', v)
print

print "all courses, 6-1", len(six1)
for k, v in popularAll61.items():
   print (k, '-->', v)
print

print "all courses, 6-2", len(six2)
for k, v in popularAll62.items():
   print (k, '-->', v)
print

print "all courses, 6-3", len(six3)
for k, v in popularAll63.items():
   print (k, '-->', v)
print

print "People similar to Allie", len(allie)
for k, v in popularAllie.items():
   print (k, '-->', v)
print

print "People similar to Alekhya", len(alekhya)
for k, v in popularAlekhya.items():
   print (k, '-->', v)
print

print "People similar to Jenny", len(jenny)
for k, v in popularJenny.items():
   print (k, '-->', v)
print
