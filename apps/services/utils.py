from apps.employees.services import fetch_employees_count


def generateEmployeeID(employees_count=None):
    if not employees_count:
        employees_count = fetch_employees_count()

    return f"EMP{employees_count + 1:05d}"
