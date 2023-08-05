from .element import Element
from .person import Person
from .task import Task
from .group import Group

from collections import defaultdict
import itertools


class Project(Element):

    def __init__(self, title, path, docname, userdata,                 
                 persons, tasks):
        super().__init__(title=title, path=path, docname=docname, userdata=userdata)
        self.persons = persons
        self.tasks = tasks

    def person_points(self, person):
        '''Given a person, return that person's score as

        :return: ``(implementation_points, documentation_points, integration_points, 
                 implementation_points + documentation_points + integration_points)``
        :rtype: ``(int, int, int, int)``

        '''

        assert self.resolved
        assert type(person) is Person
        assert person in self.persons, (person.path, self.persons)

        implementation_points = documentation_points = integration_points = 0

        for task in self.tasks:
            implementation_points += task.person_implementation_points(person)
            documentation_points += task.person_documentation_points(person)
            integration_points += task.person_integration_points(person)

        return implementation_points, documentation_points, integration_points, \
            implementation_points + documentation_points + integration_points

    def tasks_of_person(self, person):
        '''Given a person, return an iterable over that person's tasks'''

        assert self.resolved
        assert type(person) is Person
        assert person in self.persons

        her_tasks = set()
        for task in self.tasks:
            if person in (p for p,_ in itertools.chain(task.implementors, task.documenters, task.integrators)):
                her_tasks.add(task)
        return her_tasks

    def task_stats(self):
        '''Returns iterable over tuples of the form

        .. code-block:: python

           (task, 
              (implementation_percent,
               documentation_percent, 
               integration_percent, 
               total_percent,
              ),
             )

        Where

        * ``task`` is a :py:class:`task.Task` object``
        * ``implementation_percent``
        * ``documentation_percent``
        * ``integration_percent`` 
        * ``total_percent``

          These represent the completeness, in percent, of
          ``task``. (``total_percent`` is the sum of the other three.)

        See also :py:meth:`task.Task.stats()``

        '''

        for task in self.tasks:
            yield task, task.stats()

    def person_stats(self):
        '''Returns iterable over tuples of the form

        .. code-block:: python

           (person, 
              (implementation_points, 
               documentation_points, 
               integration_points, 
               total_points)
             )

        Where

        * ``person`` is a :py:class:`person.Person` object``
        * ``implementation_points``
        * ``documentation_points``
        * ``integration_points`` 
        * ``total_points``

          These represent the respective scores of ``person`` in the
          project. (``total_points`` is the sum of the other three.)

        '''

        for person in self.persons:
            yield person, self.person_points(person)

    def resolve(self, soup):
        persons = []
        tasks = []
        for person in self.persons:
            if type(person) is Person:
                persons.append(person)
            else:
                elem = soup.element_by_path(person, userdata=self.userdata)
                if isinstance(elem, Person):
                    persons.append(elem)
                elif isinstance(elem, Group):
                    persons.extend(elem.iter_recursive(cls=Person))

        for task in self.tasks:
            if type(task) is Task:
                tasks.append(task)
            else:
                elem = soup.element_by_path(task, userdata=self.userdata)
                if isinstance(elem, Task):
                    tasks.append(elem)
                elif isinstance(elem, Group):
                    tasks.extend(elem.iter_recursive(cls=Task))
        
        self.persons = persons
        self.tasks = tasks

        super().resolve(soup)
