import json
import operator
import copy

with open('subjects2.json') as json_data:
    students = json.load(json_data)
    json_data.close()

#loading in cleaned student set

#thought about group AUS or advanced classes into disciplines to limit nodes and demonstrate more general trends
#disciplines are taken from the PDF on the course 6 website (http://www.eecs.mit.edu/docs/ug/Checklist.pdf)
discipline_map = {'Applied Physics': ['6.061', ' 6.602', ' 6.S077', ' 6.621', ' 6.630', ' 6.631', ' 6.632', ' 6.634',
' 6.637', ' 6.638', ' 6.641', ' 6.642', ' 6.644', ' 6.645', ' 6.685', ' 6.690', ' 6.691', ' 6.695'], 
'Artificial Intelligence': ['6.036', ' 6.141', ' 6.189', ' 6.801', ' 6.802', ' 6.803', ' 6.804', ' 6.806', ' 6.S078',
'6.905', ' 6.345', ' 6.437', ' 6.438', ' 6.831', ' 6.832', ' 6.833', ' 6.834', ' 6.863', ' 6.864', ' 6.866', ' 6.867',
' 6.868', ' 6.872', ' 6.874', ' 6.881', ' 6.882', ' 6.883', ' 6.884', ' 6.945', ' 6.946', ' MAS.S63'],
'BioEECS': ['6.022', ' 6.023', ' 6.024', ' 6.025', ' 6.027', ' 6.047', ' 6.048', ' 6.049', ' 6.502', ' 6.503', ' 6.802',
' 6.345', ' 6.521', ' 6.522', ' 6.524', ' 6.525', ' 6.541', ' 6.542', ' 6.544', ' 6.545', ' 6.551', ' 6.552', ' 6.555',
' 6.556', ' 6.557', ' 6.561', ' 6.580', ' 6.581', ' 6.582', ' 6.589', ' 6.872', ' 6.874', ' 6.877', ' 6.878'],
'Circuits': ['6.301', ' 6.302', ' 6.331', ' 6.332', ' 6.333', ' 6.334', ' 6.374', ' 6.375', ' 6.376', ' 6.775', ' 6.776'],
'Communications': ['6.207', '16.36', ' 6.231', ' 6.255', ' 6.260', ' 6.261', ' 6.262', ' 6.263', ' 6.264', ' 6.265',
' 6.266', ' 6.267', ' 6.268', ' 6.434', ' 6.435', ' 6.436', ' 6.437', ' 6.438', ' 6.440', ' 6.441', ' 6.442', ' 6.443',
' 6.450', ' 6.451', ' 6.452', ' 6.453', ' 6.859'],
'Computer Systems': ['6.035', ' 6.172', ' 6.173', ' 6.805', ' 6.814', ' 6.816', ' 6.820', ' 6.821', ' 6.823', ' 6.824',
' 6.828', ' 6.829', ' 6.830', ' 6.836', ' 6.846', ' 6.857', ' 6.858', ' 6.885', ' 6.886', ' 6.887', ' 6.888'],
'Control': ['6.302', ' 6.231', ' 6.241', ' 6.242', ' 6.243', ' 6.245', ' 6.246', ' 6.247'], 'Graphics': ['6.801', ' 6.807',
' 6.811', ' 6.813', ' 6.815', ' 6.819', ' 6.837', ' 6.831', ' 6.835', ' 6.838', ' 6.839', ' 6.865', ' 6.869', ' 6.870',
' 6.894', ' 6.895', ' 6.896'], 'Materials and Nanotechnology': ['6.602', ' 6.701', ' 6.717', ' 6.719', ' 6.720', ' 6.728',
' 6.730', ' 6.731', ' 6.732', ' 6.735', ' 6.736', ' 6.763', ' 6.772', ' 6.774', ' 6.777', ' 6.780J', ' 6.781', ' 6.789'],
'Numerical Methods': ['6.248', ' 6.249', ' 6.251', ' 6.252', ' 6.253', ' 6.254', ' 6.255', ' 6.256', ' 6.336', ' 6.337',
' 6.338', ' 6.339', ' 6.581', ' 6.673'],
'Signals and Systems': ['6.341', ' 6.342', ' 6.344', ' 6.345', ' 6.347', ' 6.348', ' 6.437', ' 6.438', ' 6.456', ' 6.555',
' 6.556'], 'Theoretical Computer Science': ['6.045', ' 6.840', ' 6.841', ' 6.842', ' 6.845', ' 6.849', ' 6.850', ' 6.851',
' 6.852', ' 6.853', ' 6.854', ' 6.856', ' 6.875', ' 6.876', ' 6.889', ' 6.890', ' 6.891', ' 6.892', ' 6.893']}

disciplines = ['Applied Physics', 'Circuits', 'Control', 'Numerical Methods', 'Computer Systems', 'Signals and Systems',
'Communications', 'Artificial Intelligence', 'Theoretical Computer Science', 'Graphics', 'BioEECS', 'Materials and Nanotechnology']

#inverts the discpline map -> was potentially going to be useful
inv_map = {}
for k, v in discipline_map.items():
   for c in v:
      inv_map[c] = k


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
					dictionary[course[0].encode('ascii')] += 1
				else:
					dictionary[course[0].encode('ascii')] = 1
	return dictionary

# filters out classes if they are not in the specific prefix
# ie remove all non course 6 classes
# Input: dictionary: mapping course numbers to enrollment
#        prefix: str of desired prefix or course number
# Output: dictionary that courses of only a specific prefix
def filter_in_courses_given_prefix(dictionary, prefix):
	d = {}
	for item in dictionary:
		if item[0:len(prefix)] == prefix or item in disciplines:
			d[item] = dictionary[item]
	return d

students67 = filter_students_by_major(students, "6-7")

courses = course_popularity_dictionary(students67)
filtered = filter_in_courses_given_prefix(courses, "6")

# find the top 10 most popular classes
inorder = filtered.items()
inorder = sorted(inorder, key=lambda x: x[1])
inorder =  inorder[-10:]


nodes = []
for k in inorder:
   print k[0]
   nodes.append({"node": inorder.index(k),"name": k[0]})

#creates an empty map to count the number of students from any class
#to any other given class
forward_map = {}
for c in inorder:
   for d in inorder:
      if c[0]!=d[0]:
         forward_map[(c[0],d[0])] = 0


#remaps student semester labeling to make referencing easier
stud_semesters = []
# ["6-3", {"7.012":1, "8.01":1, "8.02":2}]
for s in students:
   entry = []
   entry.append(s[0])
   sem = {}
   for c in s[1:]:
      sem[c[0]] = c[1]
   entry.append(sem)
   stud_semesters.append(entry)

#counts the number of students who have taken one class
#in the semester immediately prior to another class
for s in stud_semesters:
   for k in inorder:
      if k[0] not in s[1]:
         continue
      for l in inorder:
         if l[0] not in s[1]:
            continue
         if s[1][k[0]] +1 == s[1][l[0]]:
            forward_map[(k[0],l[0])] +=1

#prunes the mapping to eliminate paths that are 0
#my code does not handle bidirectinoal mapping
#it is quite frequent for students to take classes
#"out of order", so I kept the path that was more popular
pruning = copy.deepcopy(forward_map)
for k in forward_map:
   a,b = k
   if forward_map[(b,a)] > forward_map[(a,b)]:
      del pruning[k]
   elif forward_map[k]==0:
      del pruning[(a,b)]

#creating final mapping for sankey diagram
final = {}
links = []

#just makes referencing easier for the for loop to make links
names = []
for n in nodes:
   names.append(n["name"])

for m in xrange(len(names)):
   for n in xrange(len(names)):
      try: 
         if pruning[(names[m],names[n])]:
            r = {"source":m, "target":n, "value": pruning[(names[m],names[n])]}
            links.append(r)
      except(KeyError):
         continue

final = {"nodes":nodes, "links": links}
# print final

with open('67.json', 'w') as outfile:
    json.dump(final, outfile)

