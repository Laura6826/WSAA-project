# Web Services and Applications 24-25: 8640

## Assignments submitted as part of the module Web Services and Applications 24-25: 8640, Higher Diploma in Science, Data Analytics

## *Author: Laura Lyons*

***

This README file was written using the [GitHub's documentation on READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) as a guidance document
***

  &#x26a0;&#xfe0f; **DISCLAIMER**

  Microsoft Co-Pilot was used to generate ideas of the content of the following notebook. That said, the notebook is mainly my own work, as I had to re-work the code the text in generated to meet my own needs (*The warning icon was sourced from [Stackoverflow](https://stackoverflow.com/questions/50544499/how-to-make-a-styled-markdown-admonition-box-in-a-github-gist)*).

## **Table of contents**

1. [The purpose of this module.](#1-the-purpose-of-this-module).
1. [Introduction](#2-introduction)
1. [How to get started.](#3-how-to-get-started)
1. [How to get help.](#4-how-to-get-help)
1. [How to contribute.](#5-how-to-contribute)

## 1. The purpose of this module

As noted on the [module introduction](https://vlegalwaymayo.atu.ie/course/view.php?id=12365),

- Introduce various means of retrieving data from external sources (for example CSO, weather servers, stock information).
- The module will look at the formats that data can come in (XML, JSON,CSV).
- How to retrieve (through an API) and process that data, using JavaScript and Python.
- Explore how to make your data available to the outside world by creating an API (Application Programmer's Interface) using the python module Flask.

## 2. Introduction

This project was created to fulfill an assessment requirement of Web Services and Applications 24-25: 8640, as part of the H.Dip in Science in Data Analytics.

This project is of **TYPE A:**

- A project that creates an application which provides an interface where online users can perform CRUD operations on a database.
- Which includes a Flask server that provides the RESTful API, and
- A web page that allows the user to interact with that RESTful API.

***

For this project I created a web page where a user can choose a car park from a drop down menu, choose the most appropriate car park and recieve information on the number of space available and the opening hours nd possibly height restrictions assocated with that car park (READ).

Live data from Cork City Councils Parking API, is used to provide up to date information for car space availability, for 8 car parks with in the web page. I then created a MySql database, that stores the opening hours and height restrictions for each of these car parks.

The user also has the option to:

1. Add (CREATE) a car park (including a new name, opening hours and height restrictions)
2. UPDATE a car park (this will only update the information on the MySQL database and not the live API).
3. DELETE a car park (again only data found on the MySql database)

## 3. How to get started

### Necessary software

In order to run the included files, you will need to ensure that you have access to the correct software. I would recommend downloading the following applications (ensuring sufficient space on your hard drive prior to installation):

1. [Anaconda](https://www.atu.ie/sites/default/files/2024-02/aqae022-academic-integrity-policy-1.pdf) (if Anaconda is too large, miniconda would also suffice).
2. [Visual Studio Code](https://code.visualstudio.com/Download) (this is a code editor).

### **Additions to** *.gitignore*

A number of [additional files](https://github.com/github/gitignore/tree/main/Global) were added to my .gitignore prior to running the programmes:

  1. python.gitignore
  2. macOS..gitignore
  3. VisualStudioCode.gitignore
  4. Linux.gitignore
  5. TeX.gitignore
  6. Vim.gitignore
  7. Windows.gitignore

## How to run the project

### Using Visual Studio Code & Anaconda or GitHub Codespaces

**Clone the Repository**:

```ruby
   git clone https://github.com/Laura6826/WSAA-project
```

**Install the required packages**:

For a seamless executition, I would also recommend you have access to the below libraries prior to running the files. The libraries required to run this project.

**1. How to run the virtual environment**:

To get started, open a terminal (or command prompt) and navigate to the root of the WSAA-project. From there, activate the virtual environment by running the appropriate command for your operating system (for windows)

```ruby
venv\Scripts\activate
```

Once activated, you'll see the environment’s name in your prompt (typically preceded by “(venv)”), indicating that the isolated Python environment is running. This setup ensures that all dependencies installed via the requirements.txt file are used exclusively for this project.

OR

**2. Manually install @requirements.txt'**:

```ruby
pip install -r requirements.txt
```

**Project Structure**:

WSAA-project/
  .
  ├── dao
  │   ├── car_parks_dao.py     # DAO for the car park height restriction data.
  │   └── opening_hours_dao.py # DAO for parking data.
  ├── static                   # Folder for static assets
  │   ├── css                  # Folder for stylesheets
  │   │   └── style.css        # Main CSS file for styling
  │   ├── images               # Images used in your project (e.g., icons, backgrounds)
  │   └── js                   # Folder for JavaScript files
  │       └── script.js        # Main JavaScript file
  ├── templates                # Folder for HTML
  │   └── parking_checker.html # Main HTML file for the app
  ├── .gitignore               # Git ignored files
  ├── dbconfig.py              # Database configuration file
  ├── README.md                # Documentation for your project
  ├── requirements.txt         # Python dependencies
  └── server.py                # Main Flask application

### Open in Visual Studio Code

- Open Visual Studio Code.
- Open the `WSAA_project` folder.
- Open the folder associated with the assignment you wish to look at.

## 4. How to get help

I have attached below, a number of helpful links, should you wish to extrapolate on any of the methods used within this project.

1. [Anaconda](https://www.atu.ie/sites/default/files/2024-02/aqae022-academic-integrity-policy-1.pdf)
1. [Visual Studio Code](https://code.visualstudio.com/Download)
1. [w3schools](https://www.w3schools.com/)
1. [Pandas](https://pandas.pydata.org/)
1. [Numpy](https://numpy.org/)
1. [Matplotlib.py](https://matplotlib.org/)
1. [Seaborn](https://seaborn.pydata.org/)

Additionally, a number of links are embedded within the code, in areas that I found confusing, that should help should there be any difficulty.

## 5. How to contribute

As this project was created to fulfil an assessment requirement of the Web Services and Applications 24-25: 8640, as part of the H.Dip in Science in Data Analytics, no contributions will be allowed, in order to comply with ATU Policy on [Plagiarism](https://www.atu.ie/sites/default/files/2024-02/aqae022-academic-integrity-policy-1.pdf) and the [Student Code of Conduct](https://www.atu.ie/sites/default/files/2022-08/Student%20Code_Final_August_2022.pdf).

Should you find any errors or have any recommendations, please submit a pull request on GitHub. or just wish to contact that author, you can do so at <maxwell6826@gmail.com>.

***

### End
