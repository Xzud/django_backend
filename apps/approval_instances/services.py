from apps.approval_instances.models import ApprovalInstance
from apps.approval_workflows.models import ApprovalWorkflow
from apps.approval_steps.models import ApprovalStep
from apps.approval_tasks.models import ApprovalTask


def create_tasks_from_instance_workflow(instance: ApprovalInstance):
    steps = ApprovalStep.objects.filter(workflow_id=instance.workflow_id)

    tasks = []
    for step in steps:
        task = create_task_from_workflow_step(step.id, instance.id)

    # TODO incomplete, consider the information to be manually assigned on leave creation
    pass


def create_task_from_workflow_step(step_id, instance_id):
    task = ApprovalTask.objects.create(
        approval_instance_id=instance_id,
        approval_step_id=step_id,
    )
    # TODO incomplete, consider the information to be manually assigned on leave creation
    pass
