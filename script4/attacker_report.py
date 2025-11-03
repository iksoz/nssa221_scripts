#Name:Zifeng Li
#11/03/2025
import os,subprocess,pathlib
from pathlib import Path
#,geoip
#from geoip import geolite2 

def report_gen():
    os.chdir(Path.home())
    os.chdir("student")
    stdoutput = subprocess.run(["pwd"],text=True,capture_output=True)
    print(stdoutput.stdout)

def main():
    os.system("clear")
    report_gen()

if __name__ == "__main__":
    main()