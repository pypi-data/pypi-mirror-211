import subprocess
import json

def get_powershell_path():
    try:
        # Execute the 'where' command to locate the PowerShell executable
        output = subprocess.check_output(["where", "powershell"], universal_newlines=True)

        # Extract the first line (executable location)
        executable_path = output.splitlines()[0]

        return executable_path
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