USE HabitatLA;

-- Query 1: List all volunteers and their availability
SELECT v.Name, v.Email, v.Location, va.Day, va.TimeSlot
FROM Volunteer v
JOIN VolunteerAvailability va ON v.VolunteerID = va.VolunteerID
ORDER BY v.Name;

-- Query 2: List all projects and assigned volunteers
SELECT p.Name AS ProjectName, v.Name AS VolunteerName, r.RoleName
FROM Project p
JOIN VolunteerAssignment va ON p.ProjectID = va.ProjectID
JOIN Volunteer v ON va.VolunteerID = v.VolunteerID
JOIN Role r ON va.RoleID = r.RoleID
ORDER BY p.Name;

-- Query 3: Total donation amount allocated to each project
SELECT p.Name AS ProjectName, SUM(dp.AllocationAmount) AS TotalAllocated
FROM Project p
JOIN DonationProject dp ON p.ProjectID = dp.ProjectID
GROUP BY p.Name;

-- Query 4: Hours worked by volunteers on a project
SELECT p.Name AS ProjectName, v.Name AS VolunteerName, sr.Hours
FROM ServiceReports sr
JOIN VolunteerAssignment va ON sr.AssignmentID = va.AssignmentID
JOIN Volunteer v ON va.VolunteerID = v.VolunteerID
JOIN Project p ON va.ProjectID = p.ProjectID;

-- Query 5: Generate financial report showing donations and remaining balances
SELECT d.DonationID, do.Name, d.Amount, SUM(dp.AllocationAmount) AS Allocated, 
       (d.Amount - SUM(dp.AllocationAmount)) AS RemainingBalance
FROM Donation d
JOIN Donor do ON d.DonorID = do.DonorID
LEFT JOIN DonationProject dp ON d.DonationID = dp.DonationID
GROUP BY d.DonationID, d.Amount;

-- Query 6: List volunteers with total hours worked (across all projects)
SELECT v.Name, v.Email, SUM(sr.Hours) AS TotalHours
FROM Volunteer v
JOIN VolunteerAssignment va ON v.VolunteerID = va.VolunteerID
JOIN ServiceReports sr ON va.AssignmentID = sr.AssignmentID
GROUP BY v.VolunteerID
ORDER BY TotalHours DESC;

-- Query 7: List projects that currently have no volunteers assigned
SELECT p.Name, p.Location
FROM Project p
LEFT JOIN VolunteerAssignment va ON p.ProjectID = va.ProjectID
WHERE va.AssignmentID IS NULL;

-- Query 8: List donors who have donated more than a certain amount (e.g., $1000 total)
SELECT do.Name, SUM(d.Amount) AS TotalDonated
FROM Donor do
JOIN Donation d ON do.DonorID = d.DonorID
GROUP BY do.DonorID
HAVING TotalDonated > 1000;

-- Query 9: Show detailed donation allocations for a given donor (example: DonorID = 1)
SELECT d.DonationID, p.Name AS ProjectName, dp.AllocationAmount, dp.Purpose
FROM Donation d
JOIN DonationProject dp ON d.DonationID = dp.DonationID
JOIN Project p ON dp.ProjectID = p.ProjectID
WHERE d.DonorID = 1;

-- Query 10: Volunteers available on a specific day and time (e.g., Monday Morning)
SELECT v.Name, v.Email, v.Location
FROM Volunteer v
JOIN VolunteerAvailability va ON v.VolunteerID = va.VolunteerID
WHERE va.Day = 'Monday' AND va.TimeSlot = 'Morning';

-- Query 11: Average volunteer hours per project
SELECT p.Name AS ProjectName, AVG(sr.Hours) AS AvgHoursPerVolunteer
FROM Project p
JOIN VolunteerAssignment va ON p.ProjectID = va.ProjectID
JOIN ServiceReports sr ON va.AssignmentID = sr.AssignmentID
GROUP BY p.ProjectID
ORDER BY AvgHoursPerVolunteer DESC;

-- Query 12: Monthly donation totals over the last year
SELECT DATE_FORMAT(d.Date, '%Y-%m') AS YearMonth, SUM(d.Amount) AS TotalDonations
FROM Donation d
WHERE d.Date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY YearMonth
ORDER BY YearMonth;

-- Query 13: Top 3 roles with the most volunteer hours logged
SELECT r.RoleName, SUM(sr.Hours) AS TotalHours
FROM Role r
JOIN VolunteerAssignment va ON r.RoleID = va.RoleID
JOIN ServiceReports sr ON va.AssignmentID = sr.AssignmentID
GROUP BY r.RoleID
ORDER BY TotalHours DESC
LIMIT 3;

-- Query 14: Projects with the highest funding allocated vs hours worked ratio
SELECT p.Name AS ProjectName, 
       SUM(dp.AllocationAmount) AS TotalFunding,
       COALESCE(SUM(sr.Hours), 0) AS TotalHours,
       CASE WHEN SUM(sr.Hours) > 0 THEN SUM(dp.AllocationAmount)/SUM(sr.Hours)
            ELSE NULL
       END AS FundingPerHour
FROM Project p
LEFT JOIN DonationProject dp ON p.ProjectID = dp.ProjectID
LEFT JOIN VolunteerAssignment va ON p.ProjectID = va.ProjectID
LEFT JOIN ServiceReports sr ON va.AssignmentID = sr.AssignmentID
GROUP BY p.ProjectID
ORDER BY FundingPerHour DESC;

-- Query 15: Volunteer retention — number of projects each volunteer has participated in
SELECT v.Name, COUNT(DISTINCT va.ProjectID) AS ProjectsParticipated
FROM Volunteer v
JOIN VolunteerAssignment va ON v.VolunteerID = va.VolunteerID
GROUP BY v.VolunteerID
ORDER BY ProjectsParticipated DESC;

-- Query 16: Donation purpose breakdown — total amount allocated per purpose
SELECT Purpose, SUM(AllocationAmount) AS TotalAllocated
FROM DonationProject
GROUP BY Purpose
ORDER BY TotalAllocated DESC;
