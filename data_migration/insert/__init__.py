from .insert_volunteer import insert_volunteer
from .insert_project import insert_project
from .insert_donor import insert_donor
from .insert_donation import insert_donation
from .insert_role import insert_role
from .insert_volunteer_availability import insert_volunteer_availability
from .insert_volunteer_assignment import insert_volunteer_assignment
from .insert_service_report import insert_service_report
from .insert_donation_project import insert_donation_project

__all__ = [
    "insert_volunteer",
    "insert_project",
    "insert_donor",
    "insert_donation",
    "insert_role",
    "insert_volunteer_availability",
    "insert_volunteer_assignment",
    "insert_service_report",
    "insert_donation_project",
]

# Central dictionary mapping table names to insert functions
INSERT_FUNCTIONS = {
    "volunteer": insert_volunteer,
    "project": insert_project,
    "donor": insert_donor,
    "donation": insert_donation,
    "role": insert_role,
    "volunteer_availability": insert_volunteer_availability,
    "volunteer_assignment": insert_volunteer_assignment,
    "service_reports": insert_service_report,
    "donation_project": insert_donation_project,
}
