from django.db import models, connection

# Create your models here.


def create_tables():
    raw_sql_query = """
    -- Create Faculty table without username and password
CREATE TABLE Faculty (
    FacultyID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    ContactNumber VARCHAR(15),
    Email VARCHAR(50),
    Address VARCHAR(100)
);

-- Create Credential table for storing usernames and hashed passwords
CREATE TABLE Credential (
    FacultyID INT PRIMARY KEY,
    Username VARCHAR(20) UNIQUE,
    PasswordHash VARCHAR(64),
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);

-- Create EducationDetails table
CREATE TABLE EducationDetails (
    EduID INT PRIMARY KEY,
    FacultyID INT,
    Degree VARCHAR(50),
    Major VARCHAR(50),
    University VARCHAR(50),
    YearOfPassing INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);

-- Create WorkExperience table
CREATE TABLE WorkExperience (
    ExpID INT PRIMARY KEY,
    FacultyID INT,
    Organization VARCHAR(100),
    Position VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);

-- Create Certificate table
CREATE TABLE Certificate (
    CertID INT PRIMARY KEY,
    FacultyID INT,
    CertificateName VARCHAR(100),
    IssuingAuthority VARCHAR(100),
    IssueDate DATE,
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);

-- Create Paper table
CREATE TABLE Paper (
    PaperID INT PRIMARY KEY,
    FacultyID INT,
    Title VARCHAR(100),
    Journal VARCHAR(50),
    PublicationDate DATE,
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);

-- Create Patent table
CREATE TABLE Patent (
    PatentID INT PRIMARY KEY,
    FacultyID INT,
    Title VARCHAR(100),
    PatentNumber VARCHAR(50),
    DateIssued DATE,
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);

-- Create Conference table
CREATE TABLE Conference (
    ConferenceID INT PRIMARY KEY,
    FacultyID INT,
    ConferenceName VARCHAR(100),
    Location VARCHAR(50),
    DateAttended DATE,
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);

-- Create AdminUser table
CREATE TABLE AdminUser (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(64)
);

-- Create Salary table
CREATE TABLE Salary (
    SalaryID INT PRIMARY KEY AUTO_INCREMENT,
    FacultyID INT,
    Amount DECIMAL(10, 2),
    PaymentDate DATE,
    Semester VARCHAR(20),
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);


-- Create Teaching table
CREATE TABLE Teaching (
    CourseID INT PRIMARY KEY AUTO_INCREMENT,
    FacultyID INT,
    Semester VARCHAR(20),
    Year INT,
    Department VARCHAR(50),
    Position VARCHAR(50),
    LeavesTaken INT,
    LeavesAllotted INT,
    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
);
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                print(data)
                return data
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        
# create_tables()
        
def alter_table_files():
    raw_sql_query = """
    -- Alter Certificate table to add FilePath column
    ALTER TABLE Certificate
    ADD COLUMN FilePath VARCHAR(255) NULL;

    -- Alter EducationDetails table to add TranscriptPath column
    ALTER TABLE EducationDetails
    ADD COLUMN TranscriptPath VARCHAR(255) NULL;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query)
            if cursor.description:
                data = cursor.fetchall()
                print(data)
                return data
    except Exception as e:
        print(f"Error executing SQL query: {e}")

#alter_table_files()