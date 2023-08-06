__version__ = "1.6"
import os, json
from . import check

check.check_os()
# Checking if required files exists or not
check.check_json()
check.app_names()

# Get the path of working directory
main_path = os.path.join((check.get_path()), "Data")


def list_apps():
    print()
    with open((os.path.join(main_path,"data.json")),"r") as file:
        data = json.load(file)
        key = data.keys()
        keys = sorted(key)
        count = 0
        for app in keys:
            if len(app.strip()) == 0 :
                continue
            else:
                count += 1
                print("{}. {}".format(count, app.strip().upper()))
    print()


# Run application (Regex implemented)
def run(self, output=True):
    print()
    print(self)
    if self == "ls":
        list_apps()
    else:
        os.system("explorer shell:appsFolder\\"+self)
    print()


def give_path():
    print(main_path)


