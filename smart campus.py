import json
import os
from datetime import datetime

FILE = "campus_data.json"

# Initialize database
def initialize():
    if not os.path.exists(FILE):
        data = {
            "students": [],
            "books": [],
            "fees": []
        }
        save_data(data)

def load_data():
    with open(FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(FILE, "w") as file:
        json.dump(data, file, indent=4)

# Student Registration
def register_student():
    data = load_data()

    print("\n--- Student Registration ---")

    roll = input("Enter Roll Number: ")

    for student in data["students"]:
        if student["roll"] == roll:
            print("Student already exists!")
            return

    name = input("Enter Name: ")
    department = input("Enter Department: ")
    year = input("Enter Year: ")
    email = input("Enter Email: ")

    student = {
        "roll": roll,
        "name": name,
        "department": department,
        "year": year,
        "email": email,
        "attendance": [],
        "marks": []
    }

    data["students"].append(student)
    save_data(data)

    print("Student registered successfully!")

# Display Students
def display_students():
    data = load_data()

    print("\n--- Student Details ---")

    if not data["students"]:
        print("No student records found.")
        return

    for s in data["students"]:
        print("-" * 40)
        print("Roll Number:", s["roll"])
        print("Name:", s["name"])
        print("Department:", s["department"])
        print("Year:", s["year"])
        print("Email:", s["email"])

# Search Student
def search_student():
    data = load_data()

    roll = input("Enter Roll Number: ")

    for s in data["students"]:
        if s["roll"] == roll:
            print("\nStudent Found!")
            print("Name:", s["name"])
            print("Department:", s["department"])
            print("Year:", s["year"])
            print("Email:", s["email"])
            return

    print("Student not found!")

# Delete Student
def delete_student():
    data = load_data()

    roll = input("Enter Roll Number: ")

    for s in data["students"]:
        if s["roll"] == roll:
            data["students"].remove(s)
            save_data(data)
            print("Student deleted successfully!")
            return

    print("Student not found!")

# Attendance Management
def mark_attendance():
    data = load_data()

    roll = input("Enter Student Roll Number: ")

    for s in data["students"]:
        if s["roll"] == roll:

            status = input("Present or Absent (P/A): ").upper()

            if status not in ["P", "A"]:
                print("Invalid attendance status!")
                return

            record = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": status
            }

            s["attendance"].append(record)

            save_data(data)

            print("Attendance marked!")
            return

    print("Student not found!")

# Attendance Report
def attendance_report():
    data = load_data()

    roll = input("Enter Roll Number: ")

    for s in data["students"]:
        if s["roll"] == roll:

            total = len(s["attendance"])
            present = sum(
                1 for a in s["attendance"]
                if a["status"] == "P"
            )

            percentage = (
                (present / total) * 100 if total > 0 else 0
            )

            print("\nAttendance Report")
            print("Student:", s["name"])
            print("Total Classes:", total)
            print("Present:", present)
            print("Absent:", total - present)
            print("Percentage:", round(percentage, 2), "%")
            return

    print("Student not found!")

# Marks Management
def add_marks():
    data = load_data()

    roll = input("Enter Roll Number: ")

    for s in data["students"]:
        if s["roll"] == roll:

            subject = input("Enter Subject: ")

            try:
                marks = float(input("Enter Marks (0-100): "))
            except ValueError:
                print("Enter a valid number!")
                return

            if not 0 <= marks <= 100:
                print("Marks must be between 0 and 100!")
                return

            s["marks"].append({
                "subject": subject,
                "marks": marks
            })

            save_data(data)

            print("Marks added successfully!")
            return

    print("Student not found!")

# Grade Calculation
def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "Fail"

# Marks Report
def marks_report():
    data = load_data()

    roll = input("Enter Roll Number: ")

    for s in data["students"]:
        if s["roll"] == roll:

            print("\n--- Marks Report ---")

            if not s["marks"]:
                print("No marks available.")
                return

            total = 0

            for m in s["marks"]:
                grade = calculate_grade(m["marks"])

                print(
                    m["subject"],
                    ":",
                    m["marks"],
                    "Grade:",
                    grade
                )

                total += m["marks"]

            average = total / len(s["marks"])

            print("Total:", total)
            print("Average:", round(average, 2))
            print("Overall Grade:", calculate_grade(average))
            return

    print("Student not found!")

# Library Management
def add_book():
    data = load_data()

    book_id = input("Enter Book ID: ")

    for book in data["books"]:
        if book["id"] == book_id:
            print("Book ID already exists!")
            return

    name = input("Enter Book Name: ")
    author = input("Enter Author: ")

    data["books"].append({
        "id": book_id,
        "name": name,
        "author": author,
        "available": True
    })

    save_data(data)

    print("Book added successfully!")

# Display Books
def display_books():
    data = load_data()

    print("\n--- Library Books ---")

    for book in data["books"]:
        status = (
            "Available"
            if book["available"]
            else "Issued"
        )

        print(
            book["id"],
            book["name"],
            book["author"],
            status
        )

# Issue Book
def issue_book():
    data = load_data()

    book_id = input("Enter Book ID: ")

    for book in data["books"]:
        if book["id"] == book_id:

            if book["available"]:
                book["available"] = False
                save_data(data)
                print("Book issued successfully!")
            else:
                print("Book is already issued!")

            return

    print("Book not found!")

# Return Book
def return_book():
    data = load_data()

    book_id = input("Enter Book ID: ")

    for book in data["books"]:
        if book["id"] == book_id:

            if not book["available"]:
                book["available"] = True
                save_data(data)
                print("Book returned successfully!")
            else:
                print("Book is already available!")

            return

    print("Book not found!")

# Fee Management
def add_fee():
    data = load_data()

    roll = input("Enter Student Roll Number: ")

    student_exists = any(
        s["roll"] == roll for s in data["students"]
    )

    if not student_exists:
        print("Student not found!")
        return

    try:
        amount = float(input("Enter Fee Amount: "))
    except ValueError:
        print("Invalid amount!")
        return

    if amount <= 0:
        print("Amount must be positive!")
        return

    data["fees"].append({
        "roll": roll,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    save_data(data)

    print("Fee payment recorded!")

# Fee Report
def fee_report():
    data = load_data()

    roll = input("Enter Student Roll Number: ")

    records = [
        f for f in data["fees"]
        if f["roll"] == roll
    ]

    if not records:
        print("No fee records found!")
        return

    total = sum(f["amount"] for f in records)

    print("\n--- Fee Report ---")

    for f in records:
        print(f["date"], "Rs.", f["amount"])

    print("Total Paid: Rs.", total)

# Main Menu
def main():

    initialize()

    while True:

        print("\n")
        print("=" * 45)
        print("       SMART CAMPUS MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Register Student")
        print("2. Display Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Mark Attendance")
        print("6. Attendance Report")
        print("7. Add Marks")
        print("8. Marks Report")
        print("9. Add Library Book")
        print("10. Display Books")
        print("11. Issue Book")
        print("12. Return Book")
        print("13. Add Fee")
        print("14. Fee Report")
        print("15. Exit")

        choice = input("\nEnter Your Choice: ")

        if choice == "1":
            register_student()

        elif choice == "2":
            display_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            delete_student()

        elif choice == "5":
            mark_attendance()

        elif choice == "6":
            attendance_report()

        elif choice == "7":
            add_marks()

        elif choice == "8":
            marks_report()

        elif choice == "9":
            add_book()

        elif choice == "10":
            display_books()

        elif choice == "11":
            issue_book()

        elif choice == "12":
            return_book()

        elif choice == "13":
            add_fee()

        elif choice == "14":
            fee_report()

        elif choice == "15":
            print("Thank You!")
            break

        else:
            print("Invalid Choice! Try Again.")

if __name__ == "__main__":
    main()
