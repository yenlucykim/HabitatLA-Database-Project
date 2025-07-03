def insert_service_report(connection, row, duplicate_mode="skip", dry_run=False):
    try:
        with connection.cursor() as cursor:
            # Validate required fields
            if not row.get("AssignmentID") or not row.get("Hours"):
                return False, "Missing AssignmentID or Hours"

            try:
                assignment_id = int(row["AssignmentID"])
            except ValueError:
                return False, f"Invalid AssignmentID (not an integer): {row['AssignmentID']}"

            try:
                hours = int(row["Hours"])
                if hours <= 0:
                    return False, f"Invalid Hours (must be > 0): {hours}"
            except ValueError:
                return False, f"Invalid Hours (not an integer): {row['Hours']}"

            # Check for duplicate: AssignmentID + Hours
            cursor.execute("""
                SELECT ReportID FROM ServiceReports
                WHERE AssignmentID = %s AND Hours = %s
            """, (assignment_id, hours))
            existing = cursor.fetchone()

            if existing:
                if duplicate_mode == "skip":
                    return False, f"Duplicate service report skipped for AssignmentID {assignment_id}"
                elif duplicate_mode == "update":
                    return False, "Update not supported for service reports"
                else:
                    return False, "Unknown duplicate_mode"

            # Foreign key check on validity of AssignmentID
            cursor.execute("SELECT AssignmentID FROM VolunteerAssignment WHERE AssignmentID = %s", (assignment_id,))
            if not cursor.fetchone():
                return False, f"AssignmentID {assignment_id} does not exist in VolunteerAssignment"

            # Insert
            if not dry_run:
                cursor.execute("""
                    INSERT INTO ServiceReports (AssignmentID, Hours)
                    VALUES (%s, %s)
                """, (assignment_id, hours))
                connection.commit()

            return True, f"Inserted service report for AssignmentID {assignment_id}"
    except Exception as e:
        return False, str(e)
