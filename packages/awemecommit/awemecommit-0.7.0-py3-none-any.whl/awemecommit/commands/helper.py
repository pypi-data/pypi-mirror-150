import os
import subprocess
from typing import List, Optional

import typer
from git import Git
from git.repo import Repo


def safe_process_input(input: Optional[str]) -> str:
    """安全的处理输入, 避免 Ctrl + c"""

    if input is None:
        raise typer.Abort()
    else:
        return input


def safe_run_command(function, *args, **kwargs):
    """安全的运行命令, 特别是避免 git 命令出错"""

    try:
        return function(*args, **kwargs)
    except Exception as e:
        typer.secho(e.stdout,
                    fg=typer.colors.RED, err=True)
        typer.secho(e.stderr,
                    fg=typer.colors.RED, err=True)
        typer.secho(f"{function} 出错, 请查看以上报错信息",
                    fg=typer.colors.RED, err=True)
        raise typer.Abort()


def std_info(info: str) -> None:
    typer.secho(info, fg=typer.colors.GREEN)


def std_warning(warning: str) -> None:
    typer.secho(warning, fg=typer.colors.YELLOW)


def std_error(error: str) -> None:
    typer.secho(error, fg=typer.colors.RED, err=True)


def get_top_git_path(path: Optional[str] = None) -> Optional[str]:
    """获取当前目录下的 git 目录"""

    current_path = os.getcwd()
    if path:
        os.chdir(path)
    top_git_path = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'], capture_output=True).stdout.decode().strip()
    if path:
        os.chdir(current_path)
    if top_git_path == '':
        return None
    else:
        return top_git_path


def get_parent_folder_path() -> str:
    """获取父目录路径, 如果处在子仓下, 则返回子仓父目录, 否则返回当前目录"""

    # 可能在子仓下，也可能在多仓目录下
    parent_folder_path = None
    if top_git_path := get_top_git_path():
        # 如果在子仓下，则返回子仓父目录
        parent_folder_path = os.path.dirname(top_git_path)
    else:
        # 否则返回当前目录
        parent_folder_path = os.getcwd()
    return parent_folder_path


def get_all_gits(multi: bool) -> List[Git]:
    """获取当前目录下可能的 git"""

    top_git_path = get_top_git_path()
    if not multi:
        # 单仓操作
        if not top_git_path:
            std_error('不在 git 目录中!')
            raise typer.Abort()
        elif Repo(top_git_path).git.branch('--show-current') == '':
            std_error(f'{top_git_path} HEAD is Detected, 请检查后操作')
            raise typer.Abort()
        else:
            return [Repo(top_git_path).git]
    else:
        paths: List[str] = []
        for path in [f.path for f in os.scandir(get_parent_folder_path()) if f.is_dir()]:
            if get_top_git_path(path) == path:
                paths.append(path)
        if not paths:
            std_error('无法找到 Git 仓库')
            raise typer.Abort()

        gits: List[Git] = []
        for path in paths:
            if Repo(path).git.branch('--show-current') == '':
                std_warning(f'{path} HEAD is Detected, 请单独操作!')
            else:
                gits.append(Repo(path).git)
        return gits


def get_current_branch(gits: List[Git], multi: bool) -> str:
    """获取当前分支"""

    if not gits:
        std_error('未能获取 git 目录')
        raise typer.Abort()

    current_branch = None
    if multi:
        # 检查多仓 branch 是否同步
        for git in gits:
            possible_branch = git.branch('--show-current')
            if not current_branch:
                current_branch = possible_branch
            elif current_branch != possible_branch:
                std_error('多仓分支不一致, 请检查')
                raise typer.Abort()
    else:
        current_branch = gits[0].branch('--show-current')

    return current_branch
