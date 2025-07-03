from utils.validators import is_valid_email, is_valid_phone

def insert_volunteer(connection, row, duplicate_mode="skip", dry_run=False):
    try:
        with connection.cursor() as cursor:
            # Validate required fields
            required_fields = ["Email", "Name"]
            for field in required_fields:
                if not row.get(field) or row[field].strip() == "":
                    return False, f"Missing required field: {field}"

            # Validate email format
            if not is_valid_email(row["Email"]):
                return False, f"Invalid email format: {row['Email']}"

            # Validate phone if provided
            PhoneNumber = row.get("PhoneNumber", "").strip()
            if PhoneNumber and not is_valid_phone(PhoneNumber):
                return False, f"Invalid phone number format: {PhoneNumber}"

            # Check for duplicates
            cursor.execute("SELECT VolunteerID FROM Volunteer WHERE Email = %s", (row["Email"],))
            existing = cursor.fetchone()

            if existing:
                if duplicate_mode == "skip":
                    return False, f"Duplicate email skipped: {row['Email']}"
                elif duplicate_mode == "update":
                    if not dry_run:
                        cursor.execute("""
                            UPDATE Volunteer
                            SET Name = %s, Location = %s, PhoneNumber = %s
                            WHERE Email = %s
                        """, (
                            row["Name"],
                            row.get("Location", None),
                            PhoneNumber,
                            row["Email"]
                        ))
                        connection.commit()
                    return True, f"Updated: {row['Email']}"
                else:
                    return False, f"Unknown duplicate_mode: {duplicate_mode}"

            # Insert
            if not dry_run:
                cursor.execute("""
                    INSERT INTO Volunteer (Email, Name, Location, PhoneNumber)
                    VALUES (%s, %s, %s, %s)
                """, (
                    row["Email"],
                    row["Name"],
                    row.get("Location", None),
                    PhoneNumber
                ))
                connection.commit()
            return True, f"Inserted: {row['Email']}"
    except Exception as e:
        return False, str(e)
