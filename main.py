"""Tableau metadata exporter script."""
import fnmatch
import os
import shutil
import time
import warnings
from pathlib import Path
from zipfile import ZipFile

from cryptography.utils import CryptographyDeprecationWarning

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
from urllib.parse import urlparse

import paramiko
import psycopg2
import pyodbc
from dotenv import load_dotenv
from lxml import etree  # noqa: S410

load_dotenv()
PSQLADMIN = urlparse(
    os.environ.get(
        "PSQLADMIN", "postgres://tblwgadmin:password@localhost:8060/workgroup"
    )
)
PSQLRO = urlparse(
    os.environ.get("PSQLRO", "postgres://readonly:password@hostname:8060/workgroup")
)
SSHHOST = os.environ.get("SSHHOST", "tableauServer")
SSHUSERNAME = os.environ.get("SSHUSERNAME", "mr_cool")
SSHPASSWORD = os.environ.get("SSHPASSWORD", "12345")
SLEEP = int(os.environ.get("Sleep", 5))
TABLEAUURL = os.environ.get("TABLEAUURL", "https://tableau.example.com")
SQLSERVER = os.environ.get(
    "SQLSERVER",
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=sqlServer;DATABASE=atlas_staging;UID=joe;PWD=12345",
)


session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
session.connect(
    hostname=SSHHOST,
    port=22,
    username=SSHUSERNAME,
    password=SSHPASSWORD,
)
# remove old lines
stdin, stdout, stderr = session.exec_command("del /f /Q C:\\Users\\Public\\ETL_SQL\\")

if len(stderr.readlines()) > 0:
    err = "".join(stderr.readlines())
    raise Exception(f"Failed to remove old files.\n{err}")

# note, there must be NO SPACE between your password and the "&&"!
stdin, stdout, stderr = session.exec_command(
    f"cd \"C:\\Program Files\\Tableau\\Tableau Server\\packages\\pgsql*\" && cd bin && SET PGPASSWORD={PSQLADMIN.password}& psql -U {PSQLADMIN.username} -a -d {PSQLADMIN.path.replace('/','')} -h {PSQLADMIN.hostname} -p {PSQLADMIN.port} -c \"SELECT LO_EXPORT(OID, 'C:\\Users\\Public\\ETL_SQL\\' || REPO_TEMP.ID || '_' || REPO_TEMP.REPOSITORY_URL || LO_TEMP.FILETYPE)  FROM  (SELECT W.ID,  W.REPOSITORY_URL,  RD.CONTENT AS oid FROM WORKBOOKS W  INNER JOIN REPOSITORY_DATA RD ON COALESCE(W.DATA_ID, W.REDUCED_DATA_ID) = RD.TRACKING_ID) AS repo_temp  LEFT JOIN  (SELECT LOID,  CASE  WHEN SUBSTRING(DATA  FROM 1 FOR 4) = 'PK\\003\\004' THEN '.twbx' ELSE '.twb'  END AS filetype  FROM PG_LARGEOBJECT WHERE PG_LARGEOBJECT.PAGENO = 0  ) AS lo_temp ON REPO_TEMP.OID = LO_TEMP.LOID;\""
)

if len(stderr.readlines()) > 0:
    err = "".join(stderr.readlines())
    raise Exception(f"Failed to remove old files.\n{err}")


time.sleep(SLEEP)
sftp = session.open_sftp()
sftp.chdir(r"C:\Users\Public\ETL_SQL")

if os.path.exists("TwbxFiles"):
    shutil.rmtree("TwbxFiles")
os.makedirs(str(Path(__file__).parents[0] / "TwbxFiles"))
for my_file in sftp.listdir():
    sftp.get(my_file, str(Path(__file__).parents[0] / "TwbxFiles" / my_file))
session.close()

for my_file in Path(__file__).parents[0].joinpath("TwbxFiles").glob("*.twbx"):
    with ZipFile(my_file, "r") as myzip:
        myzip.extractall(str(Path(__file__).parents[0] / "TwbxFiles"))


parser = etree.XMLParser(ns_clean=True, recover=True)

output = []

if len(list((Path(__file__).parents[0] / "TwbxFiles").glob("*.twb"))) < 1:
    raise Exception("No files loaded!")


for my_file in (Path(__file__).parents[0] / "TwbxFiles").glob("*.twb"):
    tree = etree.parse(str(my_file), parser=parser)  # noqa: S320

    for datasource in tree.getroot().find("datasources").findall("datasource"):
        connection = datasource.find("connection")
        if connection is None:
            continue
        named_connections = connection.find("named-connections")

        if named_connections is None:
            continue
        dict_db = {}
        for node in named_connections.getchildren():
            inner_connection = node.find("connection")

            dict_db[node.get("name")] = {
                "database": (
                    ("use %s;\n" % inner_connection.get("dbname"))
                    if inner_connection.get("dbname") is not None
                    else ""
                ),
                "server": (
                    ("-- server: %s\n" % inner_connection.get("server"))
                    if inner_connection.get("server") is not None
                    else ""
                ),
                "one-time-sql": (inner_connection.get("one-time-sql") or ""),
            }

        for node in connection.getchildren():
            # relations with child queries
            if node.tag.endswith("relation") and node.findall("relation"):
                for childnode in node.findall("relation"):
                    this_conn = {}
                    conn_string = (
                        dict_db[childnode.get("connection")].get("server", "")
                        + dict_db[childnode.get("connection")].get("database", "")
                        + dict_db[childnode.get("connection")].get("one-time-sql", "")
                        if dict_db.get(childnode.get("connection"))
                        else ""
                    )
                    this_conn["sql"] = (
                        conn_string
                        + "\n\n/*"
                        + (
                            ("connection: " + childnode.get("connection"))
                            if childnode.get("connection")
                            else ""
                        )
                        + (
                            (" name: " + childnode.get("name"))
                            if childnode.get("name")
                            else ""
                        )
                        + (
                            (" table: " + childnode.get("table"))
                            if childnode.get("table")
                            else ""
                        )
                        + "*/\n\n"
                        + (childnode.text or "")
                    )
                    this_conn["ReportId"] = (
                        tree.getroot().find("repository-location").get("id")
                    )
                    output.append(this_conn)

            # relations with query
            elif node.tag.endswith("relation") and node.text:
                this_conn = {
                    "sql": (
                        dict_db[node.get("connection")].get("server", "")
                        + dict_db[node.get("connection")].get("database", "")
                        + dict_db[node.get("connection")].get("one-time-sql", "")
                        + "\n\n/*"
                        + (
                            ("connection: " + node.get("connection"))
                            if node.get("connection")
                            else ""
                        )
                        + ((" name: " + node.get("name")) if node.get("name") else "")
                        + (
                            (" table: " + node.get("table"))
                            if node.get("table")
                            else ""
                        )
                        + "*/\n\n"
                        + (node.text)
                    ),
                    "ReportId": tree.getroot().find("repository-location").get("id"),
                }
                output.append(this_conn)

connection = pyodbc.connect(SQLSERVER)

cur = connection.cursor()

cur.execute(
    """
    DELETE FROM [raw].[tableau-queries] WHERE 1=1;
    DELETE FROM [raw].[tableau-hierarchy] WHERE 1=1;
    DELETE FROM [raw].[tableau-groups] WHERE 1=1;
    DELETE FROM [raw].[tableau-users] WHERE 1=1;
    DELETE FROM [raw].[tableau-rundata] WHERE 1=1;
    DELETE FROM [raw].[tableau-reports] WHERE 1=1;
    """
)

for sql in output:
    cur.execute(
        "INSERT INTO [raw].[tableau-queries] (ReportId, Query) VALUES ( ?, ? )",
        sql["ReportId"],
        sql["sql"],
    )

connection.commit()

conn = psycopg2.connect(
    f"dbname={PSQLRO.path.replace('/','')} user={PSQLRO.username} host={PSQLRO.hostname} password={PSQLRO.password} port={PSQLRO.port}"
)
cursor = conn.cursor()

for my_file in (Path(__file__).parents[0] / "SQL").glob("*.sql"):
    with open(my_file, encoding="utf8") as sql_file:
        sql = sql_file.read()
        cursor.execute(sql.replace("TABLEAUURL", TABLEAUURL))
        results = cursor.fetchall()

        if fnmatch.fnmatch(my_file, "*WorkAndView.sql"):
            sql = """INSERT INTO [raw].[tableau-hierarchy]
            (ParentID, ChildID, [Index]) VALUES (?, ?, ?)"""
            cur.executemany(sql, results)
            cur.commit()

        elif fnmatch.fnmatch(my_file, "*Groups.sql"):
            sql = """INSERT INTO [raw].[tableau-groups] (UserID, GroupName) VALUES (?, ?)"""
            cur.executemany(sql, results)
            cur.commit()

        elif fnmatch.fnmatch(my_file, "*Users.sql"):
            sql = (
                """INSERT INTO [raw].[tableau-users] (UserID, username) VALUES (?, ?)"""
            )
            cur.executemany(sql, results)
            cur.commit()

        elif fnmatch.fnmatch(my_file, "*RunData.sql"):
            sql = """INSERT INTO [raw].[tableau-rundata]
            (EventDate, UserID, DashboardID, Nviews, Series) VALUES (?, ?, ?, ?, ?)"""
            cur.executemany(sql, results)
            cur.commit()

        elif fnmatch.fnmatch(my_file, "*Views.sql"):
            sql = """
                INSERT INTO [raw].[tableau-reports]
                (Type, ID, Name, URL, Created, Updated, [Index], OwnerID)
                VALUES ('Dashboard', ?, ?, ?, ?, ?, ?, ?)
                """
            cur.executemany(sql, results)
            cur.commit()

        elif fnmatch.fnmatch(my_file, "*Workbooks.sql"):
            sql = """
                INSERT INTO [raw].[tableau-reports]
                (Type, ID, Name, Description, Created, Updated, URL, WorkbookName, OwnerID)
                VALUES ('Workbook', ?, ?, ?, ?, ?, ?, ?, ?)
                """
            cur.executemany(sql, results)
            cur.commit()

connection.commit()
connection.close()
conn.close()
