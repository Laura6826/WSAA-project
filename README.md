# Web Services and Applications 24-25: 8640

## Assignments submitted as part of the module Web Services and Applications 24-25: 8640, Higher Diploma in Science, Data Analytics

## *Author: Laura Lyons*

***

This README file was written using the [GitHub's documentation on READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) as a guidance document
***

  &#x26a0;&#xfe0f; **DISCLAIMER**

  Microsoft Co-Pilot was used to generate ideas of the content of the following notebook. That said, the notebook is mainly my own work, as I had to re-work the code the text in generated to meet my own needs (*The warning icon was sourced from [Stackoverflow](https://stackoverflow.com/questions/50544499/how-to-make-a-styled-markdown-admonition-box-in-a-github-gist)*).

## **Table of contents**

1. [Introduction.](#1-introduction).
1. [The purpose of this module.](#2-the-purpose-of-this-module)
1. [How to get started.](#3-how-to-get-started)
1. [How to get help.](#4-how-to-get-help)
1. [How to contribute.](#5-how-to-contribute)

## 1. Introduction

This project was created to fulfill an assessment requirement of Web Services and Applications 24-25: 8640, as part of the H.Dip in Science in Data Analytics.

This project is of **TYPE A:**

- A project that creates an application which provides an interface where online users can perform CRUD operations on a database.
- Which includes a Flask server that provides the RESTful API, and
- A web page that allows the user to interact with that RESTful API.

***

## 2. The purpose of this module

As noted on the [module introduction](https://vlegalwaymayo.atu.ie/course/view.php?id=12365),

- Introduce various means of retrieving data from external sources (for example CSO, weather servers, stock information).
- The module will look at the formats that data can come in (XML, JSON,CSV).
- How to retrieve (through an API) and process that data, using JavaScript and Python.
- Explore how to make your data available to the outside world by creating an API (Application Programmer's Interface) using the python module Flask.

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

For a seamless executition, I would also recommend you have access to the below libraries prior to running the files. The libraries required to run this file (as noted below), can be installed with the following code:

```ruby

```

,or you can manually install each of the libraries below.+

```ruby
import os
import json
import requests
from github import Github
from config import config as cfg
```

**Install Flask**:

```ruby
pip install -r requirements.txt
pip install flask 
pip install flask_sqlalchemy
pip install requests
```

- Flask is essential for building your RESTful API, SQLAlchemy for database interaction and Requests for fetching external API data:

***

**Initialize Project Structure**:

WSAA-project/
├── app.py                # Main Flask application
├── static/               # CSS and JavaScript files
├── templates/            # HTML files for the web interface
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation


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

### End.
