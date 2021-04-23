USE [TableauSQL]
GO
SET
  ANSI_NULLS ON
GO
SET
  QUOTED_IDENTIFIER ON
GO
  CREATE TABLE [dbo].[Groups](
    [UserID] [int] NULL,
    [GroupName] [nvarchar](max) NULL
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET
  ANSI_NULLS ON
GO
SET
  QUOTED_IDENTIFIER ON
GO
  CREATE TABLE [dbo].[Hierarchy](
    [ParentID] [nvarchar](max) NULL,
    [ChildID] [nvarchar](max) NULL,
    [Index] [int] NULL
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET
  ANSI_NULLS ON
GO
SET
  QUOTED_IDENTIFIER ON
GO
  CREATE TABLE [dbo].[Query](
    [ReportId] [nvarchar](max) NULL,
    [Query] [nvarchar](max) NULL
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET
  ANSI_NULLS ON
GO
SET
  QUOTED_IDENTIFIER ON
GO
  CREATE TABLE [dbo].[Reports](
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
SET
  ANSI_NULLS ON
GO
SET
  QUOTED_IDENTIFIER ON
GO
  CREATE TABLE [dbo].[RunData](
    [EventDate] [datetime] NULL,
    [UserID] [int] NULL,
    [DashboardID] [int] NULL
  ) ON [PRIMARY]
GO
SET
  ANSI_NULLS ON
GO
SET
  QUOTED_IDENTIFIER ON
GO
  CREATE TABLE [dbo].[Users](
    [UserID] [int] NULL,
    [Username] [nvarchar](max) NULL
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
