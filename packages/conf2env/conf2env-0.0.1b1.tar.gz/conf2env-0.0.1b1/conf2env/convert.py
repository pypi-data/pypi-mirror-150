"""Module for convert from project settings to markdown table of
environments."""
from enum import Enum
from sys import stdout
from typing import Dict, Iterable, TypeVar, Union

from pydantic import BaseSettings, Field
from pydantic.fields import ModelField, UndefinedType
from pydantic.main import ModelMetaclass

COLS = ['Name', 'Description', 'Type', 'Example', 'Default']


def pydantic_settings_to_table(obj: BaseSettings,
                               prefix: str = '',
                               config=None) -> dict:
    """From pydantic to table.

    Args:
        obj (BaseSettings): pydantic settings class

    Returns:
        list: table for markdown
    """
    if not config:
        config = obj.Config
    _table = []
    for _, field in obj.__fields__.items():
        field: ModelField = field

        env_names = field.field_info.extra.get('env_names', None)
        if env_names is None:
            env_name = field.name
        else:
            env_name = next((v for v in env_names))

        env_name = f'{prefix}{env_name}'
        if not getattr(config, 'case_sensitive', False):
            env_name = env_name.upper()

        if isinstance(field.type_, ModelMetaclass):
            if obj.Config.env_nested_delimiter:
                prefix = f'{field.name}{config.env_nested_delimiter}'
            _ttable = pydantic_settings_to_table(field.type_,
                                                 prefix=prefix,
                                                 config=config)
            _table.extend(_ttable)
            continue

        default = None
        if not isinstance(field.default, UndefinedType):
            default = field.default

        if isinstance(default, Enum):
            default = default.value

        example = default or ''
        if 'example' in field.field_info.extra:
            example = field.field_info.extra['example']

        if issubclass(field.type_, Enum):
            example = 'Any of: ' + '; '.join([v.value for v in field.type_.__members__.values()])

        if field.required:
            # env_names = f'* {env_names}'
            default = '-'
        val = [
            env_name,
            field.field_info.description or '',
            field.type_,
            example,
            default,
        ]
        _table.append(dict(zip(COLS, val)))
    return _table


MARKDOWN_TEMPLATE = "| {: <%s} | {: <%s} | {: <%s} | {: <%s} | {: <%s} |"
BREAK_TEMPLATE = "| {:-<%s} | {:-<%s} | {:-<%s} | {:-<%s} | {:-<%s} |"


def table_to_markdown(
    table: list,
    buffer=stdout,
) -> str:
    max_in_column = dict(zip(COLS, [len(col) for col in COLS]))
    for row in table:
        row['Type'] = row['Type'].__name__
        if isinstance(row['Example'], Iterable) and not isinstance(row['Example'], str):
            row['Example'] = ','.join([str(v) for v in row['Example']])
        for k in COLS:
            row[k] = str(row[k])
            size = len(row[k])
            if size > max_in_column[k]:
                max_in_column[k] = size

    maxes = tuple(max_in_column[k] for k in COLS)
    row_template = MARKDOWN_TEMPLATE % maxes

    # HEADER
    print(row_template.format(*COLS), file=buffer)
    # BREAK
    print((BREAK_TEMPLATE % maxes).format('', '', '', '', ''), file=buffer)

    # ROWS
    for row in table:
        print(row_template.format(*[row[k] for k in COLS]), file=buffer)
