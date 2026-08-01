from django.db import models

# Create your models here.
# approval_steps
# --------------
# id
# workflow_id
# step_order
# name
#     (Human-readable label)
# approver_type (
#     DIRECT_SUPERVISOR
#     SUPERVISOR_LEVEL
#     ROLE
#     DEPARTMENT_ROLE
#     SPECIFIC_EMPLOYEE
# )
# supervisor_level
# department_id
# role_id
# employee_id
# is_required
# can_skip
# created_at
# updated_at
