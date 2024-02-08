# Report template
This is a template for writing reports at AAU. 
The latex files are compiled locally on the computer. 

## Installing Tex
There are several different Tex distributions to choose from for compiling tex. 
We recomend using Tex Live since it comes with all packages which minimizes all the trouble for you. 
A guide to how to install Tex Live can be found [here](https://www.tug.org/texlive/)

Alternatively install MikTex. A guide can be found [here](https://miktex.org/download)

## Installing Python
Python is used for creating all the figures in the report. Therefore python needs to be installed. 
There are several different ways to do it Google is your friend ;-).



## IntelliJ Idea
The jetbrains tools are provided by AAU. Please make sure you have installed the Jetbrains toolbox and IntelliJ Idea Ultimate before proceeding. 

### Clone the repo
First download the repository. 

Then setup the right SDK, by pressing the gear in the to right corner, and then pressing project structure. 
Under project settings and project. 
Press the dropdown menu SDK: 
Choose "Add SDK" 
Add python SDK
Select new environment
Base interpreter should be your install of python and location should be inside the project in a directory called venv

Then to activate the virtual environment you just created open a terminal (Alt+F12) and run the following command: 
  source venv/Scripts/activate

The run the command: 
  pip install -r requirements.txt
If you would like to use some other python packages for creating the figures, simply add them to the requirements.txt and rerun the command. That way the rest of the group also gets the requirements when you push the next time. 



## Visual Studio



## 

