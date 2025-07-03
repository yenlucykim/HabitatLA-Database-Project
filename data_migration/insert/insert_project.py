from utils.validators import is_valid_date,is_date_order_valid

def insert_project(connection, row, duplicate_mode="skip", dry_run=False):
    try:
        with connection.cursor() as cursor:
            if not row.get("Name") or not row.get("Location"):
                return False, "Missing required field: Name or Location"

            # Optional date validation
            start_str = row.get("StartDate", "").strip()
            end_str = row.get("EndDate", "").strip()

            start_date = is_valid_date(start_str)
            end_date = is_valid_date(end_str)

            if start_date is False:
                return False, f"Invalid StartDate format: {start_str}"
            if end_date is False:
                return False, f"Invalid EndDate format: {end_str}"

            # Check date order
            if not is_date_order_valid(start_date, end_date):
                return False, f"EndDate {end_str} is earlier than StartDate {start_str}"

            # Check if project with same name exists
            cursor.execute("SELECT ProjectID FROM Project WHERE Name = %s", (row["Name"],))
            existing = cursor.fetchone()

            if existing:
                if duplicate_mode == "skip":
                    return False, f"Duplicate skipped: {row['Name']}"
                elif duplicate_mode == "update":
                    if not dry_run:
                        cursor.execute("""
                            UPDATE Project
                            SET Location = %s, Description = %s, StartDate = %s, EndDate = %s
                            WHERE Name = %s
                        """, (
                            row["Location"],
                            row.get("Description", None),
                            start_date if start_date else None,
                            end_date if end_date else None,
                            row["Name"]
                        ))
                        connection.commit()
                    return True, f"Updated: {row['Name']}"
                else:
                    return False, "Unknown duplicate_mode"

            # Insert
            if not dry_run:
                cursor.execute("""
                    INSERT INTO Project (Name, Location, Description, StartDate, EndDate)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    row["Name"],
                    row["Location"],
                    row.get("Description", None),
                    start_date if start_date else None,
                    end_date if end_date else None,
                ))
                connection.commit()
            return True, f"Inserted: {row['Name']}"
    except Exception as e:
        return False, str(e)
