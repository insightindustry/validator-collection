**********
Glossary
**********

.. glossary::

  Checker
    A function which takes an input value and indicates (``True``/``False``)
    whether it contains what you expect. Will always return a Boolean value,
    and will not raise an exception on failure.

  Validator
    A function which takes an input value and ensures that it is what (the type
    or contents) you expect it to be. Will return the value or
    :obj:`None <python:None>` depending on the arguments you pass to it, and
    will raise an exception if validation fails.
