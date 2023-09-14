<h1 align="center">Tableau Metadata Exporter</h1>
<h4 align="center">Atlas BI Library ETL | Atlas Supplementary Tableau ETL</h4>
<p align="center">
    <a href="https://www.atlas.bi" target="_blank">Website</a> • <a href="https://demo.atlas.bi" target="_blank">Demo</a> • <a href="https://www.atlas.bi/docs/library/" target="_blank">Documentation</a> • <a href="https://discord.gg/hdz2cpygQD" target="_blank">Chat</a>
</p>
<p align="center">
 <a href="https://www.codacy.com/gh/atlas-bi/Tableau-Metadata-Exporter/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=atlas-bi/Tableau-Metadata-Exporter&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/fa2ce293d2c04df3bfe36f9bb3115973"/></a>
 <a href="https://sonarcloud.io/project/overview?id=atlas-bi_Tableau-Metadata-Exporter"><img alt="maintainability" src="https://sonarcloud.io/api/project_badges/measure?project=atlas-bi_Tableau-Metadata-Exporter&metric=sqale_rating"></a>
 <a href=""><img alt="security" src="https://sonarcloud.io/api/project_badges/measure?project=atlas-bi_Tableau-Metadata-Exporter&metric=security_rating" /></a>
 <a href="https://discord.gg/hdz2cpygQD"><img alt="discord chat" src="https://badgen.net/discord/online-members/hdz2cpygQD/" /></a>
 <a href="https://github.com/atlas-bi/Tableau-Metadata-Exporter/releases"><img alt="latest release" src="https://badgen.net/github/release/atlas-bi/Tableau-Metadata-Exporter" /></a>
</p>


<p align="center">
A Python script pulls and parses XML data from PSQL readonly Tableau database. This data, along with data pulled from Tableau's database, is inserted into a SQL database and is able to be run daily and inserted into Atlas.
</p>

## 🔧 How Does it Work?

1.  Logs in to the Tableau server via SSH and connects to the Tableau PSQL Admin account in the workgroup database
2.  The query will create `.twbx` and `.twb` files containing SQL queries related to the workbooks stored in Tableau
3.  The files retrieved are placed in the `TwbxFiles` folder and any zipped folders are unzipped
4.  All XML files are parsed and the server, database name, and SQL queries are pulled from each along with the the respective workbook
5.  Connection to SQL database is established and all tables are truncated so as not to duplicate data
6.  All PSQL queries are run and data pulled is stored in SQl tables

## 🏃 Getting Started

-   Get the code `git clone git@github.com:atlas-bi/Tableau-Metadata-Exporter.git`
-   Create the Atlas Staging database tables. Run the `create_tables.sql` script in your `atlas_staging` database
-   Install the project depenedencies `poetry install`, or `pip install` the dependencies listed in the `pyproject.toml` file
-   Set parameters (see below)
-   Run `poetry run python main.py`, or `python main.py`

## ⚙️Parameters

The python script accepts environment variables. This is the recommended way to run the script. You can also create a `.env` file to hold the parameters.
```bash
# Tableau's psql admin account. Documentation on Tabeau's website for getting the admin password.
PSQLADMIN=postgres://tblwgadmin:password@localhost:8060/workgroup
# Tableau's psql ro account
PSQLRO=postgres://readonly:password@hostname:8060/workgroup
# Atlas Staging database connection
SQLSERVER=DRIVER={ODBC Driver 17 for SQL Server};SERVER=sqlServer;DATABASE=atlas_staging;UID=joe;PWD=12345
# SSH Connection to Tableau Server. Old servers will need to install OpenSSH
SSHHOST=tableauServer
SSHUSERNAME=mr_cool
SSHPASSWORD=12345
# Url to Tableau
TABLEAUURL=https://tableau.example.com
```

Here's a few steps to get the Tableau PSQL admin and readonly passwords.

Navigate to the Tableau server and open command prompt.
```py
cd C:\Program Files\Tableau\Tableau Server\packages\pgsql.<version>\bin

#to retrieve the Tableau admin password
tsm configuration get -k pgsql.adminpassword

#to retrieve the readonly password
tsm configuration get -k pgsql.readonly_password
```

## 📝 Notes

Some of the PSQL queries that are run look at user and group data. To access these tables, try this [guide](https://github.com/tableau/community-tableau-server-insights). The user data is mostly found in the ts_users data source.

For a list of nearly all Tableau tables along with columns and descriptions, try this [guide](https://tableau.github.io/tableau-data-dictionary/2019.4/data_dictionary.htm).
