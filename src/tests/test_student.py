import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from conversation_manager import load_history
from conversation_manager import save_history

student_id = input("Enter Student ID: ")

history = load_history(student_id)

print("\nCurrent History:")
print(history)

message = input("\nEnter Message: ")

history.append(
    {
        "role": "user",
        "content": message
    }
)

save_history(student_id, history)

print("\nSaved Successfully")