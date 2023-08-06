# `awemecommit`

commit message 辅助工具

**Usage**:

```console
$ awemecommit [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `commit`: 用规范的 message 提交 commit
* `owncommit`: 查看目前分支上所有新增的 commit, 但不包含 merge 来的

## `awemecommit commit`

用规范的 message 提交 commit

**Usage**:

```console
$ awemecommit commit [OPTIONS]
```

**Options**:

* `-g, --gits`: 多仓创建 commit  [default: False]
* `-c, --clipboard`: 将 commit message 复制到剪切板  [default: False]
* `-p, --push`: 创建 commit 后直接push  [default: False]
* `--help`: Show this message and exit.

## `awemecommit owncommit`

查看目前分支上所有新增的 commit, 但不包含 merge 来的

**Usage**:

```console
$ awemecommit owncommit [OPTIONS]
```

**Options**:

* `-b, --branch TEXT`: 作比较的分支  [default: develop]
* `--help`: Show this message and exit.
