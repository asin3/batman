from behavior.intent_classifier import classify_intent

tests/test_intent.py
tests/test_history.py

while True:

    question = input("\nQuestion: ")

    intent = classify_intent(question)

    print(f"\nIntent: {intent}")