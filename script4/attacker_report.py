#Name:Zifeng Li
#11/03/2025
import os,subprocess,pathlib,re
from pathlib import Path
#,geoip
#from geoip import geolite2 

def report_gen():
    #locates and opens the syslog file
    os.chdir(Path.home())
    os.chdir("student")
    syslog = open("syslog.log")
    ips = []
    for line in syslog:
        part = line.split(" ")
        matching = re.findall(r"(?:\d{1,3}\.){3}\d{1,3}",line)
        if matching not in ips:
            ips+= matching
        elif matching in ips:
            continue

    syslog.close()

    print(ips)

def main():
    os.system("clear")
    report_gen()

if __name__ == "__main__":
    main()