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

from quiz_manager import (
    set_setup_data,
    get_setup_data,
    clear_setup_data
)

set_setup_data(
    {
        "topics": ["force"],
        "difficulty": "hard",
        "count": 5
    }
)

print(
    get_setup_data()
)

clear_setup_data()

print(
    get_setup_data()
)