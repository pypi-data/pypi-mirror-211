import subprocess
import json

def old_skool():
    # Run the PowerShell command
    powershell_command = "Get-StartApps | ConvertTo-Json"
    process = subprocess.Popen(["powershell", "-Command", powershell_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding="utf-8")
    output, error = process.communicate()

    # Check for any errors
    if error:
        print("Error:", error)

    # Parse the output as JSON
    parsed_output = json.loads(output)
    return parsed_output