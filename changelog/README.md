# database_interface

Web front-end for research databases (initially MASS-BD database)

Framework: Python Flask

packages: flask, pandas, pyodbc, os



# Change Log (None Comprehensive, missing)

## Update 9/13/2021

Updated to the latest version

Highlight: account management, configuration file added

Next up: Date format error fix and account management hierarchy

## Update 8/4/2021

Completely implemented user saved queries

Implemented user change password

need to implement admin change password and enable/disable account

## Update 8/3/2021

Saved query access completed, need to work on redirecting to corresponding query

## Update 8/2/2021

Query Saving Implemented

Need to consider retrieving model and other displaying options.

## Update 7/30/2021

Fixed Some Bugs

## Update 7/29/2021

Updated endpoints for logout

## Update 7/28/2021

Added admin role which can register users

## Update 7/27/2021

Created Logins and basic authentication

Need to explore admin roles and email configurations.

## Update 7/26/2021

Created App Factory

Supports both partial and exact match search

created sql dabase for user information

## Update 7/21/2021

Added multiple selection on table selection

Allowed user to choose join type between tables

Enforced singular appearence of tables

## Update 7/20/2021

Added better Navigaions and input fields

Looking at dynamic table selections.

## Update 7/13/2021

Filtering option implemented, 

further testing may be needed for edge cases

Next Step is to explore adding filtering options on the table previewing page

## Update 7/12/2021

Multiple slect implemented with bootstrap multiselect

exploring sql generating methods to implement the filter

## Update 7/9/2021

Working on multiple select on the input page,

Ran into bug regarding the use of dropdown checkbox

Will explore more next week.

## Update 7/2/2021:

Added individual column search

Looking into customization

## Update 6/29/2021: 

Basic framework established. 

Table display and sample_id search.

Preview display using jquery datatable

Known issue: slow load time for large data

Next goal: Establish individual Search functions and talk more about table joining and column dropping.