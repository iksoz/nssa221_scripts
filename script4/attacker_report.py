#Name:Zifeng Li
#11/03/2025
import os,subprocess,pathlib,re,geoip
from pathlib import Path
from geoip import geolite2 

def report_gen():
    #locates and opens the syslog file
    os.chdir(Path.home())
    os.chdir("student")
    syslog = open("syslog.log")

    ips = set()
    count = {}
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')#match IPs

    for line in syslog:
        matching = ip_pattern.findall(line)#find all IPs in line
        if len(matching) == 0:
            continue
        for ip in matching:#add all ips found in the line into a stored set and dictionary
            ips.add(ip)
            count[ip] = count.get(ip,0) + 1
    syslog.close()  

    #searches for the country associated with the ip
    ip_counter_country = []
    for ip,counter in count.items():
        countryFound = geolite2.lookup(ip)
        if countryFound:
            ip_counter_country += [counter,ip,countryFound]

    #format report
    print("COUNT","\tIP ADDRESS","\tCOUNTRY")
    for i in ip_counter_country:
        print(i)

def main():
    os.system("clear")
    report_gen()

if __name__ == "__main__":
    main()