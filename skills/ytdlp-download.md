# yt-dlp 视频下载 Skill

## 概述

使用 yt-dlp 通过 MCP Code Runner 下载视频和音频。yt-dlp 支持从 YouTube 和其他1000多个视频平台下载内容。

## 前置条件

1. MCP Code Runner 服务器已启动并运行
2. yt-dlp 已预装在系统中（已在白名单中）
3. ffmpeg 已安装（用于视频/音频处理）

## 基本下载流程

### 1. 下载视频

**步骤**:
1. 使用 `run_shell` 执行 yt-dlp 命令
2. 使用 `deploy_artifacts` 部署下载的文件

**示例**:
```json
// 步骤1: 执行下载
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

// 步骤2: 部署文件
{
  "name": "deploy_artifacts",
  "arguments": {
    "workdir": "/temp/mcp-job-xxxxx"
  }
}
```

### 2. 仅下载音频

**示例**:
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

### 3. 下载播放列表

**示例**:
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

## 高级用法

### 自定义输出路径和命名

```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "-o", "/data/Movie/%(uploader)s/%(title)s.%(ext)s",
      "-f", "bv*+ba/best",
      "视频URL"
    ]
  }
}
```

### 下载字幕

```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "--write-subs",
      "--sub-langs", "en,zh-*",
      "--embed-subs",
      "视频URL"
    ]
  }
}
```

### 下载缩略图和信息文件

```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "--write-thumbnail",
      "--write-info-json",
      "--skip-download",
      "视频URL"
    ]
  }
}
```

### 使用代理

```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "--proxy", "http://127.0.0.1:7890",
      "视频URL"
    ]
  }
}
```

### 限速下载

```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "-r", "4M",
      "视频URL"
    ]
  }
}
```

## 完整工作流程示例

### 下载视频并部署

```json
// 1. 检查系统能力
{
  "name": "capabilities"
}

// 2. 执行下载
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "-f", "bv*+ba/best",
      "-o", "%(title)s.%(ext)s",
      "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ]
  }
}
// 返回: { "code": 0, "stdout": "...", "stderr": "", "workdir": "/temp/mcp-job-xxxxx" }

// 3. 检查下载的文件
{
  "name": "list_files",
  "arguments": {
    "directory": "/temp/mcp-job-xxxxx"
  }
}

// 4. 部署文件到 /data/Movie
{
  "name": "deploy_artifacts",
  "arguments": {
    "workdir": "/temp/mcp-job-xxxxx"
  }
}

// 5. 验证部署结果
{
  "name": "list_files",
  "arguments": {
    "directory": "/data/Movie"
  }
}
```

### 下载音频到音乐目录

```json
// 1. 下载音频
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "-x",
      "--audio-format", "m4a",
      "--audio-quality", "0",
      "-o", "%(title)s.%(ext)s",
      "https://www.youtube.com/watch?v=xxxxx"
    ]
  }
}

// 2. 部署到音乐目录（会自动分类到 /data/Music）
{
  "name": "deploy_artifacts",
  "arguments": {
    "workdir": "/temp/mcp-job-xxxxx"
  }
}
```

## 常用参数说明

### 格式选择
- `-f, --format FORMAT`: 选择视频/音频格式
  - `bv*+ba/best`: 最佳视频+最佳音频，合并
  - `best`: 最佳单一格式
  - `worst`: 最差质量（用于快速测试）

### 输出控制
- `-o, --output TEMPLATE`: 输出文件命名模板
  - `%(title)s`: 视频标题
  - `%(uploader)s`: 上传者名称
  - `%(ext)s`: 文件扩展名
  - `%(id)s`: 视频ID

### 音频提取
- `-x, --extract-audio`: 仅提取音频
- `--audio-format FORMAT`: 音频格式 (mp3, m4a, opus, flac, wav)
- `--audio-quality QUALITY`: 音频质量 (0-10 或 kbps)

### 字幕相关
- `--write-subs`: 下载字幕
- `--write-auto-subs`: 下载自动生成的字幕
- `--sub-langs LANGS`: 字幕语言 (如 "en,zh-*")
- `--sub-format FORMAT`: 字幕格式 (srt, ass, vtt)
- `--embed-subs`: 将字幕嵌入到视频文件

### 播放列表控制
- `--playlist-start NUMBER`: 播放列表起始序号
- `--playlist-end NUMBER`: 播放列表结束序号
- `--playlist-items ITEMS`: 指定项 (如 "1,2,5-10")
- `--max-downloads N`: 最多下载 N 个条目

### 网络相关
- `--proxy URL`: 设置代理
- `-r, --limit-rate RATE`: 限速 (如 "4M")
- `--retries N`: 失败重试次数

### 文件系统
- `--no-overwrites`: 不覆盖已存在文件
- `--continue`: 断点续传
- `--no-mtime`: 不设置文件修改时间

## 输出文件结构

### 视频文件
使用默认配置，视频文件会存放在：
```
/data/Movie/
└── 视频文件名.mp4
```

### 音频文件
音频文件会存放在：
```
/data/Music/
└── 音频文件名.m4a
```

### 自定义结构
如果使用自定义输出模板：
```json
{
  "args": [
    "-o", "/data/Movie/%(uploader)s/%(title)s.%(ext)s",
    "URL"
  ]
}
```

结果：
```
/data/Movie/
└── 上传者名/
    └── 视频标题.mp4
```

## 错误处理

### 检查下载是否成功

下载命令返回的 `code` 字段：
- `0`: 成功
- 非 `0`: 失败，查看 `stderr` 获取错误信息

### 常见错误

1. **格式不可用**: 尝试使用 `-f best` 或 `-f worst`
2. **网络错误**: 检查网络连接或使用代理
3. **权限错误**: 检查输出目录权限
4. **磁盘空间不足**: 检查可用磁盘空间

### 调试技巧

使用 `--verbose` 参数获取详细日志：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "yt-dlp",
    "args": [
      "--verbose",
      "URL"
    ]
  }
}
```

## 最佳实践

1. **选择合适的格式**: 根据需求选择视频或仅音频
2. **使用输出模板**: 统一文件命名和组织结构
3. **下载字幕**: 对于需要字幕的视频，使用 `--write-subs`
4. **检查文件大小**: 下载前使用 `-F` 列出格式，了解文件大小
5. **及时部署**: 下载完成后立即部署，避免临时文件被清理
6. **使用代理**: 如果网络不稳定，配置代理提高成功率

## 格式选择建议

### 高质量视频
```json
{
  "args": ["-f", "bv*+ba/best", "URL"]
}
```

### 中等质量（节省空间）
```json
{
  "args": ["-f", "best[height<=720]", "URL"]
}
```

### 仅音频（高质量）
```json
{
  "args": ["-x", "--audio-format", "m4a", "--audio-quality", "0", "URL"]
}
```

### 仅音频（压缩）
```json
{
  "args": ["-x", "--audio-format", "mp3", "--audio-quality", "192K", "URL"]
}
```

## 相关资源

- [yt-dlp 官方文档](https://github.com/yt-dlp/yt-dlp)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [配置文件指南](../../mcp/config/yt-dlp-guide.md)

