CPS-035  ✅ Migrate user_repository.py
CPS-036  ✅ Migrate student_repository.py

--------------------------------------------

CPS-037 — Create progress_repository.py

Purpose:
Single source of truth for progress.json

Methods:
    initialize_progress()
    get_progress()
    save_progress()

--------------------------------------------

CPS-038 — Create history_repository.py

Purpose:
Conversation history and learning history.

Methods:
    initialize_history()
    get_history()
    save_history()
    append_entry()

--------------------------------------------

CPS-039 — Create schedule_repository.py

Purpose:
Student schedules.

Methods:
    initialize_schedule()
    get_schedule()
    save_schedule()

--------------------------------------------

CPS-040 — Create learning_state_repository.py

Purpose:
Learning engine state.

Methods:
    initialize_learning_state()
    get_learning_state()
    save_learning_state()

--------------------------------------------

CPS-041 — Batman-DD Integration

Replace every direct access to:

students/<id>/*.json

with repository calls.

--------------------------------------------

CPS-042 — Batman Platform Repository Freeze

Repository Layer becomes frozen.