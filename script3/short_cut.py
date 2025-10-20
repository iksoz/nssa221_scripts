import os,pathlib,subprocess,re
from pathlib import Path
#Zifeng Li, 10/20/2025
def menu():
    print("[1] Create a symbolic link")
    print("[2] Delete a symbolic link")
    print("[3] Create symbolic link report")
    print("[Q] Quit")
# def findPath():
#     pass
def createSymbolicLink():
    os.system("clear")
    name = input("Enter the file name: ")
    #Ensures that the script is ran in home
    os.chdir(Path.home())

    #searches for the file
    stdoutput = subprocess.run(["find",str(Path.home()),"-type","f","-name",name],text=True,capture_output=True)
    #handles the case where there's multiple files with same name or doesn't exist
    matches = [Path(p) for p in stdoutput.stdout.splitlines() if p.strip()]
    if len(matches)>1:
        index = 0
        for match in matches:
            print(index,match[index])
            index+=1
        try:
            choice = int(input("Which file do you want to creata symbolic link for(index): "))
            if choice >= len(matches) or choice < 0:
                print("Choice out of range")
                return 
            else:
                path = matches[choice]
        except:
            print("Bad input")
            return
    elif len(matches)==1:
        path = matches[0]
    elif not matches:
        print("File doesn't exist")
        return
    
    #safeguard user input
    
    

    if path != "":#safeguard against not finding a path
        cmd=["ln", "-s", path, f"{str(Path.home())}/{name}"]#establishes a symbolics link for the desginated file
        LinkCreate = subprocess.run(cmd,text=True, capture_output=True)
        print(f"Symbolic link created for {path} ")
    else:
        print("File does not exist")
    

def deleteSymbolicLink():
    os.system("clear")
    name = input("Enter the file name: ")
    link = Path(f"{str(Path.home())}/{name}")
    if not link.is_symlink():#checks if the file is a symbolic link or not
        print(f"{link} doesn't exist or is not a symbolic link.")
        return
    #deletes the symbolic file for the specified file
    link.unlink()
    print(f"symbolic link deleted for {name}")

    

def symbolicLinkReport():
    os.system("clear")
    #requirement: #of links, links and their target paths
    os.chdir(Path.home())
    cmd = ["find", ".", "-type", "l", "-printf", "link:%p -> target:%l\n"]
    process = subprocess.run(cmd,text=True, capture_output=True, check=True)#formats all symbolic links 
    # Print lines and show count
    lines = [line for line in process.stdout.splitlines() if line.strip()]#splits the output into lines
    for line in lines:
        print(line)
    print(f"\nTotal count of symbolic links: {len(lines)}")

def main():
    os.system("clear")
    userinput=""
    while(True):
        menu()
        userinput = input("Enter 1-3 or Q/q to quit:")
        if(userinput.lower() == "q"):
            break
        elif(int(userinput)==1):
            createSymbolicLink()
        elif(int(userinput)==2):
            deleteSymbolicLink()
        elif(int(userinput)==3):
            print(symbolicLinkReport())
        else:
            print("Invalid command\n")

if __name__ == "__main__":
    main()