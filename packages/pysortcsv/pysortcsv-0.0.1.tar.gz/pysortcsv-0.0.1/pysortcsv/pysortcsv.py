import csv
import random

class Student:
    def __init__(self, data):
        self.data = data

class StudentList:
    def __init__(self, students=None):
        self.students = students if students is not None else []
    
    def read_from_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.students.append(Student(row))

    def write_to_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([student.data for student in self.students])

    def shuffle(self):
        random.shuffle(self.students)
    
    def sort_by_id(self):
        self.students.sort(key=lambda student: student.data[0])
    
    def sort_by_name(self):
        self.students.sort(key=lambda student: student.data[1])

    def sort_by_grade_level(self):
        self.students.sort(key=lambda student: student.data[4])

    def sort_by_major(self):
        self.students.sort(key=lambda student: student.data[5])



