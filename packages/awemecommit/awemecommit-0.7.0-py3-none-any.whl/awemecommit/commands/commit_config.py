from collections import OrderedDict
from pathlib import Path

# 理论上应该搞个模板来解析，为了方便直接硬编码了
# <type>: <subject>
# <BLANK LINE>
# <body>
# <BLANK LINE>
# <doc>

TYPE: OrderedDict = OrderedDict({
    'feat': '增加新的Feature',
    'fix': '修复Bug',
    'pref': '提高性能的代码更改',
    'refactor': '既不是修复bug也不是增加新Feature的代码重构',
    'style': '不影响代码含义的修改, 比如空格、格式化、缺失的分号等',
    'test': '增加确实的测试或者矫正已存在的测试',
    'docs': '仅对注释的修改',
    'build': '对构建系统或者外部依赖项进行了修改',
    'ci': '对CI配置文件或脚本进行了修改',
    'chore': '不修改 src 或者 test 的其余修改（一些苦力活），例如辅助工具的变动',
    'revert': '回滚到某个 commit 的提交'
})

# 缓存路径
CACHE_FILE_PATH = str(Path.home()) + '/Library/Caches/awemecommit'
CACHE_NAME = '/awemecommit_cache.json'

# 缓存
DEFAULT_CACHE = {
    'type': '',
    'scope': '',
    'subject': '',
    'body': '',
    'doc': ''
}
