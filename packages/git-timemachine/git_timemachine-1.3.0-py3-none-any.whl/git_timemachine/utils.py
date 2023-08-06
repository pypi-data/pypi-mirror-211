from typing import Iterable

import click

from pygit2 import GIT_STATUS_INDEX_NEW, GIT_STATUS_INDEX_RENAMED, GIT_STATUS_INDEX_MODIFIED
from pygit2 import GIT_STATUS_INDEX_DELETED, GIT_STATUS_INDEX_TYPECHANGE


def print_error(msg: str):
    click.echo(click.style(f'Error: {msg}', fg='red'), err=True)


def print_warning(msg: str):
    click.echo(click.style(f'Warning: {msg}', fg='yellow'))


def print_success(msg: str):
    click.echo(click.style(f'Success: {msg}', fg='green'))


def print_debug(msg: str):
    click.echo(click.style(f'Debug: {msg}', fg='cyan'))


def index_status_texts(status: int) -> Iterable:
    texts = {
        GIT_STATUS_INDEX_NEW: 'new',
        GIT_STATUS_INDEX_MODIFIED: 'modified',
        GIT_STATUS_INDEX_DELETED: 'deleted',
        GIT_STATUS_INDEX_RENAMED: 'renamed',
        GIT_STATUS_INDEX_TYPECHANGE: 'type changed'
    }

    return map(lambda i: texts[i], filter(lambda i: status & i == i, texts.keys()))
