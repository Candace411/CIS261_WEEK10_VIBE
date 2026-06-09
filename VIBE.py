#Candace Williams
#CIS261
#VIBE Coding


"""Student Records and Grade Calculator"""

import sys
import termios
import tty
from pathlib import Path
from typing import Dict, List


class Student:
    """Stores a student's name, ID, test scores, average, and grade."""

    def __init__(self, name: str, student_id: str, scores: List[float] | None = None) -> None:
        self.name = name
        self.id = student_id
        self.student_id = student_id
        self.test_scores = list(scores) if scores is not None else [0.0, 0.0, 0.0]
        self.scores = self.test_scores
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def set_scores(self, test1: float, test2: float, test3: float) -> None:
        for score in (test1, test2, test3):
            if not 0 <= score <= 100:
                raise ValueError("Each score must be between 0 and 100.")
        self.test_scores = [test1, test2, test3]
        self.scores = self.test_scores
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self) -> float:
        return sum(self.test_scores) / len(self.test_scores)

    def calculate_grade(self) -> str:
        avg = self.calculate_average()
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"


def load_students(path: str = "student_grades.txt") -> Dict[str, Student]:
    """Load student records from a text file."""
    students: Dict[str, Student] = {}
    file_path = Path(path)

    if not file_path.exists():
        return students

    try:
        with file_path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                delimiter = "|" if "|" in line else ","
                parts = [part.strip() for part in line.split(delimiter)]

                if delimiter == "|":
                    if len(parts) != 7:
                        print(f"Skipping invalid record on line {line_number}.")
                        continue
                    name, student_id, test1, test2, test3, average, grade = parts
                    record = Student(name, student_id, [float(test1), float(test2), float(test3)])
                    record.average = float(average)
                    record.grade = grade
                else:
                    if len(parts) != 5:
                        print(f"Skipping invalid record on line {line_number}.")
                        continue
                    name, student_id, test1, test2, test3 = parts
                    record = Student(name, student_id, [float(test1), float(test2), float(test3)])

                students[student_id] = record
    except OSError as error:
        print(f"Error loading records: {error}")
    except ValueError:
        print("Error loading records: file contains invalid score data.")

    return students


def save_students(students: Dict[str, Student], path: str = "student_grades.txt") -> None:
    """Save all student records to a text file."""
    file_path = Path(path)
    try:
        with file_path.open("w", encoding="utf-8") as handle:
            for student in students.values():
                handle.write(
                    f"{student.name}|{student.student_id}|{student.scores[0]:.2f}|"
                    f"{student.scores[1]:.2f}|{student.scores[2]:.2f}|"
                    f"{student.average:.2f}|{student.grade}\n"
                )
    except OSError as error:
        print(f"Error saving records: {error}")


def display_all_students(students: Dict[str, Student]) -> None:
    """Display all student records in a formatted table."""
    if not students:
        print("No student records yet.")
        return

    headers = ["Name", "ID", "Test 1", "Test 2", "Test 3", "Average", "Grade"]
    rows = []
    for student in students.values():
        avg = student.average
        rows.append([
            student.name,
            student.student_id,
            f"{student.scores[0]:.2f}",
            f"{student.scores[1]:.2f}",
            f"{student.scores[2]:.2f}",
            f"{avg:.2f}",
            student.grade,
        ])

    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def format_row(values: List[str]) -> str:
        return " | ".join(value.ljust(widths[index]) for index, value in enumerate(values))

    print("\nStudent Records")
    print("-" * (sum(widths) + 3 * (len(headers) - 1)))
    print(format_row(headers))
    print("-" * (sum(widths) + 3 * (len(headers) - 1)))
    for row in rows:
        print(format_row(row))


def display_class_statistics(students: Dict[str, Student]) -> None:
    """Display highest, lowest, and class averages."""
    if not students:
        print("No student records yet.")
        return

    try:
        averages = [student.average for student in students.values()]
        if not averages:
            print("No student records yet.")
            return
        highest = max(averages)
        lowest = min(averages)
        class_average = sum(averages) / len(averages)

        print("\nClass Statistics")
        print("----------------")
        print(f"Highest average: {highest:.2f}")
        print(f"Lowest average:  {lowest:.2f}")
        print(f"Class average:   {class_average:.2f}")
    except Exception as error:
        print(f"Error displaying statistics: {error}")


def search_student(students: Dict[str, Student], query: str) -> None:
    """Search for a student by name, case-insensitively."""
    search_term = query.lower()
    matches = [student for student in students.values() if search_term in student.name.lower()]

    if not matches:
        print("No matching students found.")
        return

    print("\nMatching Students")
    print("------------------")
    for student in matches:
        print(f"{student.name} (ID: {student.student_id}) | Average: {student.average:.2f} | Grade: {student.grade}")


def get_menu_choice(prompt: str) -> str:
    """Read a single menu key, with ESC supported."""
    file_descriptor = None
    original_settings = None
    try:
        file_descriptor = sys.stdin.fileno()
        original_settings = termios.tcgetattr(file_descriptor)
        tty.setcbreak(file_descriptor)
        print(prompt, end="", flush=True)
        key = sys.stdin.read(1)
        return key
    except (termios.error, OSError, AttributeError):
        return input(prompt).strip()
    finally:
        try:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, original_settings)
        except Exception:
            pass


def display_menu() -> str:
    """Display menu options and get user choice."""
    print("\n1. Add Student")
    print("2. View Student record")
    print("3. Display all students")
    print("4. Class Statistics")
    print("5. Search student by name")
    print("6. Save records")
    print("7. Exit")
    return get_menu_choice("Choose an option: ")


def main() -> None:
    students = load_students()

    print("Student Record Manager")
    print("======================")
    print("Records loaded from student_grades.txt (if available).")

    while True:
        choice = display_menu()

        if choice == "":
            continue

        if choice == "1":
            name = input("Enter student name: ").strip()
            student_id = input("Enter student ID: ").strip()
            if not name or not student_id:
                print("Error: Name and student ID cannot be empty.")
                continue
            if student_id in students:
                print(f"Error: Student ID '{student_id}' already exists.")
                continue

            try:
                test1 = float(input("Enter Test 1 score (0-100): ").strip())
                test2 = float(input("Enter Test 2 score (0-100): ").strip())
                test3 = float(input("Enter Test 3 score (0-100): ").strip())
                record = Student(name, student_id)
                record.set_scores(test1, test2, test3)
                students[student_id] = record
                print(f"✓ Successfully added {name} (ID: {student_id}).")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "2":
            student_id = input("Enter student ID to view: ").strip()
            if student_id not in students:
                print(f"Error: Student ID '{student_id}' not found.")
                continue

            student = students[student_id]
            avg = student.average
            print("\nStudent Record")
            print("---------------")
            print(f"Name: {student.name}")
            print(f"Student ID: {student.student_id}")
            print(f"Test 1: {student.scores[0]:.2f}")
            print(f"Test 2: {student.scores[1]:.2f}")
            print(f"Test 3: {student.scores[2]:.2f}")
            print(f"Average: {avg:.2f}")
            print(f"Grade: {student.grade}")

        elif choice == "3":
            display_all_students(students)

        elif choice == "4":
            display_class_statistics(students)

        elif choice == "5":
            query = input("Enter student name to search: ").strip()
            if not query:
                print("Error: Search term cannot be empty.")
                continue
            search_student(students, query)

        elif choice == "6":
            try:
                save_students(students)
                print("✓ Records saved to student_grades.txt.")
            except Exception as error:
                print(f"Error saving records: {error}")

        elif choice == "7":
            try:
                save_students(students)
                print("✓ Records saved. Goodbye!")
            except Exception as error:
                print(f"Error saving records: {error}")
            break

        else:
            print("Error: Invalid option. Please enter a valid menu choice.")


if __name__ == "__main__":
    main()

