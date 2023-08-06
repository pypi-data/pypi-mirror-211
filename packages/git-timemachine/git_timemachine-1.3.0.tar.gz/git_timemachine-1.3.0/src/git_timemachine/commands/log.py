import json
from pathlib import Path

import click
from pygit2 import discover_repository, Repository


@click.command('log')
@click.argument('repo_dir', type=click.Path(exists=True, file_okay=False), default=Path.cwd())
def log_command(repo_dir: Path):
    """Show commit logs of a repository in formatted data."""

    repo = Repository(discover_repository(str(repo_dir)))

    click.echo(json.dumps(
        [{
            'id': commit.id.hex,
            'author': {
                'name': commit.author.name,
                'email': commit.author.email,
                'time': commit.author.time,
                'offset': commit.author.offset
            },
            'committer': {
                'name': commit.committer.name,
                'email': commit.committer.email,
                'time': commit.committer.time,
                'offset': commit.committer.offset
            },
            'tree_id': commit.tree_id.hex,
            'commit_time': commit.commit_time,
            'commit_time_offset': commit.commit_time_offset,
            'message': commit.message
        } for commit in repo.walk(repo.head.target)], ensure_ascii=False, indent=4))
