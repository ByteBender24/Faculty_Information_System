from django.db import models, connection

'''
These functions should be run first time, to create tables and contraints, 
and make sure you comment these after so that no error shows up

If these functions not work, copy and paste these queries manually into MySQL workspace, and make sure you create these tables and contraints before working'''



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
    Experience INT,
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
    ConferenceID INT,
    FacultyID INT,
    ConferenceName VARCHAR(100),
    Location VARCHAR(50),
    DateAttended DATE,
    PRIMARY KEY (ConferenceID, FacultyID),
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

-- These should be done so that, there is a reference between departments and teachers present there, 
make sure you do it, based on the tables you have or remove them if not needed
-- Also use different INSERT INTO commands (other than that given below here)

CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY AUTO_INCREMENT,
    Location VARCHAR(50),
    DepartmentName VARCHAR(50) UNIQUE
);

-- Insert into Department table with random locations
INSERT INTO Department (DepartmentName, Location) VALUES ('Electrical Engineering', 'Building A');
INSERT INTO Department (DepartmentName, Location) VALUES ('Computer Science', 'Tech Center');
INSERT INTO Department (DepartmentName, Location) VALUES ('Biology', 'Science Building');
INSERT INTO Department (DepartmentName, Location) VALUES ('Chemistry', 'Lab Complex');
INSERT INTO Department (DepartmentName, Location) VALUES ('Mathematics', 'Mathematics Wing');
INSERT INTO Department (DepartmentName, Location) VALUES ('Physics', 'Physics Hall');
INSERT INTO Department (DepartmentName, Location) VALUES ('Psychology', 'Psychology Department');
INSERT INTO Department (DepartmentName, Location) VALUES ('Mechanical Engineering', 'Engineering Block');
INSERT INTO Department (DepartmentName, Location) VALUES ('Information Technology', 'IT Tower');
INSERT INTO Department (DepartmentName, Location) VALUES ('Computer Engineering', 'Engineering Block');
INSERT INTO Department (DepartmentName, Location) VALUES ('Civil Engineering', 'Civil Engineering Complex');

ALTER TABLE Teaching
ADD CONSTRAINT FK_Teaching_Department
FOREIGN KEY (DepartmentName) REFERENCES Department(DepartmentName);


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

# alter_table_files()


def triggers_functions_PLSQL():
    raw_sql_query = """
    DROP FUNCTION IF EXISTS generate_username;
DROP FUNCTION IF EXISTS generate_password;

-- Drop the triggers
DROP TRIGGER IF EXISTS faculty_insert_trigger;
DROP TRIGGER IF EXISTS faculty_delete_trigger;


DELIMITER //

CREATE FUNCTION generate_username(first_name VARCHAR(255), last_name VARCHAR(255))
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    DECLARE new_username VARCHAR(50);
    -- Logic to generate a unique username (customize as needed)
    SET new_username = LOWER(CONCAT(SUBSTRING(first_name, 1, 1), last_name, SUBSTRING(MD5(RAND()), 1, 4)));
    RETURN new_username;
END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION generate_password()
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE new_password VARCHAR(20);
    -- Logic to generate a random password (customize as needed)
    SET new_password = SUBSTRING(MD5(RAND()), 1, 8);
    RETURN new_password;
END //

DELIMITER ;


-- Create a trigger to generate credentials on faculty insertion
DELIMITER //
CREATE TRIGGER faculty_insert_trigger AFTER INSERT ON faculty
FOR EACH ROW
BEGIN
    DECLARE new_username VARCHAR(50);
    DECLARE new_password VARCHAR(20);
    -- Generate username and password
    SET new_username = generate_username(NEW.FirstName, NEW.LastName);
    SET new_password = generate_password();
    -- Insert into credentials table
    INSERT INTO credential (username, passwordHash, FacultyID)
    VALUES (new_username, new_password, NEW.FacultyID);
    END //
    DELIMITER ;

    -- Create a trigger to remove credentials on faculty deletion
DELIMITER //
CREATE TRIGGER faculty_delete_trigger AFTER DELETE ON faculty
FOR EACH ROW
BEGIN
    -- Delete from credentials table based on FacultyID
    DELETE FROM credential WHERE FacultyID = OLD.FacultyID;
END //
DELIMITER ;
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


# triggers_functions_PLSQL()
        
def example_run_plsql():
    raw_sql_query = """
    INSERT INTO faculty (FacultyID, FirstName, LastName, Gender) VALUES (2443, 'John', 'Doe', 'Male');

-- Check if a corresponding record is inserted into the credentials table
SELECT * FROM credential WHERE FacultyID = 2443;
-- Expected Output: Should display a record with the generated username and password for the inserted faculty

-- Clean up
DELETE FROM faculty WHERE FacultyID = 2443;

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


def check_phone_num():
    raw_sql_query = """
-- CHECK CONSTRAINT FOR PHONE NUMBER
ALTER TABLE Faculty
ADD CONSTRAINT chk_mobile_number
CHECK (CHAR_LENGTH(ContactNumber) = 10 AND ContactNumber NOT REGEXP '[^0-9]');

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

def current_status_sql():
    raw_sql_query = """
    -- Create FacultyStatus table
CREATE TABLE FacultyStatus (
    FacultyId INT,
    AreaOfSpecialization VARCHAR(255),
    Designation VARCHAR(255),
    DateOfJoining DATE,
    DateDesignatedAsAssociate DATE,
    DateDesignatedAsProfessor DATE,
    CurrentlyAssociate BOOLEAN,
    NatureOfAssociation VARCHAR(50),
    ContractType VARCHAR(50),
    DateOfLeaving DATE,
    -- Add other columns as needed

    -- Add foreign key constraint
    CONSTRAINT FK_FacultyId
    FOREIGN KEY (FacultyId)
    REFERENCES Faculty(FacultyId),

    CONSTRAINT PK_faculty_status PRIMARY KEY (FacultyID)
);

-- Add CHECK constraints
ALTER TABLE FacultyStatus
ADD CONSTRAINT CK_NatureOfAssociation
CHECK (NatureOfAssociation IN ('Full-Time', 'Part-Time', 'Adjunct'));

ALTER TABLE FacultyStatus
ADD CONSTRAINT CK_ContractType
CHECK (NatureOfAssociation <> 'Contract' OR ContractType IN ('Permanent', 'Contract'));

-- Add CHECK constraint for DateOfLeaving
ALTER TABLE FacultyStatus
ADD CONSTRAINT CK_DateOfLeaving
CHECK (
    (NatureOfAssociation <> 'No' AND DateOfLeaving IS NOT NULL)
    OR (NatureOfAssociation = 'No' AND DateOfLeaving IS NULL)
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


def profile_img_sql():
    raw_sql_query = """
    -- add profile photo url
    ALTER TABLE faculty
ADD COLUMN profile_img VARCHAR(255);

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
