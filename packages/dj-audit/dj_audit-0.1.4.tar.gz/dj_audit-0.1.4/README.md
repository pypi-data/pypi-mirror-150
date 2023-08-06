# django-audit


![GitHub issues](https://img.shields.io/github/issues/Emmarex/django-audit)
![PyPI - Downloads](https://img.shields.io/pypi/dm/dj_audit)
[![codecov](https://codecov.io/gh/Emmarex/django-audit/branch/main/graph/badge.svg?token=U964OH44O9)](https://codecov.io/gh/Emmarex/django-audit)
[![CodeCov](https://github.com/Emmarex/django-audit/actions/workflows/main.yml/badge.svg)](https://github.com/Emmarex/django-audit/actions/workflows/main.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Django Audit is a simple Django app that tracks and logs requests to your application.

## Quick Start

1. Install django-audit

```bash
pip install dj-audit
```

2. Add ```dj_audit``` to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...,
    "dj_audit"
]
```

3. Add ```dj_audit``` middleware:

```python
MIDDLEWARE = [
    ...
    "dj_audit.middleware.AuditMiddleware"
]
```

if you want access to the dj-audit dashboard, then add the following to your ```urls.py```

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("dj-audit/", include('dj_audit.urls'))
]
```

4. Run migrate

```bash
python manage.py migrate
```

## Management commands

```flush_auditlog``` - Cleans up dj-audit AuditLog table

```bash
python manage.py flush_auditlog
```

## Customizing dj-audit
You have a couple options available to you to customize ```dj-audit``` a bit. These should be defined in your ```settings.py``` file.

- ```AUDIT_LOG_TEMPLATE```: str: If set, the template here will be render when the user visits the audit log page (i.e /dj-audit/audit-logs/)

- ```REQUEST_STATUS_TEMPLATE```: str: If set, the template here will be render when the user visits the request status page (i.e /dj-audit/request-status/)

- ```IGNORE_FILE_EXTENSIONS```: list: If set, the middleware will not log endpoints containing the extensions specified in the list. **DEFAULT**: ```['.svg', '.js', '.css', '.png', '.jpg', '.ico']```

- ```AUDIT_LOG_DJ_REST_CONTENT_TYPES```: list: content type of your Rest APIs. **DEFAULT**: ```['application/json', 'application/xml']```

- ```AUDIT_LOG_DJ_EXTRA_CONDITIONS_FOR_200```: bool: Specify if there are extra conditions you will like to check to validate if a request is successful or not. **DEFAULT**: ```False```

- ```AUDIT_LOG_DJ_EXTRA_CONDITIONS```: list: Extra conditions to set to determine if a request body is successful or not. **DEFAULT**: ```[]```


## Test

```bash
make test
```

or with coverage

```bash
make coverage_test
```
