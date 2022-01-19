class Group:

    def __init__(self, students=[]):
        self.students = students

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

    def __init__(self, day, start, duration, group):
        self.day = day
        self.start = start
        self.duration = duration
        self.end = start+duration
        self.group = group

def generate_schedule_graph_from_subjects(subjects):
    from graph import Vertex, VerticesList, Graph, EdgesSet
    
    vertices = VerticesList()
    for i,c in enumerate(subjects):
        for j in range(c.amount):
            vertices.add(Vertex(str(i+1)+"_"+str(j+1), c, 'c'+str(i+1)+'_'+str(j+1)))
    lV = list(vertices)

    edges = EdgesSet()
    for i,v1 in enumerate(lV):
        for j,v2 in enumerate(lV[i+1:]):
            if any(s in v2.value.group.students for s in v1.value.group.students) or v2.value.prof == v1.value.prof:
                edges.add((v1, v2))
    
    graph = Graph(vertices, edges)

    return graph

def main_schedule():
    from ColoringAlgos import ColoringAlgos
    from consts import COLORS_ORDER  
    import data_schedule

    g = generate_schedule_graph_from_subjects(data_schedule.school[1])
    ColoringAlgos.sat(g)

    for c in COLORS_ORDER:
        cs = [course for course in g.vertices if course.color == c]
        if len(cs) == 0: break
        print(cs)

