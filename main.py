import subprocess


def run_moss():
    # Define the command to run
    command = ["bash", "./run.sh"]

    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode != 0:
        print("Error running MoSS:", result.stderr)
        return

    # Parse the output
    output = result.stdout
    # there's some data in result.stderr
    parse_output(output)


def parse_output(output):
    # Print raw output (optional)
    print("Raw Output:\n", output)


# Run the function
run_moss()
