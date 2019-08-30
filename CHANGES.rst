-----------

Release 1.3.6 (released August 29, 2019)
============================================

* #37: Added regex matching to variable name validation. Still checks compilation
  but first must pass regex validation.

-----------

Release 1.3.5 (released May 17, 2019)
============================================

* #34: Fixed case sensitivity bugs in URL validator.

-----------

Release 1.3.4 (released April 3, 2019)
============================================

* #32: Removed a `print` statement left over from debugging.

-----------

Release 1.3.3 (released March 23, 2019)
============================================

* #28 and #29: Fixed an error where special URLs (`localhost`) and special IPs (e.g.
  `10.1.1.1`) failed when used with an explicit port or path.

-----------

Release 1.3.2 (released February 9, 2019)
============================================

* #25: Fixed an error where an underscore in a host name was not being properly
  recognized (h/t @mastak) when parsing URLs and domain names.
* #23: Fixed an error where URL / domain validators and checkers were (incorrectly)
  failing on valid special names (e.g. `localhost`, etc.) and special IPs (e.g. `10.1.1.1`).
* #24: Fixed bug where checkers returned false-negatives when the underlying validator
  raised a `SyntaxError`.

-----------

Release 1.3.1 (released November 30, 2018)
============================================

* #21: Fixed `validators.datetime()` handling of timezone offsets to conform to ISO-8601.

-----------

Release 1.3.0 (released November 12, 2018)
============================================

* #18: Upgraded ``requests`` requirement to 2.20.1
* #17: Added ``validators.json()`` with support for JSON Schema validation.
* #17: Added ``checkers.is_json()`` with support for checking against JSON Schema.
* Added Python 3.7 to the Travis CI Test Matrix.

-----------

Release 1.2.0 (released August 4, 2018)
==========================================

Features Added
----------------

* #14: Added ``coerce_value`` argument to ``validators.date()``, ``validators.datetime()``,
  and ``validators.time()``.

Bugs Fixed
------------

* #11: Removed legacy print statements.
* #13: ``checkers.is_time()``, ``checkers.is_date()``, and ``checkers.is_datetime()``
  no longer return false positives

Release 1.1.0 (released April 23, 2018)
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
