import subprocess
import numpy as np
import matplotlib.pyplot as plt
import sys

import matplotlib.colors as mcolors

# Get all colors
all_colors = list(mcolors.CSS4_COLORS.keys())
# Get a subset of evenly spaced colors
colors = [all_colors[i] for i in np.linspace(10, len(all_colors) - 1, 20).astype(int)]


# colors = ['blue', 'green', 'red']
print("Start")

# Change working directory
cmd = "cd ../Script/../../noxim/bin/ && ./noxim -config ../config_examples/8x8.yaml -sim 1000"

# Explore how global average delay, network throughput, and energy consumption vary with packet injection rate



# Define a function to generate the command
def run_sim(filename, sim, packet_rate, hotspot, percentage,buffer):
    base_cmd = "cd ../Script/../../noxim/bin/ && ./noxim -config"
    base_file = "../config_examples/"
    command = base_cmd + " " + base_file + filename + " -sim " + str(sim) + " -pir " + str(packet_rate) + " poisson " + " -buffer " + str(buffer)
    if hotspot:
        for j in range(0,2):
            for i in range(1,5):
                command = command + " -hs " + str(i + j*8) + " " +str(percentage)
        
    print("-----------------------------------")
    print(command)
    print("-----------------------------------")


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

def get_results(packet_rate,cycles,hotspot, percentage,buffer = 4,file = "8x8.yaml",):
    # Generate the command and run it, capturing output in a variable
    
    command = run_sim("8x8.yaml", cycles, packet_rate,hotspot, percentage,buffer)
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

def subplotfunchold(colour, axs, locx,locy, x,y,xlabel, ylabel,title,config):
    for index, series in enumerate(y):
      print("test")
      print(config[index])
      
      axs[locx,locy].plot(x,series, 'o-',color = colors[index], label=str(config[index]))
      axs[locx,locy].set_xlabel(xlabel)
      axs[locx,locy].set_ylabel(ylabel)
      axs[locx,locy].set_title(title)
      axs[locx,locy].legend()

      # axs[locx, locy].plot(x, new_y,  'o-',color = colour)

def plotresults(pir_rates,global_average_delay_array,network_throughput_array,max_delay_array,total_energy_array,dynamic_energy_array,static_energy_array,config):
  fig, axs = plt.subplots(2, 3, figsize=(15, 10))
  subplotfunchold('red',axs,0,0,pir_rates, global_average_delay_array, 'Packet Injection Rate', 'Global Average Delay (cycles)', 'Plot of Global Average Delay vs PIR',config)
  subplotfunchold('pink',axs,0,1,pir_rates, network_throughput_array, 'Packet Injection Rate', 'Network Throughput (flits/cycle)', 'Plot of Network Throughput vs PIR',config)
  subplotfunchold('purple',axs,0,2,pir_rates, max_delay_array, 'Packet Injection Rate', 'Max delay (cycles))', 'Plot of Max delay vs PIR',config)
  subplotfunchold('blue',axs,1,0,pir_rates, total_energy_array, 'Packet Injection Rate', 'Total energy (J)', 'Plot of Total energy vs PIR',config)
  subplotfunchold('green', axs,1,1,pir_rates, dynamic_energy_array, 'Packet Injection Rate', 'Dynamic energy (J)', 'Plot of Dynamic energy vs PIR',config)
  subplotfunchold('orange',axs,1,2,pir_rates, static_energy_array, 'Packet Injection Rate', 'Static energy (J)', 'Plot of Static energy vs PIR',config)
  plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.3)
  plt.show()


#flits= get_results()

# pir_rate1 = np.arange(0.0001, 0.03, 0.0001)
# pir_rate2 = np.arange(0.05, 0.1, 0.001)
# pir_rates = np.append(pir_rate1, pir_rate2)
pir_rates = np.arange(0.001, 0.05, 0.01)
#A
global_average_delay_array = []
network_throughput_array = []
total_energy_array = []
dynamic_energy_array = []  
static_energy_array = []
max_delay_array = []
results_array = []


global_average_delay = []
network_throughput = []
total_energy = []
dynamic_energy = []  
static_energy = []
max_delay = []
results = []

buffers = [2,4,8]
routing_algorithms = ["XY","WestFirst","NorthLast","NegativeFirst","OddEven","DyAD","Random"]
topologies = ["Mesh","Torus","FatTree","FullyConnected"]



# Parse command line arguments
for arg in sys.argv[1:]:
    print('Argument:', arg)



for buffer in buffers:
  for pir in pir_rates:
    results = get_results(pir,10000,False,0,buffer)
    global_average_delay.append(results[0])
    network_throughput.append(results[1])
    total_energy.append(results[2])
    dynamic_energy.append(results[3])
    static_energy.append(results[4])
    max_delay.append(results[5])


  results_array.append(results) 
  global_average_delay_array.append(global_average_delay)
  network_throughput_array.append(network_throughput)
  total_energy_array.append(total_energy)
  dynamic_energy_array.append(dynamic_energy)
  static_energy_array.append(static_energy)
  max_delay_array.append(max_delay)


  global_average_delay = []
  network_throughput = []
  total_energy = []
  dynamic_energy = []
  static_energy = []
  max_delay = []

  
  print(global_average_delay_array)

plotresults(pir_rates,global_average_delay_array,network_throughput_array,max_delay_array,total_energy_array,dynamic_energy_array,static_energy_array,buffers)



