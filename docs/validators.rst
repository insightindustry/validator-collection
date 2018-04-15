**********************************
Validator Reference
**********************************

.. list-table::
  :widths: 30 30 30 30 30
  :header-rows: 1

  * - Core
    - Date/Time
    - Numbers
    - File-related
    - Internet-related
  * - :func:`dict <validator_collection.validators.dict>`
    - :func:`date <validator_collection.validators.date>`
    - :func:`numeric <validator_collection.validators.numeric>`
    - :func:`bytesIO <validator_collection.validators.bytesIO>`
    - :func:`email <validator_collection.validators.email>`
  * - :func:`string <validator_collection.validators.string>`
    - :func:`datetime <validator_collection.validators.datetime>`
    - :func:`integer <validator_collection.validators.integer>`
    - :func:`stringIO <validator_collection.validators.stringIO>`
    - :func:`url <validator_collection.validators.url>`
  * - :func:`iterable <validator_collection.validators.iterable>`
    - :func:`time <validator_collection.validators.time>`
    - :func:`float <validator_collection.validators.float>`
    - :func:`path <validator_collection.validators.path>`
    - :func:`ipv4 <validator_collection.validators.ipv4>`
  * - :func:`none <validator_collection.validators.none>`
    - :func:`timezone <validator_collection.validators.timezone>`
    - :func:`fraction <validator_collection.validators.fraction>`
    - :func:`path_exists <validator_collection.validators.path_exists>`
    - :func:`ipv6 <validator_collection.validators.ipv6>`
  * - :func:`not_empty <validator_collection.validators.not_empty>`
    -
    - :func:`decimal <validator_collection.validators.decimal>`
    - :func:`file_exists <validator_collection.validators.file_exists>`
    - :func:`mac_address <validator_collection.validators.mac_address>`
  * - :func:`uuid <validator_collection.validators.uuid>`
    -
    -
    - :func:`directory_exists <validator_collection.validators.directory_exists>`
    -
  * - :func:`valid_variable_name <validator_collection.validators.valid_variable_name>`
    -
    -
    -
    -

.. module:: validator_collection.validators

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

valid_variable_name
---------------------

.. autofunction:: valid_variable_name

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

Numbers
===========

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

Internet-related
===================

email
--------

.. autofunction:: email

url
------

.. autofunction:: url

ipv4
--------

.. autofunction:: ipv4

ipv6
-------

.. autofunction:: ipv6

mac_address
--------------

.. autofunction:: mac_address
