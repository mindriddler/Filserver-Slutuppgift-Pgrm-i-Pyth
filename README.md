# Filserver

## Author: Fredrik Magnusson [fredrik.magnusson2@yh.nackademin.se] ##

  

This is my version of the final assignment for the course "Programmering i Python" in the DevOps22 class at Nackademin.

---
# **Setup**

To use the program you will need python 3.10 or higher installed on your computer.

For instructions on how to install python 3.10, see further down below.

## Create and activate a virtual environment

Navigate to the folder where you cloned the repository and run the commands below in your terminal of choice.

#### Linux / OSX
```bash
python -m venv .venv # can also be python3

source .venv/bin/activate
```

#### Windows - cmd.exe

```
python -m venv .venv

.venv\Scripts\activate.bat
```

#### Windows - PowerShell

```powershell
# On Microsoft Windows, it may be required to enable the Activate.ps1 script by setting the execution policy for the user. You can do this by issuing the following PowerShell command:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

py -m venv .venv

.\.venv\Scripts\Activate.ps1
```

## Install requirements.txt 

```
pip install -r requirements.txt
```
---
## How to run the program

##### The program is made to be run over a local network, but may be configured manually to work over the internet if wanted.
1. #### Start the server
  Navigate to the folder where you cloned the repository and run the commands below in your terminal of choice.
```python
python server.py # can also be python3 or py, depending on the OS
```
2. #### Run as many clients as you want
```python
python client.py # can also be python3 or py, depending on the OS
```

##### As a client you can run the following commands;
```
- files      | Show you all available files on the server
- file_size  | Show you file size of a specified file
- remove     | Removes a specified file
- upload     | Upload a speficied file to the server
- download   | Download specified file to your download location
- dl_local   | Update your download location
- dc         | Disconnect from server
- s_close    | Turns off the server
```
## How to run tests

Navigate to the folder where you cloned the repository and run the command below in your terminal of choice.
```python
tox
```
This will give you a good visual overview of how many tests made and how well they cover the code.

I have not run any tests on socket function, seeing as this was not part of my assignment and also are not unit tests. And they are also not covered in the coverage readout.

If you want a lesser but quicker way to test you can run command below from the same folder.
```python
pytest
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
