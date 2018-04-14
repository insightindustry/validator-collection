**********************************
Checker Reference
**********************************

.. list-table::
  :widths: 30 30 30 30 30
  :header-rows: 1

  * - Core
    - Date/Time
    - Numbers
    - File-related
    - Internet-related
  * - :func:`is_type <validator_collection.checkers.is_type>`
    - :func:`is_date <validator_collection.checkers.is_date>`
    - :func:`is_numeric <validator_collection.checkers.is_numeric>`
    - :func:`is_bytesIO <validator_collection.checkers.is_bytesIO>`
    - :func:`is_email <validator_collection.checkers.is_email>`
  * - :func:`are_equivalent <validator_collection.checkers.are_equivalent>`
    - :func:`is_datetime <validator_collection.checkers.is_datetime>`
    - :func:`is_integer <validator_collection.checkers.is_integer>`
    - :func:`is_stringIO <validator_collection.checkers.is_stringIO>`
    - :func:`is_url <validator_collection.checkers.is_url>`
  * - :func:`are_dicts_equivalent <validator_collection.checkers.are_dicts_equivalent>`
    - :func:`is_time <validator_collection.checkers.is_time>`
    - :func:`is_float <validator_collection.checkers.is_float>`
    - :func:`is_pathlike <validator_collection.checkers.is_pathlike>`
    - :func:`is_ip <validator_collection.checkers.is_ip>`
  * - :func:`is_dict <validator_collection.checkers.is_dict>`
    - :func:`is_timezone <validator_collection.checkers.is_timezone>`
    - :func:`is_on_filesystem <validator_collection.checkers.is_on_filesystem>`
    - :func:`is_fraction <validator_collection.checkers.is_fraction>`
    - :func:`is_ipv4 <validator_collection.checkers.is_ipv4>`
  * - :func:`is_string <validator_collection.checkers.is_string>`
    -
    - :func:`is_decimal <validator_collection.checkers.is_decimal>`
    - :func:`is_file <validator_collection.checkers.is_file>`
    - :func:`is_ipv6 <validator_collection.checkers.is_ipv6>`
  * - :func:`is_iterable <validator_collection.checkers.is_iterable>`
    -
    -
    - :func:`is_directory <validator_collection.checkers.is_directory>`
    - :func:`is_mac_address <validator_collection.checkers.is_mac_address>`
  * - :func:`is_not_empty <validator_collection.checkers.is_not_empty>`
    -
    -
    -
    -
  * - :func:`is_none <validator_collection.checkers.is_none>`
    -
    -
    -
    -
  * - :func:`is_valid_variable_name <validator_collection.checkers.is_valid_variable_name>`
    -
    -
    -
    -
  * - :func:`is_uuid <validator_collection.checkers.is_uuid>`
    -
    -
    -
    -

.. module:: validator_collection.checkers

Core
=======

is_type
---------

.. autofunction:: is_type

are_equivalent
-----------------

.. autofunction:: are_equivalent

are_dicts_equivalent
------------------------

.. autofunction:: are_dicts_equivalent

is_dict
---------

.. autofunction:: is_dict

is_string
---------

.. autofunction:: is_string

is_iterable
--------------

.. autofunction:: is_iterable

is_not_empty
--------------

.. autofunction:: is_not_empty

is_none
--------------

.. autofunction:: is_none

is_valid_variable_name
--------------------------

.. autofunction:: is_valid_variable_name

is_uuid
---------

.. autofunction:: is_uuid

Date / Time
==============

is_date
--------------

.. autofunction:: is_date

is_datetime
--------------

.. autofunction:: is_datetime

is_time
--------------

.. autofunction:: is_time

is_timezone
--------------

.. autofunction:: is_timezone

Numbers
=========

is_numeric
--------------

.. autofunction:: is_numeric

is_integer
--------------

.. autofunction:: is_integer

is_float
--------------

.. autofunction:: is_float

is_fraction
--------------

.. autofunction:: is_fraction

is_decimal
--------------

.. autofunction:: is_decimal

File-related
===============

is_bytesIO
--------------

.. autofunction:: is_bytesIO

is_stringIO
--------------

.. autofunction:: is_stringIO

is_pathlike
--------------

.. autofunction:: is_pathlike

is_on_filesystem
-------------------

.. autofunction:: is_on_filesystem

is_file
--------------

.. autofunction:: is_file

is_directory
--------------

.. autofunction:: is_directory

Internet-related
===================

is_email
-------------------

.. autofunction:: is_email

is_url
-------------------

.. autofunction:: is_url

is_ip
-------------------

.. autofunction:: is_ip

is_ipv4
-------------------

.. autofunction:: is_ipv4

is_ipv6
-------------------

.. autofunction:: is_ipv6

is_mac_address
-------------------

.. autofunction:: is_mac_address
