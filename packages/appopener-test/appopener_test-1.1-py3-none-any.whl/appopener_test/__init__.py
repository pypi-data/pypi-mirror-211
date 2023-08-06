__version__ = "1.6"
import os
from . import check

check.check_os()
# Checking if required files exists or not
check.check_json()
check.app_names()

# Get the path of working directory
main_path = os.path.join((check.get_path()), "Data")

# Run application (Regex implemented)
def run(self, output=True):
    print()
    print("THIS IS THE BETA VERSION (FOR JUST CHECKING METHOD OF CREATION OF FILES)")
    print()

