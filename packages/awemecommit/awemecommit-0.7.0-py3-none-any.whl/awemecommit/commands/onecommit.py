import pydoc

import typer
from git import Repo

from .helper import (safe_run_command, std_error, get_top_git_path)


def owncommit(branch: str = typer.Option('develop', '--branch', '-b', help='作比较的分支')):
    """查看目前分支上所有新增的 commit, 但不包含 merge 来的"""
    top_git_path = get_top_git_path()
    if not top_git_path:
        std_error('不在 git 目录中!')
        raise typer.Abort()
    git = Repo(top_git_path).git
    current_branch = git.branch('--show-current')
    pydoc.pager(safe_run_command(
        git.log, f'{branch}..{current_branch}', '--first-parent', '--no-merges'))
