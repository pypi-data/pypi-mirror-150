from . import utils
from . import soup
from .errors import log_and_swallow_error, remove_nodes
from ..core.errors import OpenTrainingError
from ..core.project import Project
from ..core.person import Person
from ..core.task import Task
from ..core.group import Group
from ..core.errors import OpenTrainingError

from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import set_source_info
from docutils import nodes
from docutils.parsers.rst import directives 


from sphinx.util import logging
_logger = logging.getLogger(__name__)


def setup(app):
    app.add_directive('ot-personstats', _PersonStatsDirective)
    app.connect('doctree-resolved', _ev_doctree_resolved__expand_personstats_nodes)

def _ev_doctree_resolved__expand_personstats_nodes(app, doctree, docname):
    try:
        for n in doctree.traverse(_PersonStatsNode):
            project = app.soup().element_by_path(n.project, userdata=n)
            person = app.soup().element_by_path(n.person, userdata=n)

            table = nodes.table()
            tgroup = nodes.tgroup(cols=5)
            table += tgroup
            tgroup += nodes.colspec(colwidth=8)
            tgroup += nodes.colspec(colwidth=4)
            tgroup += nodes.colspec(colwidth=4)
            tgroup += nodes.colspec(colwidth=4)
            tgroup += nodes.colspec(colwidth=4)

            if 'thead':
                thead = nodes.thead()
                tgroup += thead
                row = nodes.row()
                thead += row

                entry = nodes.entry()
                row += entry
                entry += nodes.Text('Task')

                entry = nodes.entry()
                row += entry
                entry += nodes.Text('Implementation')

                entry = nodes.entry()
                row += entry
                entry += nodes.Text('Documentation')

                entry = nodes.entry()
                row += entry
                entry += nodes.Text('Integration')

                entry = nodes.entry()
                row += entry
                entry += nodes.Text('Task total')

            if 'tbody':
                tbody = nodes.tbody()
                tgroup += tbody

                for task in project.tasks_of_person(person):
                    row = nodes.row()
                    tbody += row

                    # link to task
                    entry = nodes.entry()
                    row += entry
                    p = nodes.paragraph()
                    entry += p
                    p += utils.make_reference(text=task.title, from_docname=docname, to_docname=task.docname, app=app)

                    # points scored from that task
                    implementation_score = task.person_implementation_points(person)
                    documentation_score = task.person_documentation_points(person)
                    integration_score = task.person_integration_points(person)
                    total_score = implementation_score + documentation_score + integration_score

                    entry = nodes.entry()
                    row += entry
                    entry += nodes.Text(str(implementation_score))

                    entry = nodes.entry()
                    row += entry
                    entry += nodes.Text(str(documentation_score))

                    entry = nodes.entry()
                    row += entry
                    entry += nodes.Text(str(integration_score))

                    entry = nodes.entry()
                    row += entry
                    entry += nodes.Text(str(total_score))

                row = nodes.row()
                tbody += row

                entry = nodes.entry()
                row += entry
                entry += nodes.Text('Total Score')

                entry = nodes.entry()
                row += entry

                entry = nodes.entry()
                row += entry

                entry = nodes.entry()
                row += entry

                entry = nodes.entry()
                row += entry
                *_, total_points = project.person_points(person)
                entry += nodes.Text(str(total_points))

            n.replace_self([table])
    except OpenTrainingError as e:
        remove_nodes(doctree, _PersonStatsNode)
        log_and_swallow_error(e, _logger)

class _PersonStatsNode(nodes.Element):
    def __init__(self, person, project):
        super().__init__(self)
        self.person = person
        self.project = project

class _PersonStatsDirective(SphinxDirective):
    required_arguments = 1   # person
    option_spec = {
        'project': utils.element_path,
    }

    def run(self):
        document = self.state.document

        person = utils.element_path(self.arguments[0].strip())
        project = self.options.get('project')

        if not project:
            return [document.reporter.warning('"project" option missing', line=self.lineno)]

        scores = _PersonStatsNode(
            person = person,
            project = project,
        )

        scores.document = document
        set_source_info(self, scores)

        return [scores]
