from apps.employees.models import Employee
import logging


class EmployeeService:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def fetch_employees(self):
        """Get all employees"""
        return Employee.objects.all()

    def fetch_active_employees(self):
        """Get only active employees"""
        return Employee.objects.filter(status="active")

    def fetch_employee_by_id(self, employee_id):
        """Get a single employee by id"""
        return Employee.objects.get(id=employee_id)

    def fetch_employees_by_department(self, department_id):
        """Get employees by their specific department"""
        return Employee.objects.filter(department_id=department_id)

    def fetch_employees_with_relations(self):
        """Fetch employees with their related user and department information"""
        return Employee.objects.select_related("user", "department").all()

    def fetch_employee_with_relations_by_id(self, employee_id):
        """Fetch specific employee by id with related user and department infromation"""
        return Employee.objects.select_related("user", "department").get(id=employee_id)
