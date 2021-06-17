"""Tableau metadata exporter script."""
import fnmatch
import os
import shutil
import time
from pathlib import Path
from zipfile import ZipFile

import paramiko
import psycopg2
import pyodbc
import settings
from lxml import etree  # noqa: S410

session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
session.connect(
    hostname=settings.SSH_Host,
    port=22,
    username=settings.SSH_Username,
    password=settings.SSH_Password,
)
channel = session.invoke_shell()
stdin = channel.makefile("wb")
stdout = channel.makefile("rb")
# pylint: disable=C0301
stdin.write(
    r"""
del /f /Q C:\Users\Public\ETL_SQL\
"""
    + settings.Path_to_PSQL
    + r"""psql" """
    + settings.PSQL_Admin
    + r"""
SELECT LO_EXPORT(OID,  'C:\Users\Public\ETL_SQL\' || REPO_TEMP.ID || '_' || REPO_TEMP.REPOSITORY_URL || LO_TEMP.FILETYPE)  FROM  (SELECT W.ID,  W.REPOSITORY_URL,  RD.CONTENT AS oid FROM WORKBOOKS W  INNER JOIN REPOSITORY_DATA RD ON COALESCE(W.DATA_ID, W.REDUCED_DATA_ID) = RD.TRACKING_ID) AS repo_temp  LEFT JOIN  (SELECT LOID,  CASE  WHEN SUBSTRING(DATA  FROM 1 FOR 4) = 'PK\003\004' THEN '.twbx' ELSE '.twb'  END AS filetype  FROM PG_LARGEOBJECT WHERE PG_LARGEOBJECT.PAGENO = 0  ) AS lo_temp ON REPO_TEMP.OID = LO_TEMP.LOID;"  # noqa: E501
\q
exit
"""
)

stdout.close()
stdin.close()
time.sleep(settings.Sleep)
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

for my_file in (Path(__file__).parents[0] / "TwbxFiles").glob("*.twb"):
    tree = etree.parse(str(my_file), parser=parser)  # noqa: S320

    for datasource in tree.getroot().find("datasources").findall("datasource"):
        connection = datasource.find("connection")

        if connection is None:
            continue
        named_connections = connection.find("named-connections")

        if named_connections is None:
            continue
        named_connection = named_connections.find("named-connection")

        if named_connection is None:
            continue
        query_info = named_connection.find("connection")

        if query_info is None:
            continue

        server = (
            ("-- server: %s\n" % query_info.get("server"))
            if query_info.get("server") is not None
            else ""
        )
        dbname = (
            ("use %s;\n" % query_info.get("dbname"))
            if query_info.get("dbname") is not None
            else ""
        )

        for node in connection.getchildren():

            # relations with query
            if node.tag.endswith("relation") and node.text:
                this_conn = {}
                this_conn["sql"] = (
                    server
                    + dbname
                    + (query_info.get("one-time-sql") or "")
                    + "\n\n/*"
                    + (
                        ("connection: " + node.get("connection"))
                        if node.get("connection")
                        else ""
                    )
                    + ((" name: " + node.get("name")) if node.get("name") else "")
                    + ((" table: " + node.get("table")) if node.get("table") else "")
                    + "*/"
                    + (node.text)
                )
                this_conn["ReportId"] = (
                    tree.getroot().find("repository-location").get("id")
                )
                output.append(this_conn)

            # relations with child queries
            elif node.tag.endswith("relation") and node.findall("relation"):
                for childnode in node.findall("relation"):
                    this_conn = {}
                    this_conn["sql"] = (
                        server
                        + dbname
                        + (query_info.get("one-time-sql") or "")
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
                        + "*/"
                        + (childnode.text)
                    )
                    this_conn["ReportId"] = (
                        tree.getroot().find("repository-location").get("id")
                    )
                    output.append(this_conn)

connection = pyodbc.connect(settings.SQL_Server)

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

conn = psycopg2.connect(settings.PSQL_Server)
cursor = conn.cursor()

for my_file in (Path(__file__).parents[0] / "SQL").glob("*.sql"):
    with open(my_file, "r") as sql_file:
        sql = sql_file.read()
        cursor.execute(sql)
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
            (EventDate, UserID, DashboardID) VALUES (?, ?, ?)"""
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
