import subprocess

def install(package):
    try:
        subprocess.call(['pip2', 'install', package])
    except:
        unsuccessfull.append(package)

def upgrade(package):
    try:
        subprocess.call(['pip2', 'install', package, '--upgrade'])
    except:
        unsuccessfull.append(package)
        
def installPythonPackage(package):
    try:
        subprocess.call(['sudo', 'apt-get', 'install', 'python3-'+package])
    except:
        print(package,' already installed')

        
def installLinuxCommand(linux_commands):
    try:
        subprocess.call(['sudo', 'apt-get', 'install',linux_commands])
    except:
        print(linux_commands,' already installed')
        
unsuccessfull = []
packages = []
linux_commands=[]
with open('importPythonPackages.txt') as f:
    for line in f:    
        packages.append(line)

with open('importLinuxCommands.txt') as f1:
    for line in f1:    
        linux_commands.append(line)
print(linux_commands)

for package in packages:
    install(package)
    upgrade(package)
    installPythonPackage(package)
for command in linux_commands:
    installLinuxCommand(linux_commands)
print("\nUnsuccessfull: ",unsuccessfull)