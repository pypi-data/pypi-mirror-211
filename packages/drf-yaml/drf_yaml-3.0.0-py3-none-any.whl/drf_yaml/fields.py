"""
Custom DRF fields for use in serialization when using the YAMLRenderer.

These fields are used to render the YAML in a more readable way.
"""
from typing import Any

from rest_framework import fields

from . import styles


class FlowStyleDictField(fields.DictField):
    """A DRF field which renders as a YAML flow style mapping."""

    def to_representation(self, value: Any) -> dict[Any, Any]:
        """Render a flow style mapping."""
        return styles.flow_style_mapping(super().to_representation(value))


class FlowStyleListField(fields.ListField):
    """A DRF field which renders as a YAML flow style sequence."""

    def to_representation(self, value: Any) -> list[Any]:
        """Render a flow style sequence."""
        return styles.flow_style_sequence(super().to_representation(value))


class SingleQuotedCharField(fields.CharField):
    """A DRF field which renders as a YAML single quoted string."""

    def to_representation(self, value: Any) -> str:
        """Render a single quoted string."""
        return styles.single_quoted_str(super().to_representation(value))


class DoubleQuotedCharField(fields.CharField):
    """A DRF field which renders as a YAML double quoted string."""

    def to_representation(self, value: Any) -> str:
        """Render a double quoted string."""
        return styles.double_quoted_str(super().to_representation(value))


class FoldedCharField(fields.CharField):
    """A DRF field which renders as a YAML folded string."""

    def to_representation(self, value: Any) -> str:
        """Render a folded string."""
        return styles.folded_str(super().to_representation(value))


class LiteralCharField(fields.CharField):
    """A DRF field which renders as a YAML literal string."""

    def to_representation(self, value: Any) -> str:
        """Render a literal string."""
        return styles.literal_str(super().to_representation(value))
