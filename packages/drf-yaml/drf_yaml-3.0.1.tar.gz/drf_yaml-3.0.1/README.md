# REST Framework YAML

![build-status-image]
[![pypi-version]][pypi]

**YAML support for Django REST Framework**

Full documentation for the project is available at [http://qu4tro.github.io/drf-yaml][docs].

## Overview

YAML support for the Django REST Framework, forked from [https://github.com/jpadilla/django-rest-framework-yaml][original].

## Requirements

* Python (3.8, 3.9, 3.10, 3.11)
* Django (3.2, 4.*)

## Installation

Install using `pip`...

```bash
$ pip install drf-yaml
```

## Example

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'drf_yaml.parsers.YAMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'drf_yaml.renderers.YAMLRenderer',
    ),
}
```

You can also set the renderer and parser used for an individual view, or viewset, using the APIView class based views.

```python
from rest_framework import routers, serializers, viewsets
from drf_yaml.parsers import YAMLParser
from drf_yaml.renderers import YAMLRenderer

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (YAMLParser,)
    renderer_classes = (YAMLRenderer,)
```

### Sample output

```yaml
---
-
  email: jpadilla@example.com
  is_staff: true
  url: "http://127.0.0.1:8000/users/1/"
  username: jpadilla
```

## Documentation & Support

Full documentation for the project is available at [http://qu4tro.github.io/drf-yaml][docs].


[build-status-image]: https://img.shields.io/github/checks-status/Qu4tro/drf-yaml/main
[pypi-version]: https://img.shields.io/pypi/v/drf-yaml.svg
[pypi]: https://pypi.python.org/pypi/drf-yaml
[docs]: http://qu4tro.github.io/drf-yaml
[original]: https://github.com/jpadilla/django-rest-framework-yaml
