def insert_volunteer_assignment(connection, row, duplicate_mode="skip", dry_run=False):
    try:
        with connection.cursor() as cursor:
            required_fields = ["VolunteerID", "ProjectID", "RoleID", "AvailabilityID"]
            for field in required_fields:
                if not row.get(field) or row[field].strip() == "":
                    return False, f"Missing required field: {field}"

            # Parse integers
            try:
                volunteer_id = int(row["VolunteerID"])
                project_id = int(row["ProjectID"])
                role_id = int(row["RoleID"])
                availability_id = int(row["AvailabilityID"])
            except ValueError:
                return False, f"Invalid numeric value in row: {row}"

            # Validate foreign key existence
            for table, field, value in [
                ("Volunteer", "VolunteerID", volunteer_id),
                ("Project", "ProjectID", project_id),
                ("Role", "RoleID", role_id),
                ("VolunteerAvailability", "AvailabilityID", availability_id),
            ]:
                cursor.execute(f"SELECT 1 FROM {table} WHERE {field} = %s", (value,))
                if not cursor.fetchone():
                    return False, f"{field} {value} does not exist in table {table}"

            # Check if this combo already exists
            cursor.execute("""
                SELECT AssignmentID FROM VolunteerAssignment
                WHERE VolunteerID = %s AND ProjectID = %s AND RoleID = %s AND AvailabilityID = %s
            """, (volunteer_id, project_id, role_id, availability_id))
            existing = cursor.fetchone()

            if existing:
                if duplicate_mode == "skip":
                    return False, f"Duplicate assignment skipped for Volunteer {volunteer_id}"
                elif duplicate_mode == "update":
                    return False, "Update not supported for VolunteerAssignment (composite uniqueness)"
                else:
                    return False, "Unknown duplicate_mode"

            # Insert
            if not dry_run:
                cursor.execute("""
                    INSERT INTO VolunteerAssignment (VolunteerID, ProjectID, RoleID, AvailabilityID)
                    VALUES (%s, %s, %s, %s)
                """, (volunteer_id, project_id, role_id, availability_id))
                connection.commit()
            return True, f"Inserted VolunteerAssignment for Volunteer {volunteer_id}"

    except Exception as e:
        return False, str(e)