import csv
from utils.db_config import get_db_connection
import utils.logger as logger
from utils.logger import log, log_error
from insert import *
from insert import INSERT_FUNCTIONS

def clean_table_name(table):
    return " ".join(word.capitalize() for word in table.split("_"))

def log_migration_header(table, dry_run):
    header = f"\n=== {clean_table_name(table)} Migration (Dry Run: {dry_run}) ==="
    log(header, timestamp=False)
    log_error(header, timestamp=False)

def migrate_data(csv_file_path, table, duplicate_mode="skip", dry_run=False):
    insert_func = INSERT_FUNCTIONS.get(table)
    if insert_func is None:
        raise ValueError(f"Unsupported table type: {table}")

    success, fail, errors = 0, 0, []

    log_migration_header(table, dry_run)

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        with get_db_connection() as connection:
            for row in reader:
                result, msg = insert_func(connection, row, duplicate_mode, dry_run=dry_run)

                if result:
                    log(f"[OK] {msg}")
                    success += 1
                else:
                    log_error(f"{row} -> {msg}")
                    errors.append(f"{row} -> {msg}")
                    fail += 1

    summary = f"\n{clean_table_name(table)} Migration complete: {success} succeeded, {fail} failed."
    log(summary)
    print(summary)
    print(f"Logs written to '{logger.LOG_FILE}'")

    if errors:
        errors_message = f"Errors written to '{logger.ERROR_LOG}'"
        log(errors_message)
