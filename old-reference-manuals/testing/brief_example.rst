A brief example
---------------

.. admonition:: description

    Just so that you know what we're talking about

Try to find the bug in the following piece of code:

::

    class Employee(object):
        def __init__(self, name, position, employee_no=None):
            self.name = name
            self.position = position
            self.employee_no = employee_no

    salaries = {0: 12000,
                1: 4000,
                2: 8000,
                3: 4000}

    def print_salary(employee):
        if employee.employee_no:
            salary = salaries.get(employee.employee_no, 0)
            print "You make EUR %s." % salary
        else:
            print "You're not an employee currently."

Found it yet? Did you have to spend more than a few seconds thinking
about it? Any developer could have written that code and not seen the
problem. Furthermore, the bug is an edge case that you may not have
tested using manual/through-the-web testing.

Let us write a test (actually, a doc/unit test) for this code. Don’t
worry too much about how this is set up and executed just yet.

::

    Employee w/o an employee number is ignored:

      >>> print_salary(Employee('Adam', 'Developer'))
      You're not an employee currently

    Employee w/o a known employee number earns nothing:

      >>> print_salary(Employee('Berta', 'Designer', 100))
      You make EUR 0.

    Employee w/ a valid employee number is found properly:

      >>> print_salary(Employee('Chris', 'CTO', 2))
      You make EUR 8000.

    Zero is a valid employee number:

      >>> print_salary(Employee('Devon', 'CEO', 0))
      You make EUR 12000

As it happens, the last test would fail. It would print You are not an
employee currently., unless we fixed the code:

::

    class Employee(object):
        def __init__(self, name, position, employee_no=None):
            self.name = name
            self.position = position
            self.employee_no = employee_no

    salaries = {0: 12000,
                1: 4000,
                2: 8000,
                3: 4000}

    def print_salary(employee):
        if employee.employee_no is not None:
            salary = salaries.get(employee.employee_no, 0)
            print "You make EUR %s." % salary
        else:
            print "You're not an employee currently."

The moral of the story?

* you rarely catch problems like these with manual testing
* put the time you waste catching silly bugs and typos into writing tests
* with decent test coverage, you end up saving lots of time when you refactor