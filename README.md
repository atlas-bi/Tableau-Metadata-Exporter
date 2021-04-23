[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b6bec0c189e240228baca3941e851e5b)](https://www.codacy.com/gh/Riverside-Healthcare/Tableau-Metadata-Exporter/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Riverside-Healthcare/Tableau-Metadata-Exporter&amp;utm_campaign=Badge_Grade)
[![CodeQL](https://github.com/Riverside-Healthcare/Tableau-Metadata-Exporter/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Riverside-Healthcare/Tableau-Metadata-Exporter/actions/workflows/codeql-analysis.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/3297bc558ec0f992b9ce/maintainability)](https://codeclimate.com/github/Riverside-Healthcare/Tableau-Metadata-Exporter/maintainability)

# Tableau Metadata Exporter

## About

Tableau runs a Python script that pulls and parses XML data from PSQL readonly Tableau database. This data, along with data queried from PSQL workgroup Tableau database, is inserted into a SQL database and is able to be run daily and inserted into Atlas. If multiple queries are found in a report, there will be a database entry for each query.

### What It Does

It logs in to the Tableau server and connects to the Tableau PSQL Admin account in the workgroup database.

1. The query will create .twbx and .twb files containing SQL queries related to the workbooks stored in Tableau
2. The files retrieved are placed in the "TwbxFiles" folder and any zipped folders are unzipped
3. All XML files are parsed and the server, database name, and SQL queries are pulled from each along with the the respective workbook
4. Connection to SQL database is established to hold Tableau data. All tables are truncated so as not to duplicate data
5. All PSQL queries are run and data pulled is stored in SQl tables

## How To Run

### First, install poetry

This script uses [poetry](https://python-poetry.org/docs/) as the python package manager.

### Next, install Python packages

Since this script utilizes poetry, just run:

```sh
poetry install
```

### Create Database

```SQL
CREATE DATABASE [TableauSQL]
 GO
```

### Create Tables

Run create_tables.sql

### Create settings.py file

```py
PSQL_Server = ("dbname=database_name user=username host=hostname password=password port=port")

SQL_Server = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server_name;DATABASE=database_name;UID=username;PWD=password"

SSH_Host = "SSH_server_name"
SSH_Username = "username"
SSH_Password = "password"

PSQL_Admin = '"host=host port=port dbname=database_name user=username password=password"'

Sleep = number of seconds

# this is the path to the psql executable on the Tableau server
Path_to_PSQL = (
    r'"\\\\network\\c$\\path\\to\\psql\\files\\'
)
```

### Run

```sh
poetry run python main.py
```

## Additional Information

Some of the PSQL queries that are run look at user and group data. To access these tables, try this [guide](https://github.com/tableau/community-tableau-server-insights). The user data is mostly found in the ts_users data source.

For a list of nearly all Tableau tables along with columns and descriptions, try this [guide](https://tableau.github.io/tableau-data-dictionary/2019.4/data_dictionary.htm).
