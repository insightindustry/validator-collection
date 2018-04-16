# Validator Collection
**Python library of 60+ commonly-used validator functions**

| Branch | Unit Tests and Coverage |
|--------|-------------------------|
| **[master](https://github.com/insightindustry/validator-collection/tree/master)** | [![Build Status](https://travis-ci.org/insightindustry/validator-collection.svg?branch=master)](https://travis-ci.org/insightindustry/validator-collection)[![codecov](https://codecov.io/gh/insightindustry/validator-collection/branch/master/graph/badge.svg)](https://codecov.io/gh/insightindustry/validator-collection) [![Documentation Status](https://readthedocs.org/projects/validator-collection/badge/?version=latest)](http://validator-collection.readthedocs.io/en/latest/?badge=latest) |
| **[develop](https://github.com/insightindustry/validator-collection/tree/develop)** | [![Build Status](https://travis-ci.org/insightindustry/validator-collection.svg?branch=develop)](https://travis-ci.org/insightindustry/validator-collection) [![codecov](https://codecov.io/gh/insightindustry/validator-collection/branch/develop/graph/badge.svg)](https://codecov.io/gh/insightindustry/validator-collection) [![Documentation Status](https://readthedocs.org/projects/validator-collection/badge/?version=develop)](http://validator-collection.readthedocs.io/en/latest/?badge=develop) |

The **Validator Collection** is a Python library that provides more than 60
functions that can be used to validate the type and contents of an input value.

Each function has a consistent syntax for easy use, and has been tested on
Python 2.7, 3.4, 3.5, and 3.6.

For a list of validators available, please see [below](#available-validators-and-checkers).

**For complete documentation on the library, please visit our [Validator Collection Documentation](https://validator-collection.readthedocs.io)**.

***

## Table of Contents

1. [Table of Contents](#table_of_contents)
2. [Installation](#installation)
   - [Dependencies](#dependencies)
4. [Available Validators and Checkers](#available-validators-and-checkers)
   - [Validators](#validators)
   - [Checkers](#checkers)
5. [Hello World](#hello-world)
   - [Using Validators](#using-validators)
   - [Using Checkers][#using-checkers]
6. [Best Practices](#best-practices)
   - [Defensive Approach: Check, then Convert if Necessary](#defensive-approach-check-then-convert-if-necessary)
   - [Confident Approach: try ... except](#confident-approach-try---except)
7. [Reporting Issues](#reporting-issues)
8. [Contributing](#contributing)
9. [Testing](#testing)
10. [License](#license)

***

## Installation

The **Validator Collection** will only work on Python 2.7, 3.4, 3.5, and 3.6.

To install it, just execute the following from the command-line:

```bash
$ pip install validator-collection
```

### Dependencies

If you are using Python 3.x, there are no external dependencies. The library
will use the Python standard library.

If you are using Python 2.7, the library will install the [regex](https://pypi.python.org/pypi/regex) drop-in
replacement for the Python standard library's buggy `re` module.

***

## Available Validators and Checkers

### Validators

:green_book: **[COMPLETE DOCUMENTATION: Validator Reference](http://validator-collection.readthedocs.io/en/latest/validators.html)**

- **Core**
  - [`dict`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.dict)
  - [`string`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.string)
  - [`iterable`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.iterable)
  - [`none`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.none)
  - [`not_empty`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.not_empty)
  - [`variable_name`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.variable_name)
- **Date/Time**
  - [`date`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.date)
  - [`datetime`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.datetime)
  - [`time`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.time)
  - [`timezone`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.timezone)
- **Numbers**
  - [`numeric`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.numeric)
  - [`integer`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.integer)
  - [`float`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.float)
  - [`fraction`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.fraction)
  - [`decimal`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.decimal)
- **File-related**
  - [`bytesIO`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.bytesIO)
  - [`stringIO`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.stringIO)
  - [`path`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.path)
  - [`path_exists`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.path_exists)
  - [`file_exists`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.file_exists)
  - [`directory_exists`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.directory_exists)
- **Internet-related**
  - [`email`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.email)
  - [`url`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.url)
  - [`ip_address`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.ip_address)
  - [`ipv4`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.ipv4)
  - [`ipv6`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.ipv6)
  - [`mac_address`](http://validator-collection.readthedocs.io/en/latest/validators.html#validator_collection.validators.mac_address)

### Checkers

:green_book: **[COMPLETE DOCUMENTATION: Checker Reference](http://validator-collection.readthedocs.io/en/latest/checkers.html)**

- **Core**
  - [`is_type`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_type)
  - [`is_between`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_between)
  - [`has_length`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.has_length)
  - [`are_equivalent`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.are_equivalent)
  - [`are_dicts_equivalent`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.are_dicts_equivalent)
  - [`is_dict`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_dict)
  - [`is_string`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_string)
  - [`is_iterable`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_iterable)
  - [`is_not_empty`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_not_empty)
  - [`is_none`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_none)
  - [`is_callable`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_callable)
  - [`is_uuid`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_uuid)
  - [`is_variable_name`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_variable_name)
* **Date/Time**
  - [`is_date`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_date)
  - [`is_datetime`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_datetime)
  - [`is_time`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_time)
  - [`is_timezone`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_timezone)
* **Numbers**
  - [`is_numeric`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_numeric)
  - [`is_integer`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_integer)
  - [`is_float`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_float)
  - [`is_fraction`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_fraction)
  - [`is_decimal`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_decimal)
* **File-related**
  - [`is_bytesIO`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_bytesIO)
  - [`is_stringIO`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_stringIO)
  - [`is_pathlike`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_pathlike)
  - [`is_on_filesystem`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_on_filesystem)
  - [`is_file`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_file)
  - [`is_directory`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_directory)
* **Internet-related**
  - [`is_email`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_email)
  - [`is_url`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_url)
  - [`is_ip_address`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_ip_address)
  - [`is_ipv4`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_ipv4)
  - [`is_ipv6`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_ipv6)
  - [`is_mac_address`](http://validator-collection.readthedocs.io/en/latest/checkers.html#validator_collection.checkers.is_mac_address)

***

## Hello World

All validator functions have a consistent syntax so that using them is pretty
much identical. Here's how it works:

```python
import validator_collection.validators as validators
import validator_collection.checkers as checkers

email_address = validators.email('test@domain.dev')
# The value of email_address will now be "test@domain.dev"

email_address = validators.email('this-is-an-invalid-email')
# Will raise a ValueError

email_address = validators.email(None)
# Will raise a ValueError

email_address = validators.email(None, allow_empty = True)
# The value of email_address will now be None

email_address = validators.email('', allow_empty = True)
# The value of email_address will now be None

is_email_address = checkers.is_email('test@domain.dev')
# The value of is_email_address will now be True

is_email_address = checkers.is_email('this-is-an-invalid-email')
# The value of is_email_address will now be False

is_email_address = checkers.is_email(None)
# The value of is_email_address will now be False
```

Pretty simple, right? Let's break it down just in case: Each validator comes in
two flavors: a _validator_ and a _checker_.

### Using Validators

A validator does what it says on the tin: It validates that an input value is
what you think it should be, and returns its valid form.

Each validator is expressed as the name of the thing being validated, for example
`email()`.

Each validator accepts a value as its first argument, and an optional `allow_empty`
Boolean as its second argument. For example:

```python
email_address = validators.email(value, allow_empty = True)
```

If the value you're validating validates successfully, it will be returned. If
the value you're validating needs to be coerced to a different type, the
validator will try to do that. So for example:

```python
validators.integer(1)
validators.integer('1')
```

will both return an `int` of `1`.

If the value you're validating is empty/falsey and `allow_empty` is `False`,
then the validator will raise a `ValueError` exception. If `allow_empty`
is `True`, then an empty/falsey input value will be converted to a `None`
value.

:warning: **PLEASE NOTE:** By default, `allow_empty` is always set to `False`.

If the value you're validating fails its validation for some reason, the validator
may raise different exceptions depending on the reason. In most cases, this will
be a `ValueError` though it can sometimes be a `TypeError`, or an
`AttributeError`, etc. For specifics on each validator's likely exceptions
and what can cause them, please review the **[Validator Reference](http://validator-collection.readthedocs.io/en/latest/validators.html)**.

:pencil: **PLEASE NOTE:**
Some validators (particularly numeric ones like `integer`) have additional
options which are used to make sure the value meets criteria that you set for
it. These options are always included as keyword arguments *after* the
`allow_empty` argument, and are documented for each validator below.

### Using Checkers

Likewise, a **checker** is what it sounds like: It checks that an input value
is what you expect it to be, and tells you `True`/`False` whether it is or not.

:warning: **IMPORTANT:** Checkers do *not* verify or convert object types. You can think of a checker as
a tool that tells you whether its corresponding [validator](#using-validators)
would fail. See **[Best Practices](#best-practices)** for tips and tricks on
using the two together.

Each checker is expressed as the name of the thing being validated, prefixed by
`is_`. So the checker for an email address is
`is_email()` and the checker
for an integer is `is_integer()`.

Checkers take the input value you want to check as their first (and often only)
positional argumet. If the input value validates, they will return `True`. Unlike
[validators](#using-validators), checkers will not raise an exception if
validation fails. They will instead return `False`.

:bulb: **Here's a tip:** If you need to know *why* a given value failed to validate, use the validator
instead.

:bulb: **Here's a tip:** Some checkers (particularly numeric ones like
`is_integer`) have additional
options which are used to make sure the value meets criteria that you set for
it. These options are always *optional* and are included as keyword arguments
*after* the input value argument. For details, please see the
**[Checker Reference](http://validator-collection.readthedocs.io/en/latest/checkers.html)**

***

## Best Practices

[Checkers](#using-checkers) and [Validators](using-validators)
are designed to be used together. You can think of them as a way to quickly and
easily verify that a value contains the information you expect, and then make
sure that value is in the form your code needs it in.

There are two fundamental patterns that we find work well in practice.

### Defensive Approach: Check, then Convert if Necessary

We find this pattern is best used when we don't have any certainty over a given
value might contain. It's fundamentally defensive in nature, and applies the
following logic:

1. Check whether `value` contains the information we need it to or can be converted to the form we need it in.
2. If `value` does not contain what we need but *can* be converted to what we need, do the conversion.
3. If `value` does not contain what we need but *cannot* be converted to what we need, raise an error (or handle it however it needs to be handled).

We tend to use this where we're first receiving data from outside of our control,
so when we get data from a user, from the internet, from a third-party API, etc.

Here's a quick example of how that might look in code:

```python

from validator_collection import checkers, validators

def some_function(value):
  # Check whether value contains a whole number.
  is_valid = checkers.is_integer(value,
                                 coerce_value = False)

  # If the value does not contain a whole number, maybe it contains a
  # numeric value that can be rounded up to a whole number.
  if not is_valid and checkers.is_integer(value, coerce_value = True):
      # If the value can be rounded up to a whole number, then do so:
      value = validators.integer(value, coerce_value = True)
  elif not is_valid:
      # Since the value does not contain a whole number and cannot be converted to
      # one, this is where your code to handle that error goes.
      raise ValueError('something went wrong!')

  return value

value = some_function(3.14)
# value will now be 4

new_value = some_function('not-a-number')
# will raise ValueError
```

Let's break down what this code does. First, we define `some_function()` which
takes a value. This function uses the `is_integer()` checker to see if `value`
contains a whole number, regardless of its type.

If it doesn't contain a whole number, maybe it contains a numeric value that can
be rounded up to a whole number? It again uses the `is_integer()` to check if that's
possible. If it is, then it calls the `integer()` validator to coerce `value` to a
whole number.

If it can't coerce `value` to a whole number? It raises a `ValueError`.


### Confident Approach: try ... except

Sometimes, we'll have more confidence in the values that we can expect to work
with. This means that we might expect `value` to *generally* have the kind of
data we need to work with. This means that situations where `value` doesn't
contain what we need will truly be exceptional situations, and can be handled
accordingly.

In this situation, a good approach is to apply the following logic:

1. Skip a checker entirely, and just wrap the validator in a `try...except` block.

We tend to use this in situations where we're working with data that our own
code has produced (meaning we know - generally - what we can expect, unless
something went seriously wrong).

Here's an example:

```python
from validator_collection import validators

def some_function(value):
  try:
    email_address = validators.email(value, allow_empty = False)
  except ValueError:
    # handle the error here

  # do something with your new email address value

  return email_address

email = some_function('email@domain.com')
# This will return the email address.

email = some_function('not-a-valid-email')
# This will raise a ValueError that some_function() will handle.

email = some_function(None)
# This will raise a ValueError that some_function() will handle.
```

So what's this code do? It's pretty straightforward. `some_function()` expects
to receive a `value` that contains an email address. We expect that `value`
will *typically* be an email address, and not something weird (like a number or
something). So we just try the validator - and if validation fails, we handle
the error appropriately.

***

## Reporting Issues

If you want to report issues to the **Validator Collection**, please go ahead and do so [here](https://github.com/insightindustry/validator-collection/issues).

***

## Contributing

Please see our complete **[Contributor Guide](http://validator-collection.readthedocs.io/en/latest/contributing.html)**

***

## Testing

Please see our **[Testing Reference](http://validator-collection.readthedocs.io/en/latest/testing.html)**

***

## License

The **Validator Collection** is available via an [MIT License](/LICENSE).
