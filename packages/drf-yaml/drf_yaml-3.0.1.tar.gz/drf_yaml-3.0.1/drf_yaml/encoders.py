"""Helper classes for parsers."""
import decimal
import types
from collections import OrderedDict
from datetime import time, timedelta
from uuid import UUID

import yaml
from django.utils.encoding import force_str
from django.utils.safestring import SafeString
from rest_framework.exceptions import ErrorDetail
from rest_framework.relations import Hyperlink
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from . import styles


class SafeDumper(yaml.SafeDumper):
    """
    Dumper subclass that handles commonly used DRF types.

    These are the supported types:
    - Decimal is represented as a string.
    - UUID is represented as a string.
    - Time is represented as a string.
    - TimeDelta is represented as a string.
    - Hyperlink is represented as a string.
    - ErrorDetail is represented as a string.
    - SafeString is represented as a string.
    - OrderedDict is represented as a dict.
    - ReturnDict is represented as a dict.
    - ReturnList is represented as a list.
    - Generators are represented as a list.

    It also supports the following custom types:
    - FoldedStr is represented as a string with the folded style.
    - LiteralStr is represented as a string with the literal style.
    - SingleQuotedStr is represented as a string with the single quoted style.
    - DoubleQuotedStr is represented as a string with the double quoted style.
    - FlowStyleSequence is represented as a list with the flow style.
    - FlowStyleMapping is represented as a dict with the flow style.

    These can be imported from drf_yaml.styles.
    """


SafeDumper.add_representer(
    decimal.Decimal,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        force_str(data),
    ),
)

SafeDumper.add_representer(
    UUID,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        force_str(data),
    ),
)

SafeDumper.add_representer(
    time,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        force_str(data),
    ),
)

SafeDumper.add_representer(
    timedelta,
    lambda dumper, data: dumper.represent_float(
        data.total_seconds(),
    ),
)

SafeDumper.add_representer(
    bytes,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        data.decode("utf-8"),
    ),
)

SafeDumper.add_representer(
    OrderedDict,
    yaml.representer.SafeRepresenter.represent_dict,
)

SafeDumper.add_representer(
    SafeString,
    yaml.representer.SafeRepresenter.represent_str,
)

SafeDumper.add_representer(
    Hyperlink,
    yaml.representer.SafeRepresenter.represent_str,
)

SafeDumper.add_representer(
    ErrorDetail,
    yaml.representer.SafeRepresenter.represent_str,
)

SafeDumper.add_representer(
    ReturnDict,
    yaml.representer.SafeRepresenter.represent_dict,
)

SafeDumper.add_representer(
    ReturnList,
    yaml.representer.SafeRepresenter.represent_list,
)

SafeDumper.add_representer(
    types.GeneratorType,
    yaml.representer.SafeRepresenter.represent_list,
)

SafeDumper.add_representer(
    styles.FoldedStr,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        data,
        style=">",
    ),
)

SafeDumper.add_representer(
    styles.LiteralStr,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        data,
        style="|",
    ),
)

SafeDumper.add_representer(
    styles.SingleQuotedStr,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        data,
        style="'",
    ),
)

SafeDumper.add_representer(
    styles.DoubleQuotedStr,
    lambda dumper, data: dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        data,
        style='"',
    ),
)

SafeDumper.add_representer(
    styles.FlowStyleSequence,
    lambda dumper, data: dumper.represent_sequence(
        "tag:yaml.org,2002:seq",
        data,
        flow_style=True,
    ),
)

SafeDumper.add_representer(
    styles.FlowStyleMapping,
    lambda dumper, data: dumper.represent_mapping(
        "tag:yaml.org,2002:map",
        data,
        flow_style=True,
    ),
)
