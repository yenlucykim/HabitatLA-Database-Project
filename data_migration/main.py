from migration import migrate_data

DRY_RUN = True

migrations = [
    {"file": "sample_data/volunteers.tsv", "table": "volunteer"},
    {"file": "sample_data/volunteer_availability.tsv", "table": "volunteer_availability"},
    {"file": "sample_data/roles.tsv", "table": "role", "duplicate_mode": "skip"},
    {"file": "sample_data/projects.tsv", "table": "project"},
    {"file": "sample_data/volunteer_assignment.tsv", "table": "volunteer_assignment"},
    {"file": "sample_data/service_reports.tsv", "table": "service_reports"},
    {"file": "sample_data/donors.tsv", "table": "donor"},
    {"file": "sample_data/donations.tsv", "table": "donation"},
    {"file": "sample_data/donation_projects.tsv", "table": "donation_project"},
]

def run_all_migrations():
    for migration in migrations:
        dry_run = migration.get("dry_run", DRY_RUN)
        duplicate_mode = migration.get("duplicate_mode", "skip")
        migrate_data(
            migration["file"],
            table=migration["table"],
            duplicate_mode=duplicate_mode,
            dry_run=dry_run
        )

if __name__ == "__main__":
    run_all_migrations()
