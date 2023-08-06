import json
import os
from typing import List

import pyperclip
import questionary
import typer
from git import Git
from questionary import Style

from .commit_config import CACHE_FILE_PATH, CACHE_NAME, DEFAULT_CACHE, TYPE
from .helper import (safe_process_input, safe_run_command,
                     std_error, std_info, get_parent_folder_path, get_all_gits, get_current_branch)


def save_cached_input(input: dict, parent_folder_path: str, current_branch: str) -> None:
    """保存历史输入"""

    cached_file_path = CACHE_FILE_PATH + CACHE_NAME

    if not os.path.exists(CACHE_FILE_PATH):
        os.mkdir(CACHE_FILE_PATH)

    if not os.path.exists(cached_file_path):
        open(cached_file_path, 'w+').close()

    all_cached_json: dict = None
    try:
        all_cached_json = json.load(open(cached_file_path, 'r'))
    except json.decoder.JSONDecodeError:
        all_cached_json = {}

    with open(cached_file_path, 'w+') as f:
        if parent_folder_path not in all_cached_json:
            all_cached_json[parent_folder_path] = {}
        all_cached_json[parent_folder_path][current_branch] = input
        json.dump(all_cached_json, f)


def get_cached_input(parent_folder_path: str, current_branch: str) -> dict:
    """获取缓存的输入"""

    cached_input = DEFAULT_CACHE
    cached_file_path = CACHE_FILE_PATH + CACHE_NAME

    try:
        all_cached_json = json.load(open(cached_file_path, 'r'))
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        all_cached_json = {}

    if os.path.exists(cached_file_path) and parent_folder_path in all_cached_json and current_branch in all_cached_json[parent_folder_path]:
        cached_input = all_cached_json[parent_folder_path][current_branch]
        for key in DEFAULT_CACHE.keys():
            if key not in cached_input:
                # 版本更新时, 可能缓存中为旧版本的数据, 旧版本没有的数据需要置为空
                cached_input[key] = ''
    else:
        save_cached_input(cached_input, parent_folder_path, current_branch)

    return cached_input


def get_commit_message(cached_input: dict, save: bool = False, parent_folder_path: str = "", current_branch: str = "") -> str:
    """获取 commit message"""

    commit_type_str = cached_input['type'] + ':' + \
        TYPE[cached_input['type']] if cached_input['type'] != '' else ''
    scope = cached_input['scope']
    subject = cached_input['subject']
    body = cached_input['body']
    doc = cached_input['doc']
    commit_message = ''
    while True:
        commit_type_str: str = safe_process_input(questionary.select('请选择你的 commit 类型:', choices=[f'{k}:{v}' for k, v in TYPE.items()],
                                                                     qmark='', instruction='使用↑↓选择', style=Style([
                                                                         ('highlighted',
                                                                             f'fg:{typer.colors.GREEN} bold'),
                                                                         ('instruction',
                                                                             'bold'),
                                                                         ('answer',
                                                                             f'fg:{typer.colors.YELLOW} bold'),
                                                                     ]), default=(None if commit_type_str == '' else commit_type_str)).ask())
        commit_type = commit_type_str.split(':')[0]
        cached_input['type'] = commit_type
        if save:
            save_cached_input(cached_input, parent_folder_path, current_branch)

        scope: str = safe_process_input(questionary.text('请输入改动的范围, 如上线预期版本等信息, 用 - 分割, 可省略\n e.g. 20.0.0-信息流:', qmark='', style=Style([
            ('answer',
                f'fg:{typer.colors.YELLOW} bold')
        ]), default=scope).ask())
        cached_input['scope'] = scope
        if save:
            save_cached_input(cached_input, parent_folder_path, current_branch)

        subject = safe_process_input(questionary.text('请输入本次修改的简洁描述, 如需求名, 修复的Bug等\n e.g. 抖音图文广告:', qmark='', style=Style([
            ('answer',
                f'fg:{typer.colors.YELLOW} bold'),
        ]), default=subject, validate=lambda val: len(val) > 0).ask())
        cached_input['subject'] = subject
        if save:
            save_cached_input(cached_input, parent_folder_path, current_branch)

        body_confirm = safe_process_input(questionary.confirm(
            '是否有额外信息需要补充, 如修改了哪些组件, 有哪些不兼容的修改, 遗留了哪些问题:', qmark='', default=False, style=Style([
                ('answer',
                    f'fg:{typer.colors.YELLOW} bold'),
            ])).ask())

        if body_confirm:
            body = safe_process_input(questionary.text('补充额外信息:', qmark='', multiline=True, instruction='(结束请输入 Esc 然后输入 Enter)\n', style=Style([
                ('answer',
                    f'fg:{typer.colors.YELLOW} bold'),
            ]), default=body).ask()).strip()
            cached_input['body'] = body
            if save:
                save_cached_input(
                    cached_input, parent_folder_path, current_branch)

        doc = safe_process_input(questionary.text('技术文档、Meego链接或Bug链接:', qmark='', style=Style([
            ('answer',
                f'fg:{typer.colors.YELLOW} bold'),
        ]), default=doc).ask()).strip()
        cached_input['doc'] = doc
        if save:
            save_cached_input(cached_input, parent_folder_path, current_branch)

        commit_message = commit_type + \
            ('' if scope == '' else f'({scope})') + ': ' + subject
        if body != '':
            commit_message += f'\n\n{body}\n'
        if doc != '':
            commit_message += f'\ndoc: {doc}'
        all_confirm = safe_process_input(questionary.confirm('确认以上 commit message?', qmark='', default=True, style=Style([
            ('answer',
                f'fg:{typer.colors.YELLOW} bold'),
        ])).ask())
        if all_confirm:
            break
    return commit_message


def commit(message: str = typer.Option('', '--message', '-m', hidden=True),
           multi: bool = typer.Option(
               False, '--gits', '-g', help='多仓创建 commit'),
           clipboard: bool = typer.Option(
               False, '--clipboard', '-c', help='将 commit message 复制到剪切板, 而不产生提交'),
           push: bool = typer.Option(
               False, '--push', '-p', help='创建 commit 后直接push')
           ):
    """用规范的 message 提交 commit"""

    if message != '':
        std_error('禁止使用 --message 提交消息, 请使用本工具生成 commit message!')
        raise typer.Abort()

    if clipboard:
        for k, v in locals().items():
            if not k == 'clipboard' and v:
                std_error(
                    'clipboard 功能仅用于生成 commit message! 请单独使用 --clipboard/-c 参数')
                raise typer.Abort()
        commit_message = get_commit_message(
            cached_input=DEFAULT_CACHE, save=False)
        pyperclip.copy(commit_message)
        std_info('commit 信息已复制到剪切板!')
        raise typer.Exit()

    gits: List[Git] = get_all_gits(multi)
    # 查看此时是否有 changes added to commit
    working_git: List[Git] = []
    for git in gits:
        if git.diff('--name-only', '--cached').strip() != '':
            working_git.append(git)
    if len(working_git) == 0:
        std_error('nothing to commit, working tree clean')
        raise typer.Abort()

    parent_folder_path: str = get_parent_folder_path()
    current_branch: str = get_current_branch(gits, multi)
    # 缓存输入过的信息
    cached_input: dict = get_cached_input(parent_folder_path, current_branch)

    for git in working_git:
        std_info(f'即将 Commit 的仓库:{git.rev_parse("--show-toplevel")}')

    # 生成 commit_message
    commit_message = get_commit_message(
        cached_input=cached_input, save=True, parent_folder_path=parent_folder_path, current_branch=current_branch)

    for git in working_git:
        try:
            safe_run_command(git.commit, '-m', commit_message)
        except typer.Abort():
            continue
        std_info(f'{git.rev_parse("--show-toplevel")} commit 完成!')

    if push:
        for git in working_git:
            try:
                safe_run_command(git.push)
            except typer.Abort():
                continue
            std_info(f'{git.rev_parse("--show-toplevel")} push 完成!')
