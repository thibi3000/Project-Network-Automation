#Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')) -y

#Allow global confirmation
choco feature enable -n allowGlobalConfirmation

#Install Git
choco install git -y

#Install Chrome
choco install googlechrome -y
