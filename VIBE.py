"""Student Records and Grade Calculator"""

from typing import Dict, List


class StudentRecord:
    """Stores a student's name, ID, and three test scores."""

    def __init__(self, name: str, student_id: str, scores: List[float] | None = None) -> None:
        self.name = name
        self.student_id = student_id
        self.scores = list(scores) if scores is not None else [0.0, 0.0, 0.0]

    def set_scores(self, test1: float, test2: float, test3: float) -> None:
        for score in (test1, test2, test3):
            if not 0 <= score <= 100:
                raise ValueError("Each score must be between 0 and 100.")
        self.scores = [test1, test2, test3]

    def average(self) -> float:
        return sum(self.scores) / len(self.scores)

    def letter_grade(self) -> str:
        avg = self.average()
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"


def main() -> None:
    students: Dict[str, StudentRecord] = {}

    print("Student Record Manager")
    print("======================")

    while True:
        print("\n1. Add student record")
        print("2. Enter/update three test scores")
        print("3. View all records")
        print("4. View one student record")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter student name: ").strip()
            student_id = input("Enter student ID: ").strip()
            if not name or not student_id:
                print("Name and student ID cannot be empty.")
                continue
            if student_id in {student.student_id for student in students.values()}:
                print("That student ID already exists.")
                continue

            try:
                test1 = float(input("Enter Test 1 score (0-100): ").strip())
                test2 = float(input("Enter Test 2 score (0-100): ").strip())
                test3 = float(input("Enter Test 3 score (0-100): ").strip())
                record = StudentRecord(name, student_id)
                record.set_scores(test1, test2, test3)
                students[student_id] = record
                print(f"Added {name} with ID {student_id}.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "2":
            student_id = input("Enter student ID: ").strip()
            if student_id not in students:
                print("Student not found. Add the student first.")
                continue

            try:
                test1 = float(input("Enter Test 1 score (0-100): ").strip())
                test2 = float(input("Enter Test 2 score (0-100): ").strip())
                test3 = float(input("Enter Test 3 score (0-100): ").strip())
                students[student_id].set_scores(test1, test2, test3)
                print(f"Updated scores for {students[student_id].name}.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "3":
            if not students:
                print("No student records yet.")
                continue

            print("\nStudent Records")
            print("----------------")
            for student in students.values():
                avg = student.average()
                print(
                    f"{student.name} (ID: {student.student_id}) | "
                    f"Test 1: {student.scores[0]:.1f}, Test 2: {student.scores[1]:.1f}, "
                    f"Test 3: {student.scores[2]:.1f} | Average: {avg:.1f} | Grade: {student.letter_grade()}"
                )

        elif choice == "4":
            student_id = input("Enter student ID: ").strip()
            if student_id not in students:
                print("Student not found.")
                continue

            student = students[student_id]
            avg = student.average()
            print("\nStudent Record")
            print("---------------")
            print(f"Name: {student.name}")
            print(f"Student ID: {student.student_id}")
            print(f"Test 1: {student.scores[0]:.1f}")
            print(f"Test 2: {student.scores[1]:.1f}")
            print(f"Test 3: {student.scores[2]:.1f}")
            print(f"Average: {avg:.1f}")
            print(f"Grade: {student.letter_grade()}")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Please enter a valid option.")


if __name__ == "__main__":
    main()
