## LifeTime_IGBT_Calculation

Open Source project for thermal analysis and modeling of power electronic components.
This project aims to provide a software platform for performing power loss calculations, estimating temperatures of electronic components, and predicting their operating lifetime.
It includes features for data retrieval from Excel files, signal processing, power loss calculation, thermal modeling, and cumulative damage analysis.
The project utilizes popular libraries such as NumPy, Pandas, SciPy, Matplotlib and Rainflow for data manipulation, scientific computation, and result visualization.

This project is open to contribution from the open source community. Feel free to explore the source code, submit issues, propose enhancements, and contribute to the project's development.

## Table of Contents
- [Installation](#Installation)
- [Usage](#Usage)
- [Contribute](#Contribute)
- [License](#License)

## Installation
This project requires specific versions of libraries. To setup your environment, you will need to have the following dependencies installed:

  Python: The project is written in Python. Ensure you have Python 3.6 or later installed.

  Libraries: Install the following Python libraries with the specified versions:
  - scipy==1.10.1
  - pandas==2.0.1
  - matplotlib==3.7.1
  - numpy==1.24.1
  - rainflow==3.2.0
  - openpyxl==3.1.2

You can install these packages using pip, which is a package manager for Python. If you're using a command line interface, type the following commands:

  - pip install scipy==1.10.1
  - pip install pandas==2.0.1
  - pip install matplotlib==3.7.1
  - pip install numpy==1.24.1
  - pip install rainflow==3.2.0
  - pip install openpyxl==3.1.2

To install the project, download all the files and maintain the same file organization.

## Usage
To use your own data, simply replace the files in the "examples" directory. The "variables.py" file contains a dictionary where you can store all the necessary data. For the Excel file, the required information is located at the end of the "variables.py" file.

If you wish to change the file location to match your preferred organization, modify line 4 in the "lifetime.py" file.
/!\ Make sure to provide the correct path to the Excel file to ensure proper data retrieval (line 52 in "variables.py").

To run the program, execute the "lifetime.py" file. Once everything is launched successfully, call the "global_calculation()" function. It will return the following values in order: "lifetime_IGBT", "lifetime_diode", "number_of_km_IGBT", "e_kwh_byhours", and "efficiency".

If you want to display the graphs for Torque, Speed, Current, and Total losses, you can uncomment line 33 in the "lifetime.py" file. This will enable the code to plot and show the graphs.

To integrate this program into your own script, you need to import the lifetime.py file. Following this, the function global_calculation can be invoked. Here's an example demonstrating this:

- import lifetime
- lifetime_IGBT, lifetime_diode = lifetime.global_calculation()

You can return more data like: "number_of_km_IGBT", "e_kwh_byhours", and "efficiency" by modifying line 51 in "lifetime.py"
## Example
An example of the code in action is detailed in the file [DetailedExample.md](https://gitlab.com/PGarn/LifeTime_IGBT_Calculation/-/blob/main/details/DetailedExample.md).

## Contribute
We welcome all kinds of contributions! To contribute to the project, start by forking the repository, make your proposed changes in a new branch and create a pull request. Please ensure your code is readable and well-documented. Include unit tests if possible. 

Also, you can contribute by submitting bug reports, feature requests, and issue tracking.

## License
This project is licensed under the terms of the MIT license. By contributing to the project, you agree that your contributions will be licensed under its MIT license.


