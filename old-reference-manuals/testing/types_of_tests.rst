Types of tests
--------------

.. admonition:: description

    Some terminology you should be familiar with

Broadly speaking, there are four main types of tests:

Unit tests
    These are written from the programmer’s perspective. A unit test
    should test a single method or function in isolation, to ensure that
    it behaves correctly. For example, testing that a given calculation
    is performed correctly given a variety of input is a good unit test
    for that one method.
Integration tests
    Whereas unit tests try to remove or abstract away as many
    dependencies as possible to ensure that they are truly only
    concerned with the method under test, integration tests exercise the
    integration points between a method or component and the other
    components it relies on. For example, testing that a method performs
    some calculation and then correctly stores the result in the ZODB is
    an integration test in that it tests the integration between that
    component and the ZODB.
Functional tests
    A functional test is typically demonstrating a use case, exercising
    a “vertical” of functionality. For example, testing that filling in
    a form and clicking “Save” then makes the resulting object available
    for future use, is a functional test for the use case of using that
    form to create content objects.
System tests
    These are written from the user’s perspective, and treat the system
    as a black box. A system test may be simulating a user interacting
    with the system according to expected usage patterns. By their
    nature, they are typically less systematic than the other types of
    tests.

Furthermore, functional tests may be **white box**, in which case they
can make assertions about things like the underlying data storage (but
only if this is specified clearly; implementation details should never
affect functional tests). Such tests are also called **functional
integration tests** (you can see where the lines start to blur, but
don’t worry too much about the naming). Alternatively, functional tests
can be **black box** in which case they only perceive the system from
the point of view of an actor (usually the end user) and make assertions
only on what is presented in the (user) interface to that actor. Such
tests, also known as **acceptance tests** would not make assumptions
about the underlying architecture at all.

Tests and documentation
~~~~~~~~~~~~~~~~~~~~~~~

In a post to the Zope 3 mailing list, Jim Fulton explains the importance
of tests and documentation, and how they go hand-in-hand:

       One of the important things about this is that most doctests
       should be written as documentation.  When you write new software
       components and you need to write tests for the main functionality
       of your software you need to:
       - Get your head into the mode of writing documentation. This is very very very important.
       - You need to document how to use the software.  Include  examples, which are tests

We will learn more about doctests, and how they are used for unit testing and functional
testing later. The important thing to note is that good tests often serve as documentation
describing how your component is supposed to be used. Thinking about the story they tell is
just as important as thinking about the number of input and output states they cover.