from django.db import models

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType

# Create your models here.
# approval_instances
# ------------------
# id
# workflow_id
# request_content_type_id # Lead to different request object types (e.g. LeaveRequest, ExpenseRequest, etc.)
# request_object_id
# requester_id
# status (
# DRAFT
# IN_PROGRESS
# APPROVED
# REJECTED
# CANCELLED
# )
# current_step_id
# started_at
# completed_at
# created_at
# updated_at
