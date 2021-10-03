# Datebase Interface

Author: Vincent Chiang

I developed this application as part of my internship at Vitalant Research Institute during the summer of 2021. The goal of this application is essentially making existing databases more accessible to the lab members. Our slogan is "Data for the People", and we want people without technical background to query through the database using a graphical user interface. This project is piloted with the CDC seroprevalence database which the institute is partnered with to manage. This project is under development by me, and this public repository will be updated periodically. All sensitive information has been removed in this version.

Main platform of development: Python, Flask

## Features

Table selection: Users can choose the tables they want to view and specify the join types between the tables.

Filter options: Users can add filtering options to further narrow their searches. This is where the "WHERE" clause of the query are specified.

Table preview: Users can preview the data on the application and/or download it as a CSV onto their machine.

User Logins: The application uses FLASK_SECURITY to implement a login system where users need to be authenticated to login. Admins and super users also have management right of people's account.

Saved Queries: Users have the ability to save the cuurent query to their account and access it at a later time.

### Please navigate to the change log directory for the version changes.