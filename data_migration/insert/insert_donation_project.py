def insert_donation_project(connection, row, duplicate_mode="skip", dry_run=False):
    try:
        with connection.cursor() as cursor:
            # Validate required fields
            if not row.get("DonationID") or not row.get("ProjectID") or not row.get("AllocationAmount"):
                return False, "Missing required field(s): DonationID, ProjectID, or AllocationAmount"

            try:
                donation_id = int(row["DonationID"])
                project_id = int(row["ProjectID"])
            except ValueError:
                return False, "Invalid DonationID or ProjectID (must be integers)"

            try:
                amount = float(row["AllocationAmount"])
                if amount <= 0:
                    return False, f"Invalid AllocationAmount (must be > 0): {amount}"
            except ValueError:
                return False, f"Invalid AllocationAmount: {row['AllocationAmount']}"

            # Foreign key checks
            cursor.execute("SELECT DonationID FROM Donation WHERE DonationID = %s", (donation_id,))
            if not cursor.fetchone():
                return False, f"DonationID {donation_id} does not exist"

            cursor.execute("SELECT ProjectID FROM Project WHERE ProjectID = %s", (project_id,))
            if not cursor.fetchone():
                return False, f"ProjectID {project_id} does not exist"

            # Check for duplicates: DonationID + ProjectID
            cursor.execute("""
                SELECT DonationProjectID FROM DonationProject
                WHERE DonationID = %s AND ProjectID = %s
            """, (donation_id, project_id))
            if cursor.fetchone():
                if duplicate_mode == "skip":
                    return False, f"Duplicate DonationProject skipped for Donation {donation_id}, Project {project_id}"
                elif duplicate_mode == "update":
                    return False, "Update not supported for DonationProject"
                else:
                    return False, "Unknown duplicate_mode"

            # Insert
            if not dry_run:
                cursor.execute("""
                    INSERT INTO DonationProject (DonationID, ProjectID, AllocationAmount, Purpose)
                    VALUES (%s, %s, %s, %s)
                """, (donation_id, project_id, amount, row.get("Purpose")))
                connection.commit()

            return True, f"Inserted DonationProject (DonationID={donation_id}, ProjectID={project_id})"
    except Exception as e:
        return False, str(e)
