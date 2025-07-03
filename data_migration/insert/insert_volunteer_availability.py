def insert_volunteer_availability(connection, row, duplicate_mode="update", dry_run=False):
    try:
        with connection.cursor() as cursor:
            # Validate required fields
            required_fields = ["VolunteerID", "Day", "TimeSlot"]
            for field in required_fields:
                if not row.get(field) or row[field].strip() == "":
                    return False, f"Missing required field: {field}"

            # Validate enums
            valid_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}
            valid_slots = {'Morning', 'Afternoon'}

            day = row["Day"].strip()
            slot = row["TimeSlot"].strip()

            if day not in valid_days:
                return False, f"Invalid Day: {day}"
            if slot not in valid_slots:
                return False, f"Invalid TimeSlot: {slot}"

            # Validate VolunteerID is integer and exists
            try:
                volunteer_id = int(row["VolunteerID"])
            except ValueError:
                return False, f"VolunteerID must be an integer: {row['VolunteerID']}"

            cursor.execute("SELECT VolunteerID FROM Volunteer WHERE VolunteerID = %s", (volunteer_id,))
            if not cursor.fetchone():
                return False, f"VolunteerID does not exist: {volunteer_id}"

            # Check for duplicates
            cursor.execute("""
                SELECT AvailabilityID FROM VolunteerAvailability 
                WHERE VolunteerID = %s AND Day = %s AND TimeSlot = %s
            """, (volunteer_id, day, slot))
            existing = cursor.fetchone()

            if existing:
                if duplicate_mode == "skip":
                    return False, f"Duplicate availability skipped for Volunteer {volunteer_id}, {day}, {slot}"
                elif duplicate_mode == "update":
                    return False, "Update not supported for availability"
                else:
                    return False, "Unknown duplicate_mode"

            # Insert
            if not dry_run:
                cursor.execute("""
                    INSERT INTO VolunteerAvailability (VolunteerID, Day, TimeSlot)
                    VALUES (%s, %s, %s)
                """, (volunteer_id, day, slot))
                connection.commit()

            return True, f"Inserted availability for Volunteer {volunteer_id}: {day} {slot}"
    except Exception as e:
        return False, str(e)
