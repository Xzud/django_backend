from django.db import models

# Create your models here.

# approval_tasks
# ---------------
# id
# approval_instance_id
# approval_step_id
# approver_id
# status (
# WAITING
# PENDING
# APPROVED
# REJECTED
# SKIPPED
# )
# sequence # maybe not needed?
# assigned_at
# acted_at
# remarks
# delegated_from_id # When current assigner is unavailable, approval is delegated
# created_at
# updated_at
