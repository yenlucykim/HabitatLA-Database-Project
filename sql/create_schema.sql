CREATE DATABASE IF NOT EXISTS HabitatLA;
USE HabitatLA;

CREATE TABLE Volunteer (
    VolunteerID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Name VARCHAR(50) NOT NULL,
    Location VARCHAR(100),
    PhoneNumber VARCHAR(15)
);

CREATE TABLE VolunteerAvailability (
    AvailabilityID INT AUTO_INCREMENT PRIMARY KEY,
    VolunteerID INT NOT NULL,
    Day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday') NOT NULL,
    TimeSlot ENUM('Morning', 'Afternoon') NOT NULL,
    UNIQUE(VolunteerID, Day, TimeSlot),
    FOREIGN KEY (VolunteerID) REFERENCES Volunteer(VolunteerID)
);

CREATE TABLE Role (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL
);

CREATE TABLE Project (
    ProjectID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Description TEXT,
    StartDate DATE,
    EndDate DATE
);

CREATE TABLE VolunteerAssignment (
    AssignmentID INT AUTO_INCREMENT PRIMARY KEY,
    ProjectID INT NOT NULL,
    VolunteerID INT NOT NULL,
    RoleID INT NOT NULL,
    AvailabilityID INT NOT NULL,
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID),
    FOREIGN KEY (VolunteerID) REFERENCES Volunteer(VolunteerID),
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID),
    FOREIGN KEY (AvailabilityID) REFERENCES VolunteerAvailability(AvailabilityID)
);

CREATE TABLE ServiceReports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    Hours INT NOT NULL,
    AssignmentID INT NOT NULL,
    FOREIGN KEY (AssignmentID) REFERENCES VolunteerAssignment(AssignmentID)
);

CREATE TABLE Donor (
    DonorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    PhoneNumber VARCHAR(15)
);

CREATE TABLE Donation (
    DonationID INT AUTO_INCREMENT PRIMARY KEY,
    DonorID INT NOT NULL,
    Date DATE NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL CHECK (Amount > 0),
    FOREIGN KEY (DonorID) REFERENCES Donor(DonorID)
);

CREATE TABLE DonationProject (
    DonationProjectID INT AUTO_INCREMENT PRIMARY KEY,
    DonationID INT NOT NULL,
    ProjectID INT NOT NULL,
    AllocationAmount DECIMAL(10 , 2 ) NOT NULL CHECK (AllocationAmount > 0),
    Purpose VARCHAR(255),
    FOREIGN KEY (DonationID) REFERENCES Donation(DonationID),
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID)
);


SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM ServiceReports;
DELETE FROM VolunteerAssignment;
DELETE FROM VolunteerAvailability;
DELETE FROM DonationProject;
DELETE FROM Donation;
DELETE FROM Donor;
DELETE FROM Volunteer;
DELETE FROM Project;
DELETE FROM Role;


ALTER TABLE ServiceReports AUTO_INCREMENT = 1;
ALTER TABLE VolunteerAssignment AUTO_INCREMENT = 1;
ALTER TABLE VolunteerAvailability AUTO_INCREMENT = 1;
ALTER TABLE DonationProject AUTO_INCREMENT = 1;
ALTER TABLE Donation AUTO_INCREMENT = 1;
ALTER TABLE Donor AUTO_INCREMENT = 1;
ALTER TABLE Volunteer AUTO_INCREMENT = 1;
ALTER TABLE Project AUTO_INCREMENT = 1;
ALTER TABLE Role AUTO_INCREMENT = 1;

SET FOREIGN_KEY_CHECKS = 1;

SELECT * FROM volunteeravailability;

