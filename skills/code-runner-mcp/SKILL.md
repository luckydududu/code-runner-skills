---
name: code-runner-mcp
description: 通过 MCP 服务器执行受限的命令行操作和代码，支持使用 spotdl 下载音乐和使用 yt-dlp 下载视频。所有文件存储在挂载到主机的 /data 目录中。
version: 0.6.0
author: dev@qiaobo.me
tags:
  - mcp
  - command-execution
  - music-download
  - video-download
  - music-metadata
  - jellyfin
  - musicbrainz
  - spotdl
  - yt-dlp
---

# Code Runner MCP Skill

## 概述

该技能提供了一个基于 MCP (Model Context Protocol) 的可执行代码服务器，允许在受控环境中执行命令行操作和代码。系统采用白名单机制，只允许执行预定义的安全命令，确保系统安全。主要功能包括：

- **受限命令执行**：通过白名单机制执行安全的命令行工具
- **代码执行**：支持执行 Python3 代码
- **音乐下载**：使用 spotdl 从 Spotify 和 YouTube Music 下载音乐
- **视频下载**：使用 yt-dlp 从 YouTube 等1000+平台下载视频
- **音乐元数据管理**：自动生成 Jellyfin 兼容的 NFO 文件，包含 MusicBrainz ID
- **文件管理**：自动将下载的文件分类并存储到 `/data` 目录（挂载到主机）

## 前置条件

- MCP 服务器已启动并运行（默认 HTTP/SSE 模式，端口 8080）
- `/data` 目录已挂载到主机，确保文件持久化
- 网络连接正常（用于下载音乐和视频）

## 工具版本

### spotdl
- **版本**: 4.4.3
- **用途**: 从 Spotify、YouTube Music 等平台下载音乐
- **官方文档**: [SpotDL GitHub](https://github.com/spotDL/spotify-downloader)

### yt-dlp
- **版本**: 最新版本（已明确安装）
- **用途**: 从 YouTube 和其他1000+视频平台下载视频和音频
- **官方文档**: [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)

### ImageMagick (magick)
- **版本**: 7.1.2-11（从源码编译，启用全部特性）
- **用途**: 图像处理、格式转换、尺寸调整、滤镜应用等
- **官方文档**: [ImageMagick Documentation](https://imagemagick.org/script/command-line-processing.php)

## 命令行白名单

系统采用白名单机制，只允许执行以下命令：

**默认白名单**（可通过环境变量 `SHELL_WHITELIST` 覆盖）：
- 基础命令: `ls`, `cat`, `echo`, `pwd`, `whoami`
- 文件操作: `cp`, `mv`, `mkdir`, `touch`, `find`, `which`, `type`, `file`, `stat`, `basename`, `dirname`
- 文本处理: `grep`, `sed`, `awk`, `sort`, `uniq`, `head`, `tail`, `wc`, `cut`, `tr`
- 压缩工具: `tar`, `gzip`, `gunzip`, `zip`, `unzip`
- 网络工具: `curl`, `wget`, `ping`, `nslookup`
- 系统监控: `df`, `du`, `free`, `ps`, `top`, `uptime`, `date`, `uname`
- 媒体工具: `ffmpeg`, `magick` (ImageMagick - 图像处理工具)
- **下载工具**: `spotdl` (音乐下载), `yt-dlp` (视频下载)

**安全限制**：
- 只能执行白名单中的命令
- 参数中不能包含管道符 `|`、分号 `;`、重定向符 `><` 等特殊字符
- 所有命令在隔离的临时目录中执行

## MCP 工具说明

### 1. capabilities
查看系统能力信息。

**使用方式**：
```json
{
  "name": "capabilities"
}
```

**返回信息**：
- `shell_whitelist`: 允许执行的命令列表
- `supported_languages`: 支持的编程语言（Python3）
- `deploy_root`: 部署根目录路径（`/data`）
- `buckets`: 文件分类桶列表

### 2. run_shell
执行白名单中的 shell 命令。

**参数**：
- `cmd` (必需): 要执行的命令，必须在白名单中
- `args` (可选): 命令参数数组
- `cwd` (可选): 工作目录，相对于临时工作目录

**使用示例**：
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

**参数**：
- `code` (必需): 要执行的 Python 代码
- `cwd` (可选): 工作目录

**使用示例**：
```json
{
  "name": "run_python",
  "arguments": {
    "code": "print('Hello, World!')"
  }
}
```

### 4. deploy_artifacts
将临时工作目录中的文件部署到 `/data` 目录，按文件类型自动分类。

**参数**：
- `workdir` (必需): 临时工作目录的绝对路径（由 run_shell 或 run_python 返回）
- `files` (可选): 要部署的文件列表（相对路径），如果省略则部署所有顶层文件

**文件分类规则**：
- `Music`: .mp3, .wav, .m4a, .aac, .flac, .ogg
- `Movie`: .mp4, .mov, .mkv, .webm, .avi
- `Image`: .png, .jpg, .jpeg, .gif, .webp, .tif, .tiff
- `Book`: .pdf, .epub, .mobi, .txt
- `Shows`: .mp4, .mkv, .webm
- `others`: 其他类型文件

**使用示例**：
```json
{
  "name": "deploy_artifacts",
  "arguments": {
    "workdir": "/temp/mcp-job-xxxxx"
  }
}
```

### 5. list_files
列出指定目录下的文件和子目录。

**参数**：
- `directory` (必需): 目录的绝对路径（必须在 `/data`、`/config` 或 `/temp` 下）

### 6. check_file
检查文件是否存在并返回文件信息。

**参数**：
- `file` (必需): 文件的绝对路径

### 7. read_config
读取 `/config` 目录下的配置文件。

**参数**：
- `file` (必需): 配置文件相对于 `/config` 目录的路径

### 8. generate_music_nfo
为音乐专辑生成 Jellyfin 兼容的 NFO 文件。自动从音乐文件中提取元数据，查询 MusicBrainz API 获取 MusicBrainz ID，并生成包含完整元数据的 NFO 文件。

**参数**：
- `file` (可选): 单个音乐文件路径（必须在 `/data` 目录下）。NFO 文件将生成在该文件所在的专辑目录中
- `directory` (可选): 包含音乐文件的目录路径（必须在 `/data` 目录下）。NFO 文件将生成在该目录中

**注意**：`file` 和 `directory` 参数必须提供其中一个，不能同时提供。

**功能说明**：
- 自动从音乐文件中提取元数据（标题、艺术家、专辑、日期等）
- 查询 MusicBrainz API 获取 MusicBrainz ID（专辑 ID、专辑艺术家 ID 等）
- 如果 MusicBrainz 查询失败，使用文件中的元数据作为备选
- 生成符合 Jellyfin 格式的 XML NFO 文件（`album.nfo`）
- 支持多种音频格式：MP3、FLAC、M4A、AAC、OGG、WAV

**使用示例 - 处理单个文件**：
```json
{
  "name": "generate_music_nfo",
  "arguments": {
    "file": "/data/Music/Artist/Album/01 - Song.m4a"
  }
}
```

**使用示例 - 批量处理目录**：
```json
{
  "name": "generate_music_nfo",
  "arguments": {
    "directory": "/data/Music/Artist/Album"
  }
}
```

**返回结果**：
```json
{
  "success": true,
  "nfo_file": "/data/Music/Artist/Album/album.nfo",
  "album_metadata": {
    "title": "Album Title",
    "artist": "Album Artist",
    "date": "2024",
    "musicbrainz_albumid": "xxx-xxx-xxx",
    "musicbrainz_albumartistid": "yyy-yyy-yyy"
  },
  "processed_files": [
    "/data/Music/Artist/Album/01 - Song.m4a",
    "/data/Music/Artist/Album/02 - Song2.m4a"
  ],
  "errors": null
}
```

## 使用 spotdl 下载音乐

### 基本用法

**重要提示**：推荐使用 `--config` 参数来使用预配置的配置文件，这样可以自动应用最佳设置（格式、输出路径等）。

**使用配置文件下载（推荐）**：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "--config",
      "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"
    ]
  }
}
```

**使用配置文件下载播放列表**：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "--config",
      "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
    ]
  }
}
```

**使用配置文件通过搜索词下载**：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "--config",
      "Never Gonna Give You Up"
    ]
  }
}
```

**不使用配置文件（直接下载）**：
如果不需要使用配置文件，可以直接提供链接或搜索词：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"
    ]
  }
}
```

### spotdl 版本信息
- **版本**: 4.4.3
- **配置文件位置**: `/root/.spotdl/config.json`（已预配置）
- **默认输出格式**: m4a（高质量，Jellyfin 兼容）
- **默认输出路径**: `/data/Music/{artist}/{album}/{track-number} - {title}.{output-ext}`

> 📖 **详细使用指南**: 请参考 [SpotDL 使用指南](./spotdl-guide.md) 获取完整的命令行参数、配置选项和高级用法说明。

### 完整工作流程

1. **执行下载命令**（推荐使用 `--config` 参数）：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "--config",
      "歌曲链接或搜索词"
    ]
  }
}
```
返回结果包含 `workdir` 字段，例如：`/temp/mcp-job-xxxxx`

2. **检查下载结果**：
```json
{
  "name": "list_files",
  "arguments": {
    "directory": "/temp/mcp-job-xxxxx"
  }
}
```

3. **部署文件到 /data 目录**：
```json
{
  "name": "deploy_artifacts",
  "arguments": {
    "workdir": "/temp/mcp-job-xxxxx"
  }
}
```

4. **验证部署结果**：
```json
{
  "name": "list_files",
  "arguments": {
    "directory": "/data/Music"
  }
}
```

5. **生成 NFO 文件（可选，用于 Jellyfin 元数据刮削）**：
```json
{
  "name": "generate_music_nfo",
  "arguments": {
    "directory": "/data/Music/Artist/Album"
  }
}
```

这将生成 `album.nfo` 文件，包含完整的专辑元数据和 MusicBrainz ID，Jellyfin 可以自动识别并使用这些信息进行元数据刮削。

## 使用 yt-dlp 下载视频

### 基本用法

**下载视频**：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "-f", "bv*+ba/best",
      "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ]
  }
}
```

**仅下载音频**：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "-x",
      "--audio-format", "m4a",
      "--audio-quality", "0",
      "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ]
  }
}
```

**下载播放列表**：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "-f", "bv*+ba/best",
      "https://www.youtube.com/playlist?list=PLxxxxx"
    ]
  }
}
```

### yt-dlp 版本信息
- **版本**: 最新版本（已明确安装）
- **支持平台**: YouTube 和其他1000+视频平台
- **功能**: 支持视频、音频、字幕下载

> 📖 **详细使用指南**: 请参考 [yt-dlp 使用指南](./yt-dlp-guide.md) 获取完整的命令行参数、配置选项和高级用法说明。

### 常用参数

- `-f, --format FORMAT`: 选择格式（如 `bv*+ba/best` 表示最佳视频+音频）
- `-x, --extract-audio`: 仅提取音频
- `--audio-format FORMAT`: 音频格式（mp3, m4a, opus, flac, wav）
- `--audio-quality QUALITY`: 音频质量（0-10 或 kbps）
- `-o, --output TEMPLATE`: 输出文件命名模板
- `--write-subs`: 下载字幕
- `--sub-langs LANGS`: 字幕语言（如 "en,zh-*"）

### 完整工作流程

与 spotdl 相同的工作流程：
1. 使用 `run_shell` 执行 yt-dlp 命令
2. 使用 `list_files` 检查下载结果
3. 使用 `deploy_artifacts` 部署文件
4. 使用 `list_files` 验证部署结果

## 生成音乐 NFO 文件（Jellyfin 元数据）

### 功能说明

`generate_music_nfo` 工具可以为音乐专辑自动生成 Jellyfin 兼容的 NFO 文件。这个功能类似于 Jellyfin 的元数据刮削，但可以预先生成 NFO 文件，确保 Jellyfin 能够正确识别音乐文件的元数据。

### 主要特性

- **自动元数据提取**：从音乐文件中提取标题、艺术家、专辑、日期等信息
- **MusicBrainz 集成**：自动查询 MusicBrainz API 获取 MusicBrainz ID
  - 专辑 MusicBrainz ID (`musicbrainzalbumid`)
  - 专辑艺术家 MusicBrainz ID (`musicbrainzalbumartistid`)
- **降级处理**：如果 MusicBrainz 查询失败，使用文件中的元数据作为备选
- **Jellyfin 兼容**：生成的 NFO 文件完全符合 Jellyfin 的格式要求
- **批量处理**：支持处理整个专辑目录中的所有音乐文件

### 基本用法

**为单个音乐文件所在的专辑生成 NFO**：
```json
{
  "name": "generate_music_nfo",
  "arguments": {
    "file": "/data/Music/Artist/Album/01 - Song.m4a"
  }
}
```

**为整个专辑目录生成 NFO**：
```json
{
  "name": "generate_music_nfo",
  "arguments": {
    "directory": "/data/Music/Artist/Album"
  }
}
```

### NFO 文件格式

生成的 `album.nfo` 文件包含以下信息：
- `<title>`: 专辑标题
- `<artist>`: 专辑艺术家
- `<musicbrainzalbumid>`: 专辑 MusicBrainz ID
- `<musicbrainzalbumartistid>`: 专辑艺术家 MusicBrainz ID
- `<releasedate>`: 发行日期

### 工作流程示例

1. **下载音乐**（使用 spotdl）：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": ["--config", "歌曲链接"]
  }
}
```

2. **部署文件到 /data**：
```json
{
  "name": "deploy_artifacts",
  "arguments": {
    "workdir": "/temp/mcp-job-xxxxx"
  }
}
```

3. **生成 NFO 文件**：
```json
{
  "name": "generate_music_nfo",
  "arguments": {
    "directory": "/data/Music/Artist/Album"
  }
}
```

4. **验证 NFO 文件**：
```json
{
  "name": "check_file",
  "arguments": {
    "file": "/data/Music/Artist/Album/album.nfo"
  }
}
```

### 技术细节

- **支持的音频格式**：MP3、FLAC、M4A、AAC、OGG、WAV
- **元数据提取**：使用 `mutagen` 库读取音频文件标签
- **MusicBrainz API**：使用 `musicbrainzngs` 库查询 MusicBrainz 数据库
- **NFO 文件位置**：生成在专辑目录下，文件名为 `album.nfo`
- **错误处理**：如果某个文件处理失败，会继续处理其他文件，并在返回结果中报告错误

### 注意事项

- NFO 文件必须与音乐文件在同一目录下，Jellyfin 才能正确识别
- MusicBrainz API 有访问频率限制，批量处理大量专辑时请注意
- 如果音乐文件的元数据不完整，可能无法在 MusicBrainz 中找到匹配项
- 生成的 NFO 文件会覆盖同名的现有文件

## 使用 ImageMagick (magick) 处理图像

### 基本用法

ImageMagick 是一个强大的图像处理工具集，支持超过200种图像格式的读取、写入和转换。

**查看图像信息**：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "magick",
    "args": [
      "identify",
      "/data/Image/example.jpg"
    ]
  }
}
```

**格式转换**：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "magick",
    "args": [
      "/data/Image/input.png",
      "-quality", "85",
      "/data/Image/output.jpg"
    ]
  }
}
```

**尺寸调整**：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "magick",
    "args": [
      "-resize", "800x600",
      "/data/Image/input.jpg",
      "/data/Image/output.jpg"
    ]
  }
}
```

### ImageMagick 版本信息
- **版本**: 7.1.2-11（从源码编译，启用全部特性）
- **可执行文件**: `/usr/local/bin/magick`
- **支持格式**: 超过200种图像格式
- **主要功能**: 格式转换、尺寸调整、滤镜应用、图像合成等

> 📖 **详细使用指南**: 请参考 [ImageMagick 使用指南](./imagemagick-guide.md) 获取完整的命令参数、使用示例和高级功能说明。

## 文件存储说明

### /data 目录挂载

- **容器内路径**: `/data`
- **挂载方式**: 通过 Docker volume 挂载到主机
- **文件持久化**: 所有存储在 `/data` 目录的文件都会在主机上生效
- **自动分类**: 文件会根据扩展名自动分类到对应的子目录（Music、Movie、Image 等）

### 文件组织结构

下载的音乐文件会按照以下结构存储：
```
/data/Music/
└── 艺术家名/
    └── 专辑名/
        ├── 01 - 歌曲A.m4a
        ├── 02 - 歌曲B.m4a
        └── album.nfo  (使用 generate_music_nfo 生成)
```

视频文件会存储在：
```
/data/Movie/
└── 视频文件名.mp4
```

## 安全说明

- ✅ **白名单机制**: 只允许执行预定义的安全命令
- ✅ **路径隔离**: 文件访问限制在 `/data`、`/config` 和 `/temp` 目录下
- ✅ **参数验证**: 防止命令注入攻击
- ✅ **临时目录**: 所有命令执行都在隔离的临时目录中进行

## 错误处理

### 检查命令执行结果

所有 `run_shell` 和 `run_python` 命令返回的结果包含：
- `code`: 返回码（0 表示成功，非 0 表示失败）
- `stdout`: 标准输出
- `stderr`: 标准错误输出
- `workdir`: 临时工作目录路径

### 常见错误

1. **命令不在白名单**: 检查命令是否在白名单中
2. **网络错误**: 检查网络连接
3. **文件不存在**: 检查文件路径是否正确
4. **权限错误**: 检查目录权限

## 参考资源

### 工具详细使用指南

- 📖 [SpotDL 使用指南](./spotdl-guide.md) - 完整的命令行参数、配置选项、Jellyfin 兼容性说明
- 📖 [yt-dlp 使用指南](./yt-dlp-guide.md) - 完整的命令行参数、格式选择、字幕下载等高级功能
- 📖 [ImageMagick 使用指南](./imagemagick-guide.md) - 图像处理、格式转换、滤镜应用等完整说明

### 官方文档

- [Agent Skills 规范](https://agentskills.io/home)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [SpotDL 官方文档](https://github.com/spotDL/spotify-downloader)
- [yt-dlp 官方文档](https://github.com/yt-dlp/yt-dlp)
- [ImageMagick 官方文档](https://imagemagick.org/script/command-line-processing.php)

