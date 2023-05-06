import subprocess
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib.colors as mcolors


# Get all colors
all_colors = list(mcolors.CSS4_COLORS.keys())

# Get a subset of evenly spaced colors
colors = [all_colors[i] for i in np.linspace(10, len(all_colors) - 1, 20).astype(int)]


default_hotspotsIDs = ['1','2','3','4','9','10','11','12']

# Define a function to generate the command
def gen_command(filename, sim, packet_rate,percentage, hotspotsIDs, buffer = 4,topology = "MESH", routing = "XY"):
    base_cmd = "cd ../Script/../../noxim/bin/ && ./noxim -config"
    base_file = "../config_examples/"
    command = base_cmd + " " + base_file + filename + " -sim " + str(sim) + " -pir " + str(packet_rate) + " poisson " + " -buffer " + str(buffer) + " -routing " + str(routing) + " -topology " + str(topology) 

    for hotspotID in hotspotsIDs:
         command = command + " -hs " + str(hotspotID) + " " +str(percentage)
    
        
    print("-----------------------------------")
    print(command)
    print("-----------------------------------")
    return command



def get_results(packet_rate,cycles,hotspot, percentage ,config, config_name = None,hotspot_config = default_hotspotsIDs, file = "8x8.yaml",):
    # Generate the command and run it, capturing output in a variable
    
    #Fix default params
    if config_name == None:
        command = gen_command("8x8.yaml", cycles, packet_rate, percentage,)
    elif config_name == "buffer":
        command = gen_command("8x8.yaml", cycles, packet_rate, percentage,hotspot_config, config)
    elif config_name == "topology":
        command = gen_command("8x8.yaml",config, cycles, packet_rate,percentage, hotspot_config, 4, config)
    elif config_name == "routing":
        command = gen_command("8x8.yaml", cycles, packet_rate, percentage,hotspot_config, 4, "MESH", config)
    elif config_name == "hotspot":
        command = gen_command("8x8.yaml", cycles, packet_rate, percentage,hotspot_config,4, "MESH", "XY")
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




def subplotfunchold(colour, axs, locx,locy, x,y,xlabel, ylabel,title,config,colours):
    for index, series in enumerate(y):  
      axs[locx,locy].plot(x,series, 'o-',color = colours[index], label=str(config[index]))
      axs[locx,locy].set_xlabel(xlabel)
      axs[locx,locy].set_ylabel(ylabel)
      axs[locx,locy].set_title(title)
      axs[locx,locy].legend()

      # axs[locx, locy].plot(x, new_y,  'o-',color = colour)

def plotresults(pir_rates,global_average_delay_array,network_throughput_array,max_delay_array,total_energy_array,dynamic_energy_array,static_energy_array,config,colours):
  fig, axs = plt.subplots(2, 3, figsize=(15, 10))
  subplotfunchold('red',axs,0,0,pir_rates, global_average_delay_array, 'Packet Injection Rate', 'Global Average Delay (cycles)', 'Plot of Global Average Delay vs PIR',config,colours)
  subplotfunchold('pink',axs,0,1,pir_rates, network_throughput_array, 'Packet Injection Rate', 'Network Throughput (flits/cycle)', 'Plot of Network Throughput vs PIR',config,colours)
  subplotfunchold('purple',axs,0,2,pir_rates, max_delay_array, 'Packet Injection Rate', 'Max delay (cycles))', 'Plot of Max delay vs PIR',config,colours)
  subplotfunchold('blue',axs,1,0,pir_rates, total_energy_array, 'Packet Injection Rate', 'Total energy (J)', 'Plot of Total energy vs PIR',config,colours)
  subplotfunchold('green', axs,1,1,pir_rates, dynamic_energy_array, 'Packet Injection Rate', 'Dynamic energy (J)', 'Plot of Dynamic energy vs PIR',config,colours)
  subplotfunchold('orange',axs,1,2,pir_rates, static_energy_array, 'Packet Injection Rate', 'Static energy (J)', 'Plot of Static energy vs PIR',config,colours)
  plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.3, hspace=0.3)
  plt.show()



def run_simulation(configs,config_name,pir_rates,colours, hotspot_config = default_hotspotsIDs):
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
    for config in configs:
        for pir in pir_rates:
            results = get_results(pir,10000,False,0.05,config,config_name,hotspot_config)
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

    plotresults(pir_rates,global_average_delay_array,network_throughput_array,max_delay_array,total_energy_array,dynamic_energy_array,static_energy_array,configs,colours)





# pir_rate1 = np.arange(0.0001, 0.03, 0.0001)
# pir_rate2 = np.arange(0.05, 0.1, 0.001)
# pir_rates = np.append(pir_rate1, pir_rate2)
pir_rates = np.arange(0.001, 0.05, 0.003)
#A


buffers = [2,4,8,16]
routing_algorithms = ["XY"] #,"WEST_FIRST","NORTH_LAST","NEGATIVE_FIRST","ODD_EVEN"]
topologies = ["default_configMesh.yaml","default_configBfly.yaml","default_configBaseline.yaml","default_configOmega.yaml"]

hotspot_config1 = ['1','2','3','4','9','10','11','12'] #[1,2,3,4,5,6,7,8]




step = 0.03

if '-p' in sys.argv[1:]:
    step = float(sys.argv[sys.argv.index('-p') + 1])



pir_rates = np.arange(0.001, 0.05, step)


if '-b' in sys.argv[1:]:
    colorsb = [all_colors[i] for i in np.linspace(10, len(all_colors) - 1, 20).astype(int)]
    run_simulation(buffers,"buffer",pir_rates,colorsb)

if '-r' in sys.argv[1:]:
    colorsr = [all_colors[i] for i in np.linspace(10, len(all_colors) - 1, 20).astype(int)]

    run_simulation(routing_algorithms,"routing",pir_rates,colorsr)
if '-t' in sys.argv[1:]:
    colorst = [all_colors[i] for i in np.linspace(10, len(all_colors) - 1, 20).astype(int)]
    run_simulation(topologies,"topology",pir_rates,colorst)

if '-h' in sys.argv[1:]:
    colorst = [all_colors[i] for i in np.linspace(10, len(all_colors) - 1, 20).astype(int)]
    run_simulation(["HotspotConfig1"], 'hotspot', pir_rates,colorst, hotspot_config1)
