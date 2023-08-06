# paper-jsoneditor

JSON input widget for paper-admin.

[![PyPI](https://img.shields.io/pypi/v/paper-jsoneditor.svg)](https://pypi.org/project/paper-jsoneditor/)
[![Build Status](https://github.com/dldevinc/paper-jsoneditor/actions/workflows/tests.yml/badge.svg)](https://github.com/dldevinc/paper-jsoneditor)
[![Software license](https://img.shields.io/pypi/l/paper-jsoneditor.svg)](https://pypi.org/project/paper-jsoneditor/)

## Compatibility

-   `python` >= 3.6
-   `django` >= 3.1
-   `paper-admin` >= 6.0

## Installation

Install the latest release with pip:

```shell
pip install paper-jsoneditor
```

Add `paper_jsoneditor` to your INSTALLED_APPS in django's `settings.py`:

```python
INSTALLED_APPS = (
    # other apps
    "paper_jsoneditor",
)
```

## Usage

```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from paper_jsoneditor.fields import JSONField


class SampleModel(models.Model):
    data = JSONField(_("JSON"))

    class Meta:
        verbose_name = _("Sample")
```

Result:
![image](https://user-images.githubusercontent.com/6928240/202204440-a1babd34-263f-45c8-8dd5-7ff9c05d8512.png)

## Preserving JSON object keys order

By default, Django uses the `jsonb` internal type for `JSONField` (for PostgreSQL).

From the [Postgres documentation](https://www.postgresql.org/docs/15/datatype-json.html):

> <...> jsonb does not preserve white space, does not preserve the order
> of object keys, and does not keep duplicate object keys. If duplicate keys
> are specified in the input, only the last value is kept.
>
> In general, most applications should prefer to store JSON data as jsonb,
> unless there are quite specialized needs, such as legacy assumptions about
> ordering of object keys.

If you really do need to preserve the key order, use `OrderedJSONField`.
It uses the `TEXT` type to store data:

```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from paper_jsoneditor.fields import OrderedJSONField


class SampleModel(models.Model):
    data = OrderedJSONField(_("JSON"))

    class Meta:
        verbose_name = _("Sample")
```
