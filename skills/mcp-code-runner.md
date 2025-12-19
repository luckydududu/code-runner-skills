# MCP Code Runner 使用指南

## 概述

MCP Code Runner 是一个可执行代码的 MCP 服务器，提供了安全的命令行执行环境，支持通过预定义的白名单命令来执行各种任务，特别是用于下载音乐和视频。

## MCP 服务器信息

- **服务器名称**: mcp-code-runner
- **版本**: 0.5.0
- **运行模式**: HTTP/SSE (默认端口 8080) 或 stdio
- **部署根目录**: `/data` - 最终部署产物目录
- **配置目录**: `/config` - 配置文件目录
- **临时目录**: `/temp` - 临时文件目录（会被定期清理）

## 可用工具 (Tools)

### 1. capabilities
查看系统能力信息，包括允许的命令、支持的编程语言、目录结构等。

**参数**: 无

**返回信息**:
- `shell_whitelist`: 允许执行的命令列表
- `supported_languages`: 支持的编程语言
- `deploy_root`: 部署根目录路径
- `config_root`: 配置根目录路径
- `temp_root`: 临时文件根目录路径
- `buckets`: 文件分类桶列表
- `route`: 文件类型到桶的映射关系

**使用示例**:
```json
{
  "name": "capabilities"
}
```

### 2. run_shell
执行白名单中的 shell 命令。

**参数**:
- `cmd` (必需): 要执行的命令，必须在白名单中
- `args` (可选): 命令参数数组，默认为空数组
- `cwd` (可选): 工作目录，相对于临时工作目录

**安全限制**:
- 只能执行白名单中的命令
- 参数中不能包含管道符 `|`、分号 `;`、重定向符 `><` 等特殊字符

**使用示例**:
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": ["--version"]
  }
}
```

### 3. run_python
执行 Python3 代码。

**参数**:
- `code` (必需): 要执行的 Python 代码
- `cwd` (可选): 工作目录，相对于临时工作目录

**使用示例**:
```json
{
  "name": "run_python",
  "arguments": {
    "code": "print('Hello, World!')"
  }
}
```

### 4. deploy_artifacts
将临时工作目录中的文件部署到最终的 `/data` 目录，按文件类型自动分类。

**参数**:
- `workdir` (必需): 临时工作目录的绝对路径（由 run_shell 或 run_python 返回）
- `files` (可选): 要部署的文件列表（相对路径），如果省略则部署所有顶层文件

**文件分类规则**:
- `Book`: .pdf, .epub, .mobi, .txt
- `Image`: .png, .jpg, .jpeg, .gif, .webp, .tif, .tiff
- `Movie`: .mp4, .mov, .mkv, .webm, .avi
- `Music`: .mp3, .wav, .m4a, .aac, .flac, .ogg
- `Shows`: .mp4, .mkv, .webm
- `others`: 其他类型文件

**使用示例**:
```json
{
  "name": "deploy_artifacts",
  "arguments": {
    "workdir": "/temp/mcp-job-xxxxx"
  }
}
```

### 5. read_config
读取 `/config` 目录下的配置文件。

**参数**:
- `file` (必需): 配置文件相对于 `/config` 目录的路径

**使用示例**:
```json
{
  "name": "read_config",
  "arguments": {
    "file": "spotdl/config.json"
  }
}
```

### 6. list_files
列出指定目录下的文件和子目录。

**参数**:
- `directory` (必需): 目录的绝对路径（必须在 `/data`、`/config` 或 `/temp` 下）

**使用示例**:
```json
{
  "name": "list_files",
  "arguments": {
    "directory": "/data/Music"
  }
}
```

### 7. check_file
检查文件是否存在并返回文件信息。

**参数**:
- `file` (必需): 文件的绝对路径（必须在 `/data`、`/config` 或 `/temp` 下）

**使用示例**:
```json
{
  "name": "check_file",
  "arguments": {
    "file": "/data/Music/Artist/Album/01 - Song.m4a"
  }
}
```

## 典型工作流程

### 下载任务的标准流程

1. **执行下载命令**: 使用 `run_shell` 执行下载命令（如 `spotdl` 或 `yt-dlp`）
   - 命令会在临时目录中执行
   - 下载的文件会保存在临时工作目录中

2. **检查下载结果**: 使用 `list_files` 查看临时工作目录中的文件

3. **部署文件**: 使用 `deploy_artifacts` 将文件从临时目录移动到 `/data` 目录
   - 文件会根据扩展名自动分类到对应的桶中
   - 例如：音乐文件会移动到 `/data/Music/` 目录

4. **验证部署**: 使用 `check_file` 或 `list_files` 验证文件已成功部署

## 安全说明

- 所有命令执行都在隔离的临时目录中进行
- 只能执行白名单中的命令，防止恶意代码执行
- 文件访问限制在 `/data`、`/config` 和 `/temp` 目录下
- 参数验证会阻止危险的字符和操作

## 预装工具

系统预装了以下常用工具：
- **spotdl**: 音乐下载工具（支持 Spotify、YouTube Music）
- **yt-dlp**: 视频下载工具（支持 YouTube 等1000+平台）
- **ffmpeg**: 音视频处理工具
- **magick**: ImageMagick 图像处理工具
- 以及其他基础系统命令（ls, cat, echo, pwd 等）

详细的使用说明请参考对应的 skill 文件：
- [SpotDL 音乐下载 Skill](./spotdl-download.md)
- [yt-dlp 视频下载 Skill](./ytdlp-download.md)

