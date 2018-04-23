-----------

Release 1.1.0 (in development)
==========================================

Features Added
----------------

* Added ``validators.domain()`` and ``checkers.is_domain()`` support with unit tests.
* #8: Added more verbose exceptions while retaining backwards-compatability with standard
  library exceptions.
* #6: Made it possible to disable validators by adding the validator name to the
  ``VALIDATORS_DISABLED`` environment variable.
* #6: Made it possible to disable checkers by adding the checker name to the
  ``CHECKERS_DISABLED`` environment variable.
* #6: Made it possible to force a validator or checker to run (even if disabled)
  by passing it a ``force_run = True`` keyword argument.
* #5: Added ``validators.readable()`` and ``checkers.is_readable()`` support to
  validate whether a file (path) is readable.
* #4: Added ``validators.writeable()`` and ``checkers.is_writeable()`` support to
  validate whether a file (path) is writeable. Only works on Linux, by design.
* #9: Added ``validators.executable()`` and ``checkers.is_executable()`` support
  to validate whether a file is executable. Only works on Linux, by design.

Bugs Fixed
------------

* #7: Refactored ``validators.email()`` to more-comprehensively validate email
  addresses in compliance with RFC 5322.

Testing
-------------

* #6: Added unit tests for disabling validators and checkers based on the
  ``VALIDATORS_DISABLED`` and ``CHECKERS_DISABLED`` environment variables, with
  support for the ``force_run = True`` override.
* #7: Added more extensive email address cases to test compliance with RFC 5322.
* Added unit tests for ``validators.domain()`` and ``checkers.is_domain()``.
* #5: Added unit tests for ``validators.readable()`` and ``checkers.is_readable()``
  that work on the Linux platform. Missing unit tests on Windows.
* #4: Added unit tests for ``validators.writeable()`` and ``checkers.is_writeable()``.
* #9: Added unit tests for ``validators.executable()`` and ``checkers.is_executable()``.

Documentation
---------------

* Added ``CHANGES.rst``.
* #7: Added additional detail to ``validators.email()`` documentation.
* #8: Added detailed exception / error handling documentation.
* #8: Updated validator error documentation.
* #6: Added documentation on disabling validators and checkers.
* #5: Added documentation for ``validators.readable()`` and ``checkers.is_readable()``.
* #4: Added documentation for ``validators.writeable()`` and ``checkers.is_writeable()``.
* #9: Added documentation for ``validators.executable()`` and ``checkers.is_executable()``.

----------------

Release 1.0.0 (released April 16, 2018)
=========================================

* First public release
