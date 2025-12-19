# Code Runner MCP - 可执行代码的 MCP 服务器

一个基于 MCP (Model Context Protocol) 的可执行代码服务器，提供安全的命令行执行环境，特别适用于通过 AI 远程执行音乐和视频下载任务。

## 项目概述

本项目包含：
1. **MCP 服务器**: 提供安全的代码执行环境，支持执行预定义白名单中的命令
2. **预装工具**: 包含 spotdl（音乐下载）、yt-dlp（视频下载）、ffmpeg（音视频处理）等工具
3. **Skills 描述**: 详细的技能描述文件，指导 AI 如何使用 MCP 服务器执行任务

## 项目结构

```
code-runner-mcp/
├── mcp/                    # MCP 服务器代码
│   ├── src/
│   │   └── server.py       # MCP 服务器主程序
│   ├── config/             # 配置文件目录
│   │   ├── spotdl/         # SpotDL 配置
│   │   ├── yt-dlp/         # yt-dlp 配置
│   │   └── *.md            # 工具使用指南
│   ├── docker-compose.yaml # Docker Compose 配置
│   └── build.sh            # 构建脚本
├── skills/                  # Skills 描述文件
│   ├── mcp-code-runner.md  # MCP 使用指南
│   ├── spotdl-download.md  # SpotDL 下载技能
│   ├── ytdlp-download.md  # yt-dlp 下载技能
│   └── README.md           # Skills 说明
└── README.md               # 本文件
```

## 核心功能

### MCP 服务器功能

- **安全执行**: 白名单机制，只允许执行预定义的安全命令
- **隔离环境**: 所有命令在临时目录中执行，确保系统安全
- **文件管理**: 自动将下载的文件分类到对应的目录（Music、Movie、Image 等）
- **工具支持**: 
  - `run_shell`: 执行 shell 命令
  - `run_python`: 执行 Python 代码
  - `deploy_artifacts`: 部署文件到最终目录
  - `read_config`: 读取配置文件
  - `list_files`: 列出目录文件
  - `check_file`: 检查文件信息
  - `capabilities`: 查看系统能力

### 预装工具

- **spotdl**: 音乐下载工具（支持 Spotify、YouTube Music）
- **yt-dlp**: 视频下载工具（支持 YouTube 等1000+平台）
- **ffmpeg**: 音视频处理工具
- **ImageMagick**: 图像处理工具
- 其他基础系统命令

## 快速开始

### 1. 构建 Docker 镜像

```bash
cd mcp
./build.sh
```

### 2. 启动服务

```bash
docker-compose up -d
```

### 3. 使用 MCP 服务器

MCP 服务器默认运行在 HTTP/SSE 模式，端口 8080。

## 使用示例

### 通过 AI 使用

AI 可以通过阅读 `skills/` 目录下的描述文件来学习如何使用 MCP 服务器：

1. **下载音乐**:
   - 参考 `skills/spotdl-download.md`
   - 使用 `run_shell` 执行 `spotdl` 命令
   - 使用 `deploy_artifacts` 部署文件

2. **下载视频**:
   - 参考 `skills/ytdlp-download.md`
   - 使用 `run_shell` 执行 `yt-dlp` 命令
   - 使用 `deploy_artifacts` 部署文件

### 典型工作流程

```json
// 1. 执行下载命令
{
  "name": "run_shell",
  "arguments": {
    "cmd": "spotdl",
    "args": ["歌曲链接或名称"]
  }
}

// 2. 部署文件
{
  "name": "deploy_artifacts",
  "arguments": {
    "workdir": "/temp/mcp-job-xxxxx"
  }
}
```

## 目录结构说明

- `/data`: 最终部署产物目录，按文件类型分类
  - `Music/`: 音乐文件
  - `Movie/`: 视频文件
  - `Image/`: 图像文件
  - `Book/`: 电子书
  - `Shows/`: 剧集
  - `others/`: 其他类型文件

- `/config`: 配置文件目录
  - `spotdl/config.json`: SpotDL 配置
  - `yt-dlp/`: yt-dlp 配置
  - `*.md`: 工具使用指南

- `/temp`: 临时文件目录（会被定期清理）

## 安全特性

- ✅ 白名单机制：只允许执行预定义的安全命令
- ✅ 路径隔离：文件访问限制在指定目录
- ✅ 参数验证：防止命令注入攻击
- ✅ 临时目录：所有操作在隔离的临时目录中进行

## Skills 描述文件

详细的技能描述文件位于 `skills/` 目录：

- **[mcp-code-runner.md](skills/mcp-code-runner.md)**: MCP 服务器完整使用指南
- **[spotdl-download.md](skills/spotdl-download.md)**: SpotDL 音乐下载技能
- **[ytdlp-download.md](skills/ytdlp-download.md)**: yt-dlp 视频下载技能

## 配置说明

### SpotDL 配置

配置文件位置: `/config/spotdl/config.json`

主要配置项：
- 输出格式: `m4a`（高质量，Jellyfin 兼容）
- 输出模板: `/data/Music/{artist}/{album}/{track-number} - {title}.{output-ext}`
- 歌词生成: 启用 LRC 歌词文件

详细说明: [SpotDL 使用指南](mcp/config/spotdl-guide.md)

### yt-dlp 配置

支持通过配置文件或命令行参数设置。

详细说明: [yt-dlp 使用指南](mcp/config/yt-dlp-guide.md)

## 开发

### 修改 MCP 服务器

编辑 `mcp/src/server.py`，然后重新构建镜像。

### 添加新工具

1. 在 `server.py` 中添加新的工具处理函数
2. 在 `list_tools()` 中注册新工具
3. 在 `call_tool()` 中添加路由
4. 更新 `skills/` 目录下的描述文件

### 添加新命令到白名单

修改 `docker-compose.yaml` 中的 `SHELL_WHITELIST` 环境变量。

## 许可证

[根据项目实际情况添加]

## 相关链接

- [MCP 协议文档](https://modelcontextprotocol.io/)
- [SpotDL 官方文档](https://spotdl.readthedocs.io/)
- [yt-dlp 官方文档](https://github.com/yt-dlp/yt-dlp)
