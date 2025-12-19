# Skills 描述文件

本目录包含 MCP Code Runner 的使用技能描述文件，用于指导 AI 如何使用 MCP 服务器来执行各种任务。

## 文件列表

### 1. [mcp-code-runner.md](./mcp-code-runner.md)
通用的 MCP Code Runner 使用指南，包含：
- MCP 服务器概述
- 所有可用工具（Tools）的详细说明
- 典型工作流程
- 安全说明

### 2. [spotdl-download.md](./spotdl-download.md)
SpotDL 音乐下载技能，包含：
- SpotDL 基本用法
- 下载单曲、播放列表、专辑
- 高级配置选项
- 完整工作流程示例
- 最佳实践

### 3. [ytdlp-download.md](./ytdlp-download.md)
yt-dlp 视频下载技能，包含：
- yt-dlp 基本用法
- 视频和音频下载
- 字幕下载
- 格式选择
- 完整工作流程示例
- 最佳实践

## 使用方式

这些 skill 文件旨在：
1. **供 AI 学习**: AI 可以通过阅读这些文件了解如何使用 MCP 服务器
2. **文档参考**: 作为开发和使用参考文档
3. **技能描述**: 描述每个工具的能力和使用场景

## 工作流程

典型的下载任务工作流程：

1. **执行下载命令**: 使用 `run_shell` 执行 `spotdl` 或 `yt-dlp`
2. **检查结果**: 使用 `list_files` 查看临时目录中的文件
3. **部署文件**: 使用 `deploy_artifacts` 将文件移动到 `/data` 目录
4. **验证部署**: 使用 `check_file` 或 `list_files` 验证文件位置

## 相关资源

- [MCP Code Runner 主 README](../README.md)
- [配置文件指南](../mcp/config/README.md)
- [SpotDL 详细指南](../mcp/config/spotdl-guide.md)
- [yt-dlp 详细指南](../mcp/config/yt-dlp-guide.md)

