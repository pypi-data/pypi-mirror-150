from copy import copy
from dataclasses import dataclass, fields
from typing import Optional, Any

from dataclasses_json import DataClassJsonMixin, config, Undefined

# Ensures we don't render 'null' fields.
ignore_none_cfg = config(undefined=Undefined.EXCLUDE, exclude=lambda f: f is None)["dataclasses_json"]


@dataclass
class Op:
    DELETE: str = "del"
    INIT: str = "init"
    UPSERT: str = "ups"
    ARR_INSERT: str = "arr_ins"


_op_fields = [f.default for f in fields(Op)]


@dataclass
class Change(DataClassJsonMixin):
    dataclass_json_config = copy(ignore_none_cfg)
    op: str
    path: str  # jsonpath str
    value: Optional[Any] = None  # Optional when deleting
    index: Optional[int] = None  # Used only in list processing

    def __post_init__(self):
        if self.op not in _op_fields:
            raise ValueError("Operation '%s' not found in list of legal operations, %s" % (self.op, _op_fields))


@dataclass
class ChangeSet(DataClassJsonMixin):
    changes: list[Change]
