from utils.validators import is_valid_phone

def insert_donor(connection, row, duplicate_mode="skip", dry_run=False):
    try:
        with connection.cursor() as cursor:
            if not row.get("Name") or row["Name"].strip() == "":
                return False, "Missing required field: Name"

            # Validate phone if provided
            PhoneNumber = row.get("PhoneNumber", "").strip()
            if PhoneNumber and not is_valid_phone(PhoneNumber):
                return False, f"Invalid phone number format: {PhoneNumber}"

            # Check if donor exists (use name + optional phone number)
            cursor.execute("SELECT DonorID FROM Donor WHERE Name = %s", (row["Name"],))
            existing = cursor.fetchone()

            if existing:
                if duplicate_mode == "skip":
                    return False, f"Duplicate skipped: {row['Name']}"
                elif duplicate_mode == "update":
                    if not dry_run:
                        cursor.execute("UPDATE Donor SET PhoneNumber = %s WHERE Name = %s",
                                       (row.get("PhoneNumber", None), row["Name"]))
                        connection.commit()
                    return True, f"Updated: {row['Name']}"
                else:
                    return False, "Unknown duplicate_mode"

            if not dry_run:
                cursor.execute("INSERT INTO Donor (Name, PhoneNumber) VALUES (%s, %s)",
                               (row["Name"], row.get("PhoneNumber", None)))
                connection.commit()
            return True, f"Inserted: {row['Name']}"
    except Exception as e:
        return False, str(e)
