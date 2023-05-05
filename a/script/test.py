import subprocess

print("Start")

# Change working directory
cmd = "cd ../Script/../../noxim/bin/ && ./noxim -config ../config_examples/8x8.yaml -sim 1000"

# Define a function to generate the command
def make_command(filename, sim):
    base_cmd = "cd ../Script/../../noxim/bin/ && ./noxim -config"
    base_file = "../config_examples/"
    command = base_cmd + " " + base_file + filename + " -sim " + str(sim)
    print(command)
    return command






def get_results():
    # Generate the command and run it, capturing output in a variable
    command = make_command("8x8.yaml", 1000)
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)

    # Parse output to extract total received flits
    total_received_flits = None
    for line in output.split("\n"):
        if line.startswith("% Total received flits:"):
            total_received_flits = int(line.split(":")[1].strip())
            break

    # Save output to file
    with open("output.txt", "w") as outfile:
        outfile.write(output)

    return total_received_flits

flits= get_results()
print(flits)
