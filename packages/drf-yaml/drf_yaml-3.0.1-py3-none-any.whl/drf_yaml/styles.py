"""String types for YAML."""


class FoldedStr(str):
    """A string which should be rendered as a YAML folded string."""


class LiteralStr(str):
    """A string which should be rendered as a YAML literal string."""


class SingleQuotedStr(str):
    """A string which should be rendered as a YAML single quoted string."""


class DoubleQuotedStr(str):
    """A string which should be rendered as a YAML double quoted string."""


class FlowStyleSequence(list):
    """A sequence which should be rendered as a YAML flow style sequence."""


class FlowStyleMapping(dict):
    """A mapping which should be rendered as a YAML flow style mapping."""
