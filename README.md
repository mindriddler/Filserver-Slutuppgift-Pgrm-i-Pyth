# Filserver

## Author: Fredrik Magnusson [fredrik.magnusson2@yh.nackademin.se] ##

  

This is my version of the final assignment for the course "Programmering i Python" in the DevOps22 class at Nackademin.

---
# **Setup**

To use the program you will need python 3.10 or higher installed on your computer
For how to install python 3.10, see instructions at the bottom

### Create and activate a virtual environment

Linux / OSX
```bash
python -m venv .venv # can also be python3

source .venv/bin/activate
```

Windows - cmd.exe

```
python -m venv .venv

.venv\Scripts\activate.bat
```

Windows - PowerShell

```powershell
# On Microsoft Windows, it may be required to enable the Activate.ps1 script by setting the execution policy for the user. You can do this by issuing the following PowerShell command:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

py -m venv .venv

.\.venv\Scripts\Activate.ps1
```

### Install requirements.txt 

```
pip install -r requirements.txt
```
---
## How to run the program
1. #### Start the server
```python
python server.py
```
2. #### Run as many clients as you want
```python
python client.py
```

As a client you can run the following commands;
- #### files 
```
	will return all files on the server
```
- #### file_size
```
	will return the file size of a specified file
```
- #### remove
```
	will remove a specific file from the server
```
- #### upload
 ```
	will upload a specified file from client
 ```
- #### download
```
	will download a specified file to the client
```

## How to install python

## **Windows** 

You can either download python by clicking **_[here](https://www.python.org/downloads/)_**

  

you can use also use winget by typing the line below into powershell

```powershell
winget install python --accept-package-agreements
```

<sup>read more about winget [here](https://learn.microsoft.com/en-us/windows/package-manager/winget/)</sup>

  

## **Linux** ##

First check if python3.10 is already installed

```
python3 -v
```

if you get no return from that input, follow below

```
sudo apt update

sudo apt-get install python3