# Habitat for Humanity LA - Volunteer, Project, and Donation Management Database

This project is a relational database system built for **Habitat for Humanity Los Angeles**, a nonprofit focused on building and repairing homes for low-income families. The system centralizes operations like volunteer registration, project tracking, and donation management into a single, structured solution.

The purpose of this database is to enable smarter resource planning, improved transparency, and more efficient operations.

---

## Technologies Used

- **MySQL** – Schema design, constraints, and relational logic
- **Python** – For CSV/TSV-to-MySQL data migrations

---

## What's Inside

```
HabitatLA-Database-Project/
├── docs/ # ER diagram, final write-ups
├── sql/ # DDL, DML, and test query scripts
├── data_migration/ # Python scripts to import, validate, and insert data
├── demo/ # Quick demos of data migration pipeline and sample queries
├── README.md
```

---

## Schema Overview

- `Volunteer` — Stores personal details
- `VolunteerAvailability` — Tracks availability by day and timeslot
- `Role` — Builder, Planner, Team Leader, etc.
- `Project` — Project details like location and timeline
- `VolunteerAssignment` — Assigns volunteers to projects
- `ServiceReports` — Hours volunteered
- `Donor` — Stores donor information
- `Donation` — Records amount, date, and donor
- `DonationProject` — Links donations to projects and purpose

View diagram: [ER_Diagram](docs/diagrams/ER_diagram.png)

---

## How to Run

1. Clone or download the repository.

2. Open MySQL Workbench or any SQL client and run `sql/create_schema.sql`

3. Configure environment variable: Copy `.env.example` to `.env` and fill in your database credentials.

4. Run the data migration pipeline: `python data_migration/main.py`

   - This will populate all tables using the sample data in `/sample_data/`
   - Log summaries and errors will be written to `/logs/`

5. Query the database to verify the results and demonstrate use cases: Run `sql/test_queries.sql`

---

## Data Migration

See [Data Migration](data_migration/) for a fully functional migration pipeline built in Python. It reads .csv or .tsv files, validates and cleans data, handles duplicate entries based on existing database records, and inserts valid data into the MySQL database.

Key features include:

- Field-level validation (e.g., email, phone number, date formats, required fields)
- Duplicate handling with customizable logic (skip, update, etc.)
- Dry-run mode to simulate insertions without modifying the database
- Detailed logging for successful migrations and error tracking

---

## Future Enhancements

- Admin UI for non-technical users
- Build web-based front-end interface for CRUD operations
- Automate financial summaries or other reports
- Add dashboards or visual summaries [In Progress]

---

## Author

**Yea Yen Kim**  
[LinkedIn](https://www.linkedin.com/in/yea-yen-kim/) | [Portfolio](https://yenlucykim.github.io/Portfolio.github.io/)

---
