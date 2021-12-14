
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
        
class Course:

    def __init__(self, duration, amount, group):
        self.duration = duration
        self.amount = amount
        self.group = group

class Plan:

    def __init__(self, day, start, duration, group):
        self.day = day
        self.start = start
        self.duration = duration
        self.end = start+duration
        self.group = group

def generate_schedule_graph():
    from graph import Vertex, VerticesList, Graph, EdgesSet

    g1 = Group([1,2,3])
    g2 = Group([4,5,6])
    g3 = Group([1,5,7])
    g4 = Group([8,9,10])
    g5 = Group([11,12,13])

    c1 = Course(3.0, 4, g1)
    c2 = Course(1.5, 3, g2)
    c3 = Course(3.0, 3, g4)
    c4 = Course(2.0, 3, g2)
    c5 = Course(1.0, 2, g5)
    c6 = Course(3.0, 4, g4)
    c7 = Course(1.5, 2, g1)
    c8 = Course(3.0, 3, g3)
    c9 = Course(2.0, 3, g3)

    Courses = [c1,c2,c3,c4,c5,c6,c7,c8,c9]
    
    vertices = VerticesList()
    for i,c in enumerate(Courses):
        for j in range(c.amount):
            vertices.add(Vertex(str(i+1)+"_"+str(j+1), c, 'c'+str(i+1)+'_'+str(j+1)))
    lV = list(vertices)

    edges = EdgesSet()
    for i,v1 in enumerate(lV):
        for j,v2 in enumerate(lV[i+1:]):
            if any(s in v2.value.group.students for s in v1.value.group.students):
                edges.add((v1, v2))
    
    graph = Graph(vertices, edges)

    return graph

def main_schedule():
    from ColoringAlgos import ColoringAlgos
    from consts import COLORS_ORDER  

    g = generate_schedule_graph()
    ColoringAlgos.sat(g)

    minH = 8
    maxH = 21

    pauseDuration = 1
    pauseTime = [11.5, 13.5]

    interPlan = 0.25

    for c in COLORS_ORDER:
        cs = [course for course in g.vertices if course.color == c]
        if len(cs) == 0: break
        print(cs)

