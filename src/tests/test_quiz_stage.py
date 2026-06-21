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

from quiz_manager import set_setup_stage
from quiz_manager import get_setup_stage

set_setup_stage("DIFFICULTY")

print(
    get_setup_stage()
)