-----------

Release 1.1.0 (in development)
==========================================

Features Added
----------------

* Added `validators.domain()` and `checkers.is_domain()` support with unit tests.
* #8: Added more verbose exceptions while retaining backwards-compatability with standard
  library exceptions.

Bugs Fixed
------------

* #7: Refactored `validators.email()` to more-comprehensively validate email
  addresses in compliance with RFC 5322.

Testing
-------------

* #7: Added more extensive email address cases to test compliance with RFC 5322.
* Added unit tests for `validators.domain()` and `checkers.is_domain()`.

Documentation
---------------

* Added CHANGES.rst.
* #7: Added additional detail to `validators.email()` documentation.
* #8: Added detailed exception / error handling documentation.
* #8: Updated validator error documentation.

----------------

Release 1.0.0 (released April 16, 2018)
=========================================

* First public release
