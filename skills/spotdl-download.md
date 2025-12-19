# SpotDL 音乐下载 Skill

## 概述

使用 SpotDL 通过 MCP Code Runner 下载音乐。SpotDL 支持从 Spotify、YouTube Music 等平台下载高质量音频文件。

## 前置条件

1. MCP Code Runner 服务器已启动并运行
2. SpotDL 已预装在系统中（已在白名单中）
3. SpotDL 配置文件位于 `/config/spotdl/config.json`（可选，但推荐）

## 配置文件

SpotDL 使用配置文件来设置默认参数。配置文件位置：
- 容器内: `/root/.spotdl/config.json`
- 映射路径: `/config/spotdl/config.json`

**推荐配置**（已预配置）:
- 输出格式: `m4a`（高质量，Jellyfin 兼容）
- 比特率: `disable`（保留原始质量）
- 输出模板: `/data/Music/{artist}/{album}/{track-number} - {title}.{output-ext}`
- 歌词生成: 启用 LRC 歌词文件
- 元数据更新: 强制更新元数据

## 基本下载流程

### 1. 下载单首歌曲

**步骤**:
1. 使用 `run_shell` 执行 spotdl 命令
2. 使用 `deploy_artifacts` 部署下载的文件

**示例**:
```json
// 步骤1: 执行下载
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"
    ]
  }
}

// 步骤2: 部署文件（使用返回的 workdir）
{
  "name": "deploy_artifacts",
  "arguments": {
    "workdir": "/temp/mcp-job-xxxxx"
  }
}
```

### 2. 下载播放列表

**示例**:
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
    ]
  }
}
```

### 3. 使用搜索词下载

**示例**:
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "Never Gonna Give You Up"
    ]
  }
}
```

## 高级用法

### 使用配置文件

如果配置文件已设置好，可以直接使用：
```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "--config",
      "歌曲名称或链接"
    ]
  }
}
```

### 自定义输出格式

```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "--format", "flac",
      "--output", "/data/Music/{artist}/{album}/{track-number} - {title}",
      "歌曲链接或名称"
    ]
  }
}
```

### 下载专辑

```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "--fetch-albums",
      "歌曲链接或名称"
    ]
  }
}
```

### 生成 M3U 播放列表

```json
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "--m3u",
      "播放列表链接"
    ]
  }
}
```

## 完整工作流程示例

### 下载并部署音乐文件

```json
// 1. 检查系统能力
{
  "name": "capabilities"
}

// 2. 执行下载
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": [
      "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"
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

// 4. 部署文件到 /data/Music
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
    "directory": "/data/Music"
  }
}
```

## 常用参数说明

### 输出相关
- `--format {mp3,flac,ogg,opus,m4a,wav}`: 输出格式
- `--output TEMPLATE`: 输出文件命名模板
- `--bitrate {auto,disable,128k,320k}`: 比特率设置

### 元数据相关
- `--force-update-metadata`: 强制更新元数据
- `--generate-lrc`: 生成 LRC 歌词文件
- `--playlist-retain-track-cover`: 保留曲目原始封面

### 下载控制
- `--overwrite {skip,metadata,force}`: 处理已存在文件策略
- `--scan-for-songs`: 扫描输出目录识别已存在文件
- `--archive FILE`: 归档文件，避免重复下载

### 播放列表相关
- `--fetch-albums`: 基于查询中的歌曲补拉对应专辑
- `--m3u [FILE]`: 生成 M3U 播放列表

## 输出文件结构

使用默认配置，文件会按以下结构存放：

```
/data/Music/
└── 艺术家名/
    └── 专辑名/
        ├── 01 - 歌曲A.m4a
        ├── 01 - 歌曲A.lrc  (如果启用)
        ├── 02 - 歌曲B.m4a
        └── 02 - 歌曲B.lrc
```

## 错误处理

### 检查下载是否成功

下载命令返回的 `code` 字段：
- `0`: 成功
- 非 `0`: 失败，查看 `stderr` 获取错误信息

### 常见错误

1. **认证失败**: 检查 Spotify 客户端 ID 和密钥配置
2. **网络错误**: 检查网络连接或代理设置
3. **文件已存在**: 使用 `--overwrite` 参数控制行为

## 最佳实践

1. **使用配置文件**: 预先配置好常用参数，简化命令
2. **检查工作目录**: 下载后先检查临时目录中的文件
3. **及时部署**: 下载完成后立即部署，避免临时文件被清理
4. **验证结果**: 部署后验证文件是否在正确位置
5. **使用归档文件**: 对于播放列表，使用 `--archive` 避免重复下载

## 相关资源

- [SpotDL 官方文档](https://spotdl.readthedocs.io/)
- [SpotDL GitHub](https://github.com/spotDL/spotify-downloader)
- [配置文件指南](../../mcp/config/spotdl-guide.md)

