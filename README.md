# Datebase Interface

Author: Vincent Chiang

I developed this application as part of my internship at [Vitalant Research Institute](https://research.vitalant.org) during the summer of 2021. The goal of this application is to make research databases more accessible to lab staff who are not familiar relational databases and SQL. Our slogan is "Data for the People", and we want people without technical backgrounds to be able to query complex relational databases using a graphical user interface. This project was piloted with the database for the [CDC Multistate Assessment of SARS-CoV-2 Seroprevalence in Blood Donors (MASS-BD) study](https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/blood-bank-serosurvey.html). This project is under development by me, and this public repository will be updated periodically. All sensitive information has been removed from this version.

Guidance on development goals were provided by Mars Stone, Hasan Sulaeman and Eduard Grebe.

Main platform for development: Python (>=3.8), Flask

## Features

Table selection: Users can choose the tables they want to view and specify the join types between the tables.

Filter options: Users can add filtering options to further narrow their searches. This is where the "WHERE" clause of the query are specified.

Table preview: Users can preview the data on the application and/or download it as a CSV onto their machine.

User Logins: The application uses FLASK_SECURITY to implement a login system where users need to be authenticated to login. Admins and super users also have management right of people's account.

Saved Queries: Users have the ability to save the cuurent query to their account and access it at a later time.

## Installation and running

The application can be run on any Unix-based machine that has Python 3 available by 

1. Cloning this repository
2. Editing the `config.py` file as appropriate
3. Executing the following commands while in the project directory:

```
./create_venv.sh
./activate_venv.sh
cd ..
set FLASK_APP=database_interface
flask run
```

### Please navigate to the change log directory for the version changes.