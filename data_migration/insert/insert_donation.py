from utils.validators import is_valid_date

def insert_donation(connection, row, duplicate_mode="skip", dry_run=False):
    try:
        with connection.cursor() as cursor:
            #Validate required fields 
            required_fields=["DonorID", "Amount", "Date"]
            for field in required_fields:
                if not row.get(field) or row[field].strip() == "":
                    return False, f"Missing required field: {field}"
            
            # Validate DonorID is integer
            try: 
              donor_id = int(row["DonorID"])
            except ValueError:
                return False, f"Invalid DonorID: {row['DonorID']}"  

            # Validate amount > 0
            try:
                amount = float(row["Amount"])
                if amount <= 0:
                    return False, f"Donation amount must be > 0: {amount}"
            except ValueError:
                return False, f"Invalid amount: {row['Amount']}"

            # Date validation
            date_raw = row.get("Date", "").strip()
            converted_date = is_valid_date(date_raw)
            if converted_date is False:
                return False, f"Invalid date format: {date_raw}"
            date = converted_date

            # Check for duplicate (DonorID + Date + Amount)
            cursor.execute("""
                SELECT DonationID FROM Donation 
                WHERE DonorID = %s AND Date = %s AND Amount = %s
            """, (donor_id, date, amount))
            existing = cursor.fetchone()

            if existing:
                if duplicate_mode == "skip":
                    return False, f"Duplicate donation skipped: Donor {donor_id} on {date or 'NULL'}"
                elif duplicate_mode == "update":
                    return False, "Update not supported for donations (too ambiguous)"
                else:
                    return False, "Unknown duplicate_mode"

            if not dry_run:
                cursor.execute("""
                    INSERT INTO Donation (DonorID, Date, Amount)
                    VALUES (%s, %s, %s)
                """, (donor_id, date, amount))
                connection.commit()
            return True, f"Inserted donation: Donor {donor_id} on {date or 'NULL'}"
    except Exception as e:
        return False, str(e)
