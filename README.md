# Seedstars jenkins test challenge

## Description
A Python that uses Jenkins' API to get a list of jobs and their status from a given Jenkins instance and store the record in a sqlite database along with the time for when it was checked.

## Requirement
1. Python 3.6
2. python-jenkins library you can check it out [here](https://python-jenkins.readthedocs.io/en/latest/index.html)

## Installation
Clone the project 
```
    git clone https://github.com/adekoder/seedstar-jenkins-test.git
```
Next CD into the project directory
```
    cd seedstars-jenkins-test
```

Next create a virtal environment.
```
    virtualenv --python=python3 venv
```

Next activate your virtal environment
```
    source venv/bin/activate
```

Next install the dependencies
```
    pip insatll requirement.txt
```

Running the script
```
    python jenkins_script.py
```

