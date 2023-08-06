import os
from os import PathLike
from datetime import datetime, timedelta

import click
from pygit2 import discover_repository, init_repository, Repository, Signature
from pygit2 import GIT_SORT_REVERSE, GIT_DIFF_REVERSE, GIT_DIFF_SHOW_BINARY, GIT_APPLY_LOCATION_BOTH
from git_timemachine.utils import print_error


@click.command('migrate')
@click.argument('src_dir', type=click.Path(exists=True, file_okay=False), default=os.getcwd())
@click.argument('dest_dir', type=click.Path(exists=False, file_okay=False), required=False, default=None)
@click.option('-o', '--offset', help='Time offset for each commit.', type=str, required=False)
@click.option('--default-head', help='Reference name of default HEAD', type=str, default='main')
@click.pass_context
def migrate_command(ctx: click.Context, src_dir: PathLike, dest_dir: PathLike, offset: str, default_head: str):
    """Migrate commit logs from a repository to another."""

    if dest_dir is None:
        dest_dir = f'{src_dir}.migrated'

    if os.path.exists(dest_dir):
        raise FileExistsError(f'Destination directory {dest_dir} already exists.')

    os.mkdir(dest_dir, 0o755)

    src_repo = Repository(discover_repository(str(src_dir)))
    dest_repo = init_repository(dest_dir, initial_head=default_head)

    parent = []

    ref_name = f'refs/heads/{default_head}'

    for commit in src_repo.walk(src_repo.head.target, GIT_SORT_REVERSE):
        if len(commit.parents) > 0:
            diff = commit.tree.diff_to_tree(commit.parents[0].tree, flags=GIT_DIFF_REVERSE | GIT_DIFF_SHOW_BINARY)
        else:
            diff = commit.tree.diff_to_tree(flags=GIT_DIFF_REVERSE | GIT_DIFF_SHOW_BINARY)

        dest_repo.apply(diff, location=GIT_APPLY_LOCATION_BOTH)
        dest_repo.index.write()

        tree = dest_repo.index.write_tree()

        if tree is None:
            print_error('Failed to write index tree.')
            ctx.exit(1)

        seconds = 0
        if offset is not None:
            unit = offset[-1]
            multi = {'s': 1, 'm': 60, 'h': 60 * 60, 'd': 60 * 60 * 24}

            if unit not in multi:
                raise ValueError(f'Unknown offset unit: {unit}')

            seconds = int(offset[:-1]) * multi[unit]

        dt = datetime.fromtimestamp(commit.author.time) + timedelta(seconds=seconds)

        author = Signature(
            name=commit.author.name,
            email=commit.author.email,
            time=int(dt.timestamp()),
            encoding='utf-8',
            offset=int(dt.astimezone().tzinfo.utcoffset(dt).seconds / 60)
        )

        committer = author

        oid = dest_repo.create_commit(ref_name, author, committer, commit.message, tree, parent)

        if oid is None:
            print_error('Failed to create commit.')
            ctx.exit(1)

        parent = [dest_repo.head.target]
