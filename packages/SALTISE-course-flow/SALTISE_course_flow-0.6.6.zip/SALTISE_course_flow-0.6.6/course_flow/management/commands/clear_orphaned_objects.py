import json

from django.core.management.base import BaseCommand

from course_flow.models import (
    Activity,
    Column,
    Node,
    NodeLink,
    NodeWeek,
    Outcome,
    Project,
    Week,
    Workflow,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        # Deletes all the orphaned material. This can be produced when copying/importing is interrupted. Use with extreme caution.
        orphaned_nodes = Node.objects.filter(nodeweek=None)
        orphaned_nodes.delete()
        orphaned_nodelinks = NodeLink.objects.filter(source_node=None)
        orphaned_nodelinks.delete()
        orphaned_weeks = Week.objects.filter(weekworkflow=None)
        orphaned_weeks.delete()
        orphaned_columns = Column.objects.filter(columnworkflow=None)
        orphaned_columns.delete()
        orphaned_outcomes = Outcome.objects.filter(
            outcomeworkflow=None, parent_outcome_links=None
        )
        orphaned_outcomes.delete()
        orphaned_workflows = Workflow.objects.filter(
            workflowproject=None, is_strategy=False
        )
        orphaned_workflows.delete()
