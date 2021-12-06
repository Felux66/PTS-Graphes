
class Group:

    def __init__(self, students=[]):
        self.students = students

    def add_students(self, students):
        if isinstance(int, students):
            self.students.append(students)
        
        elif type(students) in (list, set, tuple) and all(type(s) == int for s in students): 
                self.students += students

        else:
            print("Error, could not add students")
        
class Course:

    def __init__(self, duration, group):
        self.duration = duration
        self.group = group