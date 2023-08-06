import json
from copy import copy
from typing import Union

from .models import ChangeSet, Op
from jsonpath_ng import Fields, Index
from jsonpath_ng.ext import parse


def update_json(input: Union[str, dict], changeset: Union[str, ChangeSet]) -> Union[str, dict]:
    """
    Updates a json (or json-compatible dict) as per the provided changeset, returning the modified result.

    :param input: If passed a json str, will parse into dict
    :param changeset: If passed a json str, will parse into ChangeSet object
    :return: will return whatever format was passed in as input
    """

    input_type_json = False
    if type(input) == str:
        input = json.loads(input)
        input_type_json = True
    elif type(input) == dict:
        input = copy(input)
    else:
        raise ValueError("Unsupported input type %s" % type(input))

    if type(changeset) == str:
        changeset = ChangeSet.from_json(changeset)
    elif type(changeset) == dict:
        changeset = ChangeSet.from_dict(changeset)
    elif type(changeset) != ChangeSet:
        raise ValueError("Unsupported ChangeSet type %s" % type(input))

    for change in changeset.changes:
        expr = parse(change.path)

        if change.op == Op.DELETE:
            idx_item = []
            for m in expr.find(input):
                if type(m.path) == Fields:
                    fields = list(filter(lambda p: p is not None, m.path.reified_fields(input)))
                    for field in fields:
                        del m.context.value[field]
                elif type(m.path) == Index:  # If we have an array element to delete
                    idx_item.append((m.path.index, m.context))

        elif change.op == Op.INIT:
            for m in expr.find_or_create(input):
                if type(m.path) == Fields:
                    fields = list(filter(lambda p: p is not None, m.path.reified_fields(input)))
                    for field in fields:
                        if m.context.value[field] == {}:
                            m.context.value[field] = change.value
                elif type(m.path) == Index:  # If we have an array element to delete
                    if m.context.value[m.path.index] == {}:
                        m.context.value[m.path.index] = change.value

            for index, context in sorted(idx_item, key=lambda ix: ix[0], reverse=True):
                if context.value:
                    context.value.pop(index)  # always pop the last item in each

        elif change.op == Op.REPLACE:
            for m in expr.find(input):
                fields = list(filter(lambda p: p is not None, m.path.reified_fields(input)))
                for field in fields:
                    m.context.value[field] = change.value

        elif change.op == Op.UPSERT:
            input = expr.update_or_create(input, change.value)

        elif change.op == Op.ARR_INSERT:
            # Only for array insertion
            for m in expr.find(input):
                if type(m.value) != list:
                    raise ValueError("Operator '%s' should only be used against arrays, but was aimed at a '%s'" % (Op.ARR_INSERT, type(m.value)))
                else:
                    if change.index is None:
                        m.value.append(change.value)
                    elif type(change.index) == int:
                        m.value.insert(change.index, change.value)
                    else:
                        raise ValueError('Array Index of "%s" was passed, which was not of type int' % change.index)


    # Convert back to json str if necessary.
    if input_type_json:
        input = json.dumps(input)

    return input
