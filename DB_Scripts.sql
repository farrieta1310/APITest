USE [master]
GO

/****** Object:  Database [DataTest]    Script Date: 7/24/2023 12:00:38 PM ******/
CREATE DATABASE [DataTest]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'DataTest', FILENAME = N'/var/opt/mssql/data/DataTest.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 10%)
 LOG ON 
( NAME = N'DataTest_log', FILENAME = N'/var/opt/mssql/data/DataTest_log.ldf' , SIZE = 1024KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO

IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [DataTest].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO

ALTER DATABASE [DataTest] SET ANSI_NULL_DEFAULT OFF 
GO

ALTER DATABASE [DataTest] SET ANSI_NULLS OFF 
GO

ALTER DATABASE [DataTest] SET ANSI_PADDING OFF 
GO

ALTER DATABASE [DataTest] SET ANSI_WARNINGS OFF 
GO

ALTER DATABASE [DataTest] SET ARITHABORT OFF 
GO

ALTER DATABASE [DataTest] SET AUTO_CLOSE OFF 
GO

ALTER DATABASE [DataTest] SET AUTO_SHRINK OFF 
GO

ALTER DATABASE [DataTest] SET AUTO_UPDATE_STATISTICS ON 
GO

ALTER DATABASE [DataTest] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO

ALTER DATABASE [DataTest] SET CURSOR_DEFAULT  GLOBAL 
GO

ALTER DATABASE [DataTest] SET CONCAT_NULL_YIELDS_NULL OFF 
GO

ALTER DATABASE [DataTest] SET NUMERIC_ROUNDABORT OFF 
GO

ALTER DATABASE [DataTest] SET QUOTED_IDENTIFIER OFF 
GO

ALTER DATABASE [DataTest] SET RECURSIVE_TRIGGERS OFF 
GO

ALTER DATABASE [DataTest] SET  DISABLE_BROKER 
GO

ALTER DATABASE [DataTest] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO

ALTER DATABASE [DataTest] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO

ALTER DATABASE [DataTest] SET TRUSTWORTHY OFF 
GO

ALTER DATABASE [DataTest] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO

ALTER DATABASE [DataTest] SET PARAMETERIZATION SIMPLE 
GO

ALTER DATABASE [DataTest] SET READ_COMMITTED_SNAPSHOT OFF 
GO

ALTER DATABASE [DataTest] SET HONOR_BROKER_PRIORITY OFF 
GO

ALTER DATABASE [DataTest] SET RECOVERY SIMPLE 
GO

ALTER DATABASE [DataTest] SET  MULTI_USER 
GO

ALTER DATABASE [DataTest] SET PAGE_VERIFY CHECKSUM  
GO

ALTER DATABASE [DataTest] SET DB_CHAINING OFF 
GO

ALTER DATABASE [DataTest] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO

ALTER DATABASE [DataTest] SET TARGET_RECOVERY_TIME = 0 SECONDS 
GO

ALTER DATABASE [DataTest] SET DELAYED_DURABILITY = DISABLED 
GO

ALTER DATABASE [DataTest] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO

ALTER DATABASE [DataTest] SET QUERY_STORE = OFF
GO

ALTER DATABASE [DataTest] SET  READ_WRITE 
GO


USE DataTest;

CREATE TABLE HIRED_EMPLOYEES
(
ID INT,
NAME VARCHAR(100),
HIRE_DATE DATETIME,
DEPARTMENT_ID INT,
JOBS_ID INT
);

CREATE TABLE DEPARTMENTS
(
DEPARTMENT_ID INT,
DEPARTMENT_NAME VARCHAR(150)
);

CREATE TABLE JOBS
(
JOBS_ID INT,
DEPARTMENT_NAME VARCHAR(150)
);

CREATE PROCEDURE dbo.ADD_JOBS(@job_id int, @department varchar(150))
AS
BEGIN
	SET NOCOUNT ON;
	BEGIN TRY
		--Attempt to insert into the jobs table
		INSERT INTO dbo.JOBS([JOBS_ID],[DEPARTMENT_NAME])
		VALUES(@job_id, @department);

		SELECT 'Success' AS RESULT;
	END TRY
	BEGIN CATCH
		SELECT ERROR_NUMBER() AS ErrorNumber, ERROR_MESSAGE() AS ErrorMessage
	END CATCH
END;

CREATE PROCEDURE dbo.ADD_DEPARTMENTS(@department_id int, @department varchar(150))
AS
BEGIN
	SET NOCOUNT ON;
	BEGIN TRY
		--Attempt to insert into the department table
		INSERT INTO dbo.DEPARTMENTS([DEPARTMENT_ID],[DEPARTMENT_NAME])
		VALUES(@department_id, @department);

		SELECT 'Success' AS RESULT;
	END TRY
	BEGIN CATCH
		SELECT ERROR_NUMBER() AS ErrorNumber, ERROR_MESSAGE() AS ErrorMessage
	END CATCH
END;

CREATE PROCEDURE dbo.ADD_HIRED_EMPLOYEES(@id int, @name varchar(100), @hire_date datetime, @department_id varchar(10), @job_id varchar(10))
AS
BEGIN
	SET NOCOUNT ON;

	DECLARE @fixed_dept INT,
	        @fixed_job INT

	BEGIN TRY
		SET @fixed_dept = (SELECT CAST(CAST(CASE WHEN @department_id = 'NaN' THEN NULL ELSE @department_id END AS FLOAT)AS INT));
		SET @fixed_job = (SELECT CAST(CAST(CASE WHEN @job_id = 'NaN' THEN NULL ELSE @job_id END AS FLOAT)AS INT))

		--Attempt to insert into the hired employees table
		INSERT INTO dbo.HIRED_EMPLOYEES([ID],[NAME], [HIRE_DATE], [DEPARTMENT_ID], [JOBS_ID])
		VALUES(@id, @name, @hire_date, @fixed_dept, @fixed_job);

		SELECT 'Success' AS RESULT;
	END TRY
	BEGIN CATCH
		SELECT ERROR_NUMBER() AS ErrorNumber, ERROR_MESSAGE() AS ErrorMessage
	END CATCH
END;
