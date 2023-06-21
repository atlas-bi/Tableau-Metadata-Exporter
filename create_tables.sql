USE [atlas_staging]
GO
SET
  ANSI_NULLS ON
GO
SET
  QUOTED_IDENTIFIER ON
GO
  CREATE TABLE [raw].[tableau-groups](
    [UserID] [int] NULL,
    [GroupName] [nvarchar](max) NULL
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
  CREATE TABLE [raw].[tableau-hierarchy](
    [ParentID] [nvarchar](max) NULL,
    [ChildID] [nvarchar](max) NULL,
    [Index] [int] NULL
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
  CREATE TABLE [raw].[tableau-queries](
    [ReportId] [nvarchar](max) NULL,
    [Query] [nvarchar](max) NULL
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
  CREATE TABLE [raw].[tableau-reports](
    [Type] [nvarchar](max) NULL,
    [ID] [int] NULL,
    [Name] [nvarchar](max) NULL,
    [Description] [nvarchar](max) NULL,
    [Created] [datetime] NULL,
    [Updated] [datetime] NULL,
    [Index] [int] NULL,
    [URL] [nvarchar](max) NULL,
    [WorkbookName] [nvarchar](max) NULL
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
  CREATE TABLE [raw].[tableau-rundata](
    [EventDate] [datetime] NULL,
    [UserID] [int] NULL,
    [DashboardID] [int] NULL,
    [Nviews] [int] NULL,
    [Series] [int] NULL
  ) ON [PRIMARY]
GO
  CREATE TABLE [raw].[tableau-users](
    [UserID] [int] NULL,
    [Username] [nvarchar](max) NULL
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

CREATE TABLE raw.TableauSubscriptions
(
Id int NULL
,TargetType nVarchar(50) NULL
,TargetId int NULL
, Created datetime NULL
, LastRun dateTime NULL
, UserId int NULL
, UserName nVarchar(50) NULL
, Description nVarchar(250) NULL
, Details nVarchar(1000) NULL

)