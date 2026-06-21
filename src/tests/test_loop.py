student_id = input("Enter Student ID: ")

while True:

    question = input("\nAsk Batman: ")

    if question.lower() == "exit":
        break

    print(f"\nYou asked: {question}")

print("\nSession Ended")