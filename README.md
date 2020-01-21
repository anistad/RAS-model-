# RAS-model-

This repository contains the code for the RAS energy model, developed as part of my Master's Thesis: Energy use and efficiency in Recirculating
Aquaculture Systems (RAS). 
The details regarding assumptions and modeling is detailed in the Master's Thesis report. The Project Thesis report is found in the repository.

## To run the model
1. ```git clone``` into desired directory
2. Install Anaconda: https://www.anaconda.com/distribution/#windows 
3. In the terminal, create an environement and install the required packages by 
    ```conda create --name <env> --file req.txt```
4. Activate the environment by ```conda activate env```
5. The model can then be run in spyder or any other IDE installed in the environment

## Code 
The file energy_functions.py contaians the functions needed to calculate the energy use of each water treatment process. 
Then the file classes.py defines the system. The main class is RAS, which can contain a number of different departments. Each department has defined dimensions and flow rates, and the energy use is calculated for each department before summed. Finally the class fish is a subclass of departments, and contains the variables concerning fish growth, feed intake, oxygen consumption etc. The file run_example1.py shows a simple example of defining a system and running the model. 

By running the file run_RAS.py, the RAS described in the Master's Thesis is defined and simulated. The output is a df containing the SEC for fish with a weight from 171 g to 4000 g. 

The output files for the results shown in the Master's Thesis report is included in the folder output files. 
The input files for growth, feed and oxygen consumption are included in the files growth.xlsx (base case) and growth2.xlsx (25% decreased growth rate)


