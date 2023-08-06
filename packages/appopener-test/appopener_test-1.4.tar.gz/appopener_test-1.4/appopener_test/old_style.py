import subprocess
import json

import os

def get_powershell_path():
    try:
        # Default installation directories for PowerShell
        installation_directories = [
            r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe"
        ]

        # Check if the PowerShell executable exists in the default directories
        for path in installation_directories:
            if os.path.isfile(path):
                return path

        return None
    except Exception as e:
        print("Error occurred:", e)

# Call the function to get the PowerShell executable location
powershell_path = get_powershell_path()

print("PowerShell executable path:", powershell_path)

def old_skool():
    # Run the PowerShell command
    powershell_command = "Get-StartApps | ConvertTo-Json"
    process = subprocess.Popen([powershell_path, "-Command", powershell_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding="utf-8")
    output, error = process.communicate()

    # Check for any errors
    if error:
        print("Error:", error)

    # Parse the output as JSON
    parsed_output = json.loads(output)
    return parsed_output