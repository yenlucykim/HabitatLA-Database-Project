# Data Migration for HabitatLA Database

This folder contains Python scripts for importing, validating, nd inserting tabular data into the HabitatLA relational database. It supports structured data migration from TSV (tab-separated values) files into multiple related tables with options for dry-run simulation, validation, and duplicate handling.

---

## What’s Inside

```
data_migration/
├── main.py                      # Main script to run migrations
├── migration.py                 # Core logic for migration
├── insert/                      # Insert functions for each table
│   └── insert_volunteer.py      # Example: handles volunteer-specific validation & insertion
├── utils/
│   ├── db_config.py             # Securely manages DB connection using .env
│   ├── logger.py                # Logging system for migration summary & errors
│   ├── validation.py            # Reusable validators for email, phone, dates, etc.
├── sample_data/                 # Example TSV files for each table
│   └── volunteers.tsv           # Example: input file with both valid and invalid rows
├── logs/
│   ├── migration_logs.log       # Log of all successful/attempted operations
│   ├── migration_errors.log     # Log of detailed errors during migration
```

---

## How It Works

The main migration logic is managed through `migration.py` and launched through `main.py`. For each row in the TSV input:

1. Required fields are validated.
2. Email, phone, and date formats are checked.
3. Uniqueness is verified by querying the database based on the table's rules.
4. The row is either:
   - Inserted (if new),
   - Updated (if duplicate_mode is set to "update"), or
   - Skipped (if duplicate_mode is set to "skip").
5. All results are logged in either the success log or error log.


### Dry Run Mode

Set `dry_run=True` in `main.py` when calling `migrate_data()` to simulate the process without modifying the database. This is useful for testing large datasets, identifying validation issues, and fixing them without affecting the actual database.

---

## Duplicate Handling

Each insert function checks for duplicates **against the existing records in the database** using custom logic per table. For example:

- **Volunteers**: duplicates are checked via the `Email` field.
- **Donors**: duplicates are checked via the `Name + PhoneNumber` combination.
- **Donations**: duplicates are checked via the `DonorID + Date + Amount` combination.

You can set `duplicate_mode="skip"` to ignore duplicates or `duplicate_mode="update"` to update the existing record.

---
