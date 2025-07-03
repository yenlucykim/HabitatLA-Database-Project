def insert_role(connection, row, duplicate_mode="skip", dry_run=False):
    try:
        with connection.cursor() as cursor:
            role_name = row.get("RoleName", "").strip()

            # Validate
            if not role_name:
                return False, "Missing required field: RoleName"

            # Check for duplicate
            cursor.execute("SELECT RoleID FROM Role WHERE RoleName = %s", (role_name,))
            existing = cursor.fetchone()

            if existing:
                if duplicate_mode == "skip":
                    return False, f"Duplicate role skipped: {role_name}"
                elif duplicate_mode == "update":
                    return False, "Update not supported for roles"
                else:
                    return False, "Unknown duplicate_mode"

            # Insert
            if not dry_run:
                cursor.execute("INSERT INTO Role (RoleName) VALUES (%s)", (role_name,))
                connection.commit()

            return True, f"Inserted role: {role_name}"
    except Exception as e:
        return False, str(e)
