from email.errors import MultipartInvariantViolationDefect
from ColoringAlgos import ColoringAlgos


class Group:

    def __init__(self, students=[],name=None):
        self.students = students
        self.name = name

    def add_students(self, students):
        if isinstance(int, students):
            self.students.append(students)
        
        elif type(students) in (list, set, tuple) and all(type(s) == int for s in students): 
                self.students += list(students)

        else:
            print("Error, could not add students")
        
class Subject:

    def __init__(self, duration, amount, group, prof=None):
        self.duration = duration
        self.amount = amount
        self.group = group
        self.prof = prof

class Course:

    def __init__(self, day, start, duration, group, prof):
        self.day = day
        self.start = start
        self.duration = duration
        self.end = None
        self.group = group
        self.prof = prof

class Diary:
    def __init__(self,school) :
        self.all_diaries = dict.fromkeys(school[0])
        for k in list(self.all_diaries.keys()) :
            self.all_diaries[k] = [["Pause" if x in [4,9,10,15] else None for x in range(20)]for x in range(5)]

    def generate_diary (self,school):
        graph_sche = generate_schedule_graph_from_subjects(school[1])
        ColoringAlgos.sat(graph_sche)
        colors_hours={}
        for i in graph_sche.vertices:
            if i.color in colors_hours:
                i.value.day = colors_hours[i.color][0]
                i.value.start = colors_hours[i.color][1]
                i.value.end = i.value.start+i.value.duration
                self.all_diaries[i.value.group][colors_hours[i.color][0]][colors_hours[i.color][1]] = i.name
                self.all_diaries[i.value.group][colors_hours[i.color][0]][colors_hours[i.color][1]+1] = i.name
                if (i.value.duration==2):
                    self.all_diaries[i.value.group][colors_hours[i.color][0]][colors_hours[i.color][1]+2] = i.name
                    self.all_diaries[i.value.group][colors_hours[i.color][0]][colors_hours[i.color][1]+3] = i.name
            else:
                place = False
                for l in range(5):
                    for j in [0,5,11,16]:
                        if (l,j) not in colors_hours.values() and j not in [4,9,10,15] and not place:
                            colors_hours[i.color]=(l,j)
                            i.value.day = l
                            i.value.start = j
                            i.value.end = i.value.start+i.value.duration
                            self.all_diaries[i.value.group][l][j] = i.name
                            self.all_diaries[i.value.group][l][j+1] = i.name
                            if (i.value.duration==2):
                                self.all_diaries[i.value.group][l][j+2] = i.name
                                self.all_diaries[i.value.group][l][j+3] = i.name
                            place = True

'''
Constraints
1) Start of diary at 8h and end at 18h
2) Luch time between 12h30 and 13h30
3) Break between 10h-10h30 and 15h30-16h
4) Maximum two courses of the same subject a day
5) Class can't have two courses at the same
6) Same for the teacher
7) No courses during the weekend
8) Remove subjects that have ammount = 0
Diary : list of (18,5)
'''



def generate_schedule_graph_from_subjects(subjects):
    from graph import Vertex, VerticesList, Graph, EdgesSet
    
    vertices = VerticesList()
    for i,c in enumerate(subjects):
        for j in range(c.amount):
            vertices.add(Vertex(str(i+1)+"_"+str(j+1), Course(None,None,c.duration,c.group,c.prof), 'c'+str(i+1)+'_'+str(j+1)))
    lV = list(vertices)
    print(lV)

    edges = EdgesSet()
    for i,v1 in enumerate(lV):
        for j,v2 in enumerate(lV[i+1:]):
            if any(s in v2.value.group.students for s in v1.value.group.students) or v2.value.prof == v1.value.prof:
                edges.add((v1, v2))
    
    graph = Graph(vertices, edges)

    return graph



def generate_schedule (school):
    pass

def main_schedule():
    from consts import COLORS_ORDER  
    import usages.schedule.data_schedule as dsh


    d = Diary(dsh.school)
    d.generate_diary(dsh.school)
    for k in list(d.all_diaries.keys()) :
        print(d.all_diaries[k])
    