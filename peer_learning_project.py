import mysql.connector
from datetime import datetime

# Database connection to Aiven MySQL
def get_connection():
    try:
        return mysql.connector.connect(
            host='mysql-teeghee-alustudent-ea0a.f.aivencloud.com',
            user='avnadmin',
            port=13667,
            password='',
            database='defaultdb',
            use_unicode=True,
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise
# Initialize database and create tables
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
# Create student's information table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            score INT CHECK (score >= 0 AND score <= 100),
            date DATE NOT NULL
        )
    ''')
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL,
            parent_name VARCHAR(100) NOT NULL,
            message TEXT NOT NULL,
            date DATE NOT NULL
        )
    ''')
    # Create parent responses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parent_responses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL,
            response TEXT NOT NULL,
            date DATE NOT NULL
        )
    ''')

# Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()
# Add new student record
def add_student():
    from datetime import datetime
    print("\n--- Add New Student Record ---")
    name = input("Student Name: ").strip() # Validate student name input
    if not name:
        print("Error: Student name cannot be empty.")
        return
        
    subject = input("Subject: ").strip()
    if not subject:
        print("Error: Subject cannot be empty.")
        return
# Validate score input
    while True:
        try:
            score = int(input("Score (0-100): "))
            if 0 <= score <= 100:
                break
            print("Error: Score must be between 0 and 100.")
        except ValueError:
            print("Error: Please enter a valid number.")
# Get current date
    date = datetime.now().strftime("%Y-%m-%d") 
    # Establish database connection and insert record
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (name, subject, score, date)
            VALUES (%s, %s, %s, %s)
        ''', (name, subject, score, date))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Added {name}'s {subject} score!")
    except mysql.connector.Error as err:
        print(f"Error adding student: {err}")
# View all records
def view_records():
    print("\n--- View All Records ---")
    # Check if there are any records to view
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students ORDER BY name')
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        if not records:
            print("\nNo records found.")
            return
# Print all records
        print("\n--- All Records ---")
        for row in records:
            print(f"ID: {row[0]} | {row[1]} | {row[2]} | Score: {row[3]}% | Date: {row[4]}")
    except mysql.connector.Error as err:
        print(f"Error viewing records: {err}")
# Generate progress report
def progress_report():
    # Check if there are any records to analyze
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name, subject, score FROM students')
        data = cursor.fetchall()
        cursor.execute('SELECT subject, AVG(score) FROM students GROUP BY subject')
        averages = cursor.fetchall()
        cursor.close()
        conn.close()
# Analyze data and print report
        if not data:
            print("\nNo records to analyze.")
            return
# Check if averages are empty
        if not averages:
            print("\nNo subject averages available.")
            return
        print("\n" + "=" * 110)
        print("Progress Report".center(110))
        print("\n" + "=" * 110)
        print(f"{'Name':<25} {'Subject'.center(50)} {'Score':^10} {'Status'.center(20)}")
        print("-" * 110)
        for name, subject, score in data:
            status = "🟢 Excellent" if score >= 70 else "🔴 Needs Help"
            print(f"{name:<25} {(subject).center(50)} {str(score) + '%':^10} {status.center(20)}")

        print("\n" + "=" * 110)
        print("Subject Averages".center(110))
        print("-" * 110)
        for subject, avg in averages:
            print(f"{subject:<50}: {avg:.1f}%")
    except mysql.connector.Error as err:
        print(f"Error generating progress report: {err}")
# Search parent and send message
def search_message_parent():
    print("\n--- Send Message to Parent ---")
    student_name = input("Enter Student's Name: ").strip()
    # Validate student name input
    if not student_name:
        print("Error: Student name cannot be empty.")
        return
    # Validate parent name input
    parent_name = input("Enter Parent's Name: ").strip()
    if not parent_name:
        print("Error: Parent name cannot be empty.")
        return
    # Validate message input 
    message = input("Enter Message: ").strip()
    if not message:
        print("Error: Message cannot be empty.")
        return
        
    date = datetime.now().strftime("%Y-%m-%d")
# Establish database connection and insert message
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (student_name, parent_name, message, date)
            VALUES (%s, %s, %s, %s)
        ''', (student_name, parent_name, message, date))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Message sent to {parent_name} for {student_name}.")
    except mysql.connector.Error as err:
        print(f"Error sending message: {err}")
# View parent responses
def view_parent_responses():
    # Check if there are any parent responses to view
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM parent_responses ORDER BY date DESC')
        responses = cursor.fetchall()
        cursor.close()
        conn.close()
        # Check if there are any responses
        if not responses:
            print("\nNo parent responses yet.")
            return

        print("\n--- Parent Responses ---")
        for row in responses:
            print(f"{row[1]} responded on {row[3]}: {row[2]}")
    except mysql.connector.Error as err:
        print(f"Error viewing parent responses: {err}")
        return
# Teacher dashboard for managing student records and communication
def teacher_dashboard():
    # Initialize database
    init_db()
    print("\nWelcome to the Teacher Dashboard!")
    # Main loop for dashboard menu
    while True:
        print("\n" + "="*35)
        print(" TEACHER DASHBOARD - ADMIN MENU")
        print("="*35)
        print("1. Add New Student Record")
        print("2. View All Records")
        print("3. Generate Progress Report")
        print("4. Search Parent and Send Message")
        print("5. View Parent Responses")
        print("6. Logout")
        # Get user choice
        choice = input("\nSelect option (1-6): ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            view_records()
        elif choice == "3":
            progress_report()
        elif choice == "4":
            search_message_parent()
        elif choice == "5":
            view_parent_responses()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")
# Main function to initialize database and start dashboard
def main():
    # Ensure the database is initialized before starting the dashboard
    try:
        init_db()
        teacher_dashboard()
    except Exception as e:
        print(f"Application error: {e}")
# Ensure the script runs only if executed directly
if __name__ == "__main__":
    main()