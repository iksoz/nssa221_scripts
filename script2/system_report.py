import os,platform,subprocess,re,glob,datetime
#Zifeng Li, 10/16/2025
# Translates numbes to their corresponding months
NUM_TO_MONTH = {
    "1"  : "January",
    "2"  : "February",
    "3"  : "March",
    "4"  : "April",
    "5"  : "May",
    "6"  : "June",
    "7"  : "July",
    "8"  : "August",
    "9"  : "September",
    "10" : "October",
    "11" : "November",
    "12" : "December"
}

PADDING_SIZE = 30

def get_date():
    """
    Returns the current date in string form
    Ex: May 3, 2025
    """
    # today() will return yyyy-mm-dd
    cur_date = str(datetime.date.today()).split("-")
    year = cur_date[0]
    month = cur_date[1]
    day = cur_date[2]

    # Switches the number form to the word form
    month = NUM_TO_MONTH[month]

    return f"{month} {day}, {year}"

def print_device_info():
    """
    Finds the device host name and domain name and prints it out
    """
    cmd = ["hostname"]
    result = subprocess.run(cmd, text=True, capture_output=True).stdout.strip()

    # finds the index where the first period occurs
    # user.domain_name
    first_period = result.find(".")

    # Splice to get user
    host_name = result[:first_period]
    # Splice to get domain name
    domain_name = result[first_period+1:]

    print("Device Information")
    print(f"{'Hostname:':<{PADDING_SIZE}} {host_name}")
    print(f"{'Domain:':<{PADDING_SIZE}} {domain_name}")
    print()

def get_host_ip():
    """
    Returns the IP of the host
    """
    # This command just returns the host ip address
    cmd = ["hostname","-I"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def get_default_gateway():
    """
    Gets the user default gateway
    """
    cmd = ["ip", "route"]
    routes = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    # Grabs the default line
    cmd = ["egrep", "default"]
    default_line = subprocess.run(cmd, stdin=routes.stdout, text=True, capture_output=True)

    # the ip is located on the 2nd index
    d_gateway_ip = default_line.stdout.strip().split()[2]
    return d_gateway_ip

def get_network_mask():
    """
    Finds the network mask of the host
    """
    cmd = ["ifconfig"]
    ifconfig_result = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    # Search for the line with netmask
    cmd = ["egrep", "netmask "]
    egrep_inet_result = subprocess.Popen(cmd, stdin=ifconfig_result.stdout, stdout=subprocess.PIPE)

    # Removes the loopback from consideration
    cmd = ["egrep", "-v", "127.0.0.1"]
    egrep_no_127 = subprocess.run(cmd, stdin=egrep_inet_result.stdout, text=True, capture_output=True)

    # Splits the result of egrep_no_127 using white space
    tokens = egrep_no_127.stdout.strip().split()
    
    # index 3 contains the netmask
    return tokens[3]

def get_dns_info():
    """
    Get the dns information for the host
    """
    cmd = ["cat", "/etc/resolv.conf"]
    cat_result = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    # Get the lines for name server
    cmd = ["egrep", "nameserver"]
    egrep_result = subprocess.run(cmd, stdin=cat_result.stdout, text=True, capture_output=True)
    tokens = egrep_result.stdout.strip().split()
    # 0 and 2 are "nameserver", so we should only return 1 and 3
    return tokens[1], tokens[3]

def print_network_info():
    """
    Calls the functions to get all network details
    Prints the necessary information
    """
    host_ip = get_host_ip()
    df_gateway_ip = get_default_gateway()
    network_mask_ip = get_network_mask()
    dns = get_dns_info()

    print("Network Information")
    print(f"{'IP Address:':<{PADDING_SIZE}} {host_ip}")
    print(f"{'Gateway:':<{PADDING_SIZE}} {df_gateway_ip}")
    print(f"{'Network Mask:':<{PADDING_SIZE}} {network_mask_ip}")
    print(f"{'DNS1:':<{PADDING_SIZE}} {dns[0]}")
    print(f"{'DNS2:':<{PADDING_SIZE}} {dns[1]}")
    print()

def get_os_name():
    """
    Grabs information from /etc/*release to get the pretty name for the current os
    """
    glob_path = "/etc/*release"
    cmd = ["cat"]
    # Glob is necessary as we're using subprocess to run this glob path
    os_info = subprocess.Popen(cmd + glob.glob(glob_path), stdout=subprocess.PIPE)

    cmd = ["grep", "PRETTY_NAME="]
    os_name = subprocess.run(cmd, stdin=os_info.stdout, text=True, capture_output=True).stdout
    os_name = os_name.lstrip("PRETTY_NAME=").strip().strip('"')

    return os_name

def get_os_version():
    """
    Grabs information from /etc/*release to get the version ID for the current os
    """
    glob_path = "/etc/*release"
    cmd = ["cat"]
    # Glob is necessary as we're using subprocess to run this glob path
    os_info = subprocess.Popen(cmd + glob.glob(glob_path), stdout=subprocess.PIPE)
    
    cmd = ["grep", "VERSION_ID="]
    os_version = subprocess.run(cmd, stdin=os_info.stdout, text=True, capture_output=True).stdout
    os_version = os_version.lstrip("VERSION_ID=").strip().strip('"')

    return os_version

def get_kernel_info():
    cmd = ["uname", "-r"]
    result = subprocess.run(cmd, text=True, capture_output=True)
    return result.stdout.strip()

def print_os_info():
    os_name = get_os_name()
    os_version = get_os_version()
    kernel_info = get_kernel_info()

    print("Operating System Information")
    print(f"{'Operating System:':<{PADDING_SIZE}} {os_name}")
    print(f"{'OS Version:':<{PADDING_SIZE}} {os_version}")
    print(f"{'Kernel Version:':<{PADDING_SIZE}} {kernel_info}")
    print()

def print_storage_info():
    cmd = ["df", "-h", "/home/"]
    df_rs = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    cmd = ["grep", "-v", "Filesystem"]
    grep_rs = subprocess.run(cmd, stdin=df_rs.stdout, text=True, capture_output=True)
    tokens = grep_rs.stdout.strip().split()
    total = tokens[1].replace("G", " Gib")
    used = tokens[2].replace("G", " Gib")
    avil = tokens[3].replace("G", " Gib")

    print("Stroage Information")
    print(f"{'System Drive Total:':<{PADDING_SIZE}} {total}")
    print(f"{'System Drive Used:':<{PADDING_SIZE}} {used}")
    print(f"{'System Drive Free:':<{PADDING_SIZE}} {avil}")
    print()

def print_processor_info():
    cmd = ["cat", "/proc/cpuinfo"]
    cat_res = subprocess.run(cmd, capture_output=True, text=True).stdout

    model_name_line = re.search(r"model name.*\n", cat_res).group() # type: ignore
    model_name = model_name_line.split(":")[1].strip()

    processor_lines = re.findall(r"processor.*\n", cat_res)
    num_of_processor = len(processor_lines)

    core_lines = re.findall(r"cpu cores.*\n", cat_res)
    num_of_cores = 0
    for line in core_lines:
        cur_core_num = line.split(":")[1].strip()
        cur_core_num = int(cur_core_num)
        num_of_cores += cur_core_num
    
    print("Processor Information")
    print(f"{'CPU Model:':<{PADDING_SIZE}} {model_name}")
    print(f"{'Number of Processors:':<{PADDING_SIZE}} {num_of_processor}")
    print(f"{'Number of Cores:':<{PADDING_SIZE}} {num_of_cores}")
    print()

def print_memory_info():
    # Will be ouput as megabyte
    cmd = ["free", "--mega"]
    result = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

    tokens = re.search("Mem:.*\n", result).group().split() # type: ignore
    tot_mem = int(tokens[1]) / 1000
    # tot_mem = str(tot_mem)
    avil_mem = int(tokens[3]) / 1000
    # avil_mem = str(avil_mem)


    print(f"{'Total RAM:':<{PADDING_SIZE}} {tot_mem:.2f} GB")
    print(f"{'Available:':<{PADDING_SIZE}} {avil_mem:.2f} GB")


def main():
    subprocess.run("clear")

    print(f"System Report: {get_date()}")
    print()
    
    print_device_info()
    
    print_network_info()

    print_os_info()

    print_storage_info()

    print_processor_info()

    print_memory_info()


if __name__ == "__main__":
    main()
