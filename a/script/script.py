import subprocess
import numpy as np
import matplotlib.pyplot as plt

print("Start")

# Change working directory
cmd = "cd ../Script/../../noxim/bin/ && ./noxim -config ../config_examples/8x8.yaml -sim 1000"

# Explore how global average delay, network throughput, and energy consumption vary with packet injection rate



# Define a function to generate the command
def run_sim(filename, sim, packet_rate):
    base_cmd = "cd ../Script/../../noxim/bin/ && ./noxim -config"
    base_file = "../config_examples/"
    command = base_cmd + " " + base_file + filename + " -sim " + str(sim) + " -pir " + str(packet_rate) + " poisson"
    print(command)
    return command





# def get_results():
#     # Generate the command and run it, capturing output in a variable
#     command = run_sim("8x8.yaml", 1000,0.05)
#     try:
#         output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
#     except subprocess.CalledProcessError as e:
#         print("Error running command: ", e.output)
#         return None
    
#     #output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)

#     # Parse output to extract total received flits
#     total_received_flits = None
#     for line in output.split("\n"):
#         if line.startswith("% Total received flits:"):
#             total_received_flits = int(line.split(":")[1].strip())
#             break

#     # Save output to file
#     with open("output.txt", "w") as outfile:
#         outfile.write(output)

#     return total_received_flits

def get_results(packet_rate,cycles = 10000):
    # Generate the command and run it, capturing output in a variable
    command = run_sim("8x8.yaml", cycles, packet_rate)
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print("Error running command: ", e.output)
        return None

    # Parse output to extract required metrics
    global_average_delay = None
    network_throughput = None
    total_energy = None
    dynamic_energy = None
    static_energy = None
    max_delay = None
    for line in output.split("\n"):
        if line.startswith("% Global average delay"):
            global_average_delay = float(line.split(":")[1].strip())
        elif line.startswith("% Network throughput"):
            network_throughput = float(line.split(":")[1].strip())
        elif line.startswith("% Max delay"):
            max_delay = float(line.split(":")[1].strip())
        elif line.startswith("% Total energy"):
            total_energy = float(line.split(":")[1].strip())
        elif line.startswith("% 	Dynamic energy"):
            dynamic_energy = float(line.split(":")[1].strip())
        elif line.startswith("% 	Static energy"):
            static_energy = float(line.split(":")[1].strip())



    # Save output to file
    with open("output.txt", "w") as outfile:
        outfile.write(output)

    return global_average_delay, network_throughput, total_energy, dynamic_energy, static_energy, max_delay


def plot(x, y, xlabel, ylabel, title):
    plt.plot(x, y, 'o')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def subplotfunc(colour, axs, locx,locy, x,y, xlabel, ylabel, title):
    axs[locx,locy].plot(x, y, 'o-',color = colour)
    axs[locx,locy].set_xlabel(xlabel)
    axs[locx,locy].set_ylabel(ylabel)
    axs[locx,locy].set_title(title)

    # plt.show()




#flits= get_results()
global_average_delay_array = []
network_throughput_array = []
total_energy_array = []
dynamic_energy_array = []  
static_energy_array = []
max_delay_array = []
results = []
pir_rates = np.arange(0.0001, 0.03, 0.0001)
# pir_rate2 = np.arange(0.05, 0.1, 0.001)
# pir_rates = np.append(pir_rate1, pir_rate2)



for pir in pir_rates:
    print("RESULTS")
    # print(pir)
    # print(get_results(pir))
    results = get_results(pir,cycles = 10000)
    global_average_delay_array.append(results[0])
    network_throughput_array.append(results[1])
    total_energy_array.append(results[2])
    dynamic_energy_array.append(results[3])
    static_energy_array.append(results[4])
    max_delay_array.append(results[5])


# print(pir_rates)
# print(total_energy_array)
# Plot the two arrays against each other

fig, axs = plt.subplots(2, 3, figsize=(15, 10))

subplotfunc('red',axs,0,0,pir_rates, global_average_delay_array, 'Packet Injection Rate', 'Global Average Delay (cycles)', 'Plot of Global Average Delay vs PIR')
subplotfunc('black',axs,0,1,pir_rates, network_throughput_array, 'Packet Injection Rate', 'Network Throughput (flits/cycle)', 'Plot of Network Throughput vs PIR')
subplotfunc('purple',axs,0,2,pir_rates, max_delay_array, 'Packet Injection Rate', 'Max delay (cycles))', 'Plot of Max delay vs PIR')
subplotfunc('blue',axs,1,0,pir_rates, total_energy_array, 'Packet Injection Rate', 'Total energy (J)', 'Plot of Total energy vs PIR')
subplotfunc('green', axs,1,1,pir_rates, dynamic_energy_array, 'Packet Injection Rate', 'Dynamic energy (J)', 'Plot of Dynamic energy vs PIR')
subplotfunc('orange',axs,1,2,pir_rates, static_energy_array, 'Packet Injection Rate', 'Static energy (J)', 'Plot of Static energy vs PIR')

# axs[1, 2].axis('off')

# plt.tight_layout()
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.3)
plt.show()
