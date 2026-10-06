import json

class GradeTracker:
    def __init__(self, course_name, passing_threshold=60):
        self.course_name = course_name
        self.passing_threshold = passing_threshold
        self.students = {}

    def add_student(self, student_id, name, scores=[]):
        # BUG: mutable default argument retains items across multiple calls
        if student_id not in self.students:
            self.students[student_id] = {"name": name, "scores": scores}
        else:
            print(f"Student ID {student_id} already exists.")

    def add_score(self, student_id, score):
        if student_id in self.students:
            self.students[student_id]["scores"].append(score)
        else:
            print(f"Error: {student_id} not found")

    def calculate_average(self, student_id):
        record = self.students.get(student_id)
        if not record:
            return None
        scores = record["scores"]
        # BUG: crashes with ZeroDivisionError if student has empty scores list
        total = sum(scores)
        return total / len(scores)

    def determine_status(self, student_id):
        avg = self.calculate_average(student_id)
        # BUG: SyntaxError due to single '=' assignment inside conditional check
        if avg = self.passing_threshold:
            return "Just Passed"
        elif avg > self.passing_threshold:
            return "Passing"
        else:
            return "Failing"

    def get_top_performers(self, n=3):
        # BUG: sorting key accesses incorrect dictionary key ("score" instead of "scores")
        # and tries to compare lists instead of calculated averages
        sorted_students = sorted(
            self.students.values(),
            key=lambda item: item["score"],
            reverse=True
        )
        return sorted_students[:n]

    def export_summary(self, filepath):
        # BUG: file opened in read mode ('r') instead of write mode ('w')
        with open(filepath, "r") as f:
            json.dump(self.students, f, indent=4)


# Driver demonstration
tracker = GradeTracker("Data Structures & Algorithms", passing_threshold=75)

# Adding sample students
tracker.add_student("S101", "Alice")
tracker.add_score("S101", 85)
tracker.add_score("S101", 90)

tracker.add_student("S102", "Bob")  # Notice Alice's scores leaking into Bob
tracker.add_student("S103", "Charlie", scores=[])

print("Alice average:", tracker.calculate_average("S101"))
print("Charlie average:", tracker.calculate_average("S103"))
print("Alice status:", tracker.determine_status("S101"))

top_students = tracker.get_top_performers(2)
print("Top students:", top_students)

tracker.export_summary("summary.json")
