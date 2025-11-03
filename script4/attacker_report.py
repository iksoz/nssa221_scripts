#Name:Zifeng Li
#11/03/2025
#! can be ran anywhere
import os,subprocess,pathlib,re,geoip
from pathlib import Path
from geoip import geolite2 

def report_gen():
    #locates and opens the syslog file
    os.chdir(Path.home())
    syslog = open("syslog.log")

    count = {}
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')#match IPs

    for line in syslog:
        matching = ip_pattern.findall(line)#find all IPs in line
        if len(matching) == 0:#continues if the line in log did not contain an ip
            continue
        for ip in matching:#add all ips found in the line into a stored set and dictionary
            count[ip] = count.get(ip,0) + 1
    syslog.close()  

    #searches for the country associated with the ip
    ip_counter_country = []
    for ip,counter in count.items():
        search = geolite2.lookup(ip)
        if search and counter >= 10:#if a country can be found associated with the ip and has more than 10 failed attempts
            countryFound = search.country#match the country
            ip_counter_country.append((counter,ip,countryFound))#formats it for output

    #sorts the list of entries
    ip_counter_country.sort()

    #format report
    stdoutput = subprocess.run(["date"],text=True,capture_output=True)
    print(stdoutput.stdout)
    print("COUNT","\tIP ADDRESS","\tCOUNTRY",sep="")

    for i in ip_counter_country:
        print(f"{i[0]:<7} {i[1]:<18} {i[2]}")

def main():
    os.system("clear")
    report_gen()

if __name__ == "__main__":
    main()