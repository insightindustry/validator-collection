**********************************
Validator Reference
**********************************

.. |strong| raw:: html

  <strong>

.. |/strong| raw:: html

  </strong>

.. include:: _validator_list.rst

Using Validators
====================

.. include:: _using_validators.rst

.. module:: validator_collection.validators

-----------

Core
=========

dict
-------

.. autofunction:: dict

string
---------

.. autofunction:: string

iterable
----------

.. autofunction:: iterable

none
-------

.. autofunction:: none

not_empty
-----------

.. autofunction:: not_empty

uuid
-------

.. autofunction:: uuid

variable_name
---------------------

.. autofunction:: variable_name

-------------

Date / Time
===============

date
----------

.. autofunction:: date

datetime
----------

.. autofunction:: datetime

time
----------

.. autofunction:: time

timezone
----------

.. autofunction:: timezone

---------------

Numbers
===========

.. note::

  Because Python's :class:`None <python:None>` is implemented as an integer
  value, numeric validators do not check "falsiness". Doing so would find
  false positives if ``value`` were set to ``0``.

  Instead, all numeric validators explicitly check for the Python global singleton
  :class:`None <python:None>`.

numeric
----------

.. autofunction:: numeric

integer
----------

.. autofunction:: integer

float
----------

.. autofunction:: float

fraction
----------

.. autofunction:: fraction

decimal
----------

.. autofunction:: decimal

------------

File-related
===============

bytesIO
----------

.. autofunction:: bytesIO

stringIO
----------

.. autofunction:: stringIO

path
--------

.. autofunction:: path

path_exists
-------------

.. autofunction:: path_exists

file_exists
---------------

.. autofunction:: file_exists

directory_exists
------------------

.. autofunction:: directory_exists

readable
------------

.. autofunction:: readable

writeable
------------

.. autofunction:: writeable

-------------------

Internet-related
===================

email
--------

.. autofunction:: email

url
------

.. autofunction:: url

domain
--------

.. autofunction:: domain

ip_address
-------------

.. autofunction:: ip_address

ipv4
--------

.. autofunction:: ipv4

ipv6
-------

.. autofunction:: ipv6

mac_address
--------------

.. autofunction:: mac_address
