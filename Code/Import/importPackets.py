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
        
def installLinuxCommand():
    try:
        subprocess.call(['sudo apt-get install', 'sysstat'])
    except:
        print('sysstat already installed')
        
unsuccessfull = []
packages = []

with open('importPackages.txt') as f:
    for line in f:    
        packages.append(line)

print(packages)

for package in packages:
    install(package)
    upgrade(package)
installLinuxCommand()
print("\nUnsuccessfull: ",unsuccessfull)