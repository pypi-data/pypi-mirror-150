from typing import Iterable

import typer
from click import Context, Group


from .commands.onecommit import owncommit
from .commands.commit import commit


class OrderedCommands(Group):
    def list_commands(self, ctx: Context) -> Iterable[str]:
        # 修改command默认顺序
        return ['commit', 'owncommit', 'pullrebase']


app = typer.Typer(cls=OrderedCommands, help='commit message 辅助工具')

app.command(help='用规范的 message 提交 commit')(commit)
app.command(help='查看目前分支上所有新增的 commit, 但不包含 merge 来的')(owncommit)


if __name__ == '__main__':
    app()
