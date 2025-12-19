# yt-dlp 使用指南

## 版本信息

- **当前版本**: yt-dlp (通过 pip 安装，随 spotdl 一起安装)
- **官方文档**: [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- **官方网站**: [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- **依赖关系**: 作为 spotdl 的依赖自动安装

## 概述

yt-dlp 是一个强大的视频下载工具，是 youtube-dl 的改进版本。它支持从 YouTube 和其他1000多个视频平台下载视频和音频，具有更好的性能和更多的功能。

## 基本用法

### 基本语法
```bash
yt-dlp [选项] URL
```

### 常用参数

#### 通用（General Options）
- `-h, --help`：显示帮助并退出。
- `--version`：显示版本并退出。
- `-U, --update`：将 yt-dlp 更新到最新版本。
- `--abort-on-error`：遇到错误立即中止。
- `-i, --ignore-errors`：忽略错误，继续处理后续条目。
- `--dump-user-agent`：打印当前 User-Agent。
- `--list-extractors`：列出已支持的站点提取器。
- `--extractor-descriptions`：显示提取器简述。
- `--force-generic-extractor`：强制使用通用提取器。
- `--default-search PREFIX`：设置默认搜索前缀（如 `ytsearch:`）。
- `--ignore-config`：忽略配置文件。
- `--config-location PATH`：指定配置文件路径。
- `--flat-playlist`：仅列出播放列表条目信息，不解析/下载每个视频详情。
- `--mark-watched`：将视频标记为“已观看”（YouTube）。
- `--no-mark-watched`：不标记为“已观看”。

> 参考来源：yt-dlp README → General Options（见下方链接）

## USAGE AND OPTIONS（完整）

### 基本语法
```bash
yt-dlp [OPTIONS] URL [URL...]
```

下面选项按官方分类汇总，便于查阅。除特别标注外，所有选项均可写入配置文件（每行一个参数，支持内联注释与引号）。

### 1) 通用（General）
- `-h, --help`：显示帮助并退出
- `--version`：显示版本号并退出
- `-U, --update`：自更新到最新版本
- `--update-to nightly|stable`：指定更新通道
- `--abort-on-error`：任一条目出错即中止
- `-i, --ignore-errors`：忽略出错条目，继续执行
- `--no-warnings`：隐藏警告
- `--dump-user-agent`：打印 User-Agent
- `--list-extractors`：列出所有提取器
- `--extractor-descriptions`：打印提取器描述
- `--force-generic-extractor`：强制使用通用提取器
- `--default-search PREFIX`：默认搜索前缀（如 `ytsearch:`）
- `--ignore-config`：不加载任何配置文件
- `--config-location PATH`：仅加载指定路径的配置文件
- `--flat-playlist`：不逐条解析视频详情，仅列出条目
- `--mark-watched/--no-mark-watched`：YouTube 已观看标记开关
- `--compat-options OPTS`：启用兼容性选项（如 `mtime-by-default` 等，详见 README）

### 2) 网络（Network）
- `--proxy URL`：设置代理，如 `http://127.0.0.1:7890`
- `--socket-timeout SECONDS`：网络超时时间
- `--source-address IP`：绑定本地 IP
- `--force-ipv4/--force-ipv6`：强制 IPv4/IPv6
- `--geo-bypass`：自动尝试绕过地区限制
- `--geo-bypass-country CODE`：伪装为指定国家
- `--geo-bypass-ip-block CIDR`：伪装为 IP 网段
- `--xattr-set-filesize`：将文件大小写入 xattr（某些平台不推荐）

### 3) 选择（Video Selection & Filtering）
- `--playlist-start NUMBER`：播放列表起始序号（从 1 开始）
- `--playlist-end NUMBER`：播放列表结束序号
- `--playlist-items ITEMS`：指定项，如 `1,2,5-10`
- `--min-filesize SIZE`/`--max-filesize SIZE`：按体积过滤（如 `50M`）
- `--date DATE`/`--datebefore DATE`/`--dateafter DATE`：按日期过滤（YYYYMMDD）
- `--min-views N`/`--max-views N`：按播放量过滤
- `--match-filters EXPR`：表达式过滤（强大，详见 README）
- `--break-match-filters`：当匹配过滤条件时中止
- `--max-downloads N`：最多下载 N 个条目

### 4) 下载（Download）
- `-r, --limit-rate RATE`：限速（如 `4.2M`）
- `--retries N`：失败重试次数
- `--fragment-retries N`：分片下载重试次数
- `--buffer-size SIZE`：缓冲区
- `--no-resize-buffer`：禁用自动调整缓冲
- `--http-chunk-size SIZE`：HTTP 分块大小
- `--playlist-reverse/--playlist-random`：反转/随机顺序
- `--downloader [PROTO:]NAME`：选择外部下载器（如 `ffmpeg`）
- `--downloader-args NAME:ARGS`：外部下载器参数

### 5) 文件系统（Filesystem & Output Templates）
- `-a, --batch-file FILE`：从文件批量读取 URL
- `-o, --output TEMPLATE`：文件命名模板（如 `%(title)s.%(ext)s`）
- `--output-na-placeholder TEXT`：缺失字段占位符
- `--restrict-filenames`：限制为安全 ASCII 文件名
- `--windows-filenames`：Windows 兼容文件名
- `--no-overwrites`/`--force-overwrites`：不覆盖/强制覆盖
- `--continue/--no-continue`：断点续传开关
- `--no-part`：不生成 `.part` 临时文件
- `--no-mtime`：不设置文件修改时间
- `--write-description`：写出描述文件
- `--write-info-json`：写出 `info.json`
- `--load-info-json FILE`：从 JSON 加载信息
- `--cookies FILE`/`--no-cookies`：使用/禁用 cookies
- `--cache-dir DIR`/`--no-cache-dir`/`--rm-cache-dir`：缓存目录控制

### 6) 格式（Format Selection）
- `-f, --format FORMAT`：选择格式表达式（如 `bestvideo+bestaudio/best`）
- `-S, --format-sort SORT`：格式排序键（如 `res,codec:vp9`）
- `-F, --list-formats`：列出可用格式
- `--merge-output-format EXT`：合并后输出格式（如 `mp4`）

### 7) 字幕与缩略图（Subtitles & Thumbnails）
- `--write-subs/--write-auto-subs`：下载字幕/自动字幕
- `--sub-langs LANGS`：字幕语言（如 `en,zh-*`）
- `--sub-format FORMAT`：字幕格式（如 `srt/ass`）
- `--list-subs`：列出可用字幕
- `--write-thumbnail/--no-write-thumbnail`：下载缩略图
- `--convert-thumbnails FORMAT`：转换缩略图格式（如 `jpg`）

### 8) 认证（Authentication）
- `-u, --username USER`/`-p, --password PASS`：站点登录
- `-2, --twofactor CODE`：二步验证码
- `--netrc`：使用 `~/.netrc`
- `--video-password PASS`：视频密码
- `--oauth2 Bearer|...`：以 OAuth2 方式授权（特定站点）

### 9) 兼容/绕过（Workarounds & Geo）
- `--referer URL`/`--add-headers FIELD:VALUE`：自定义请求头
- `--user-agent UA`：自定义 UA
- `--extractor-args KEY:ARG`：为提取器传参（如 `youtube:player_client=android`）
- `--geo-verification-proxy URL`：地区验证代理

### 10) 下载器（External Downloaders）
- `--downloader NAME`：`aria2c`、`ffmpeg`、`curl` 等
- `--downloader-args NAME:ARGS`：为特定下载器传参

### 11) 后处理（Post-processing）
- `-x, --extract-audio`：提取音频
- `--audio-format FORMAT`：音频格式（`mp3/m4a/opus/flac/wav`）
- `--audio-quality Q`：音频质量（如 `0..10` 或 kbps）
- `--recode-video FORMAT`：重封装/转码为指定容器
- `--postprocessor-args NAME:ARGS`：为后处理器传参（如 `ffmpeg:`）
- `--embed-subs/--embed-thumbnail/--embed-metadata`：嵌入字幕/缩略图/元数据
- `--remove-chapters`：移除指定章节
- `--split-chapters`：按章节切分

### 12) 日志与调试（Logging & Verbosity）
- `-q, --quiet`：安静模式
- `-s, --simulate`：仅模拟，不下载
- `--print CMD`：打印字段/表格（如 `title,formats_table`）
- `-v, --verbose`：详细日志
- `--dump-pages`/`--print-traffic`：调试输出

### 配置文件（Configuration Files）
- 支持在配置文件中书写任意命令行参数，每行一个；可使用引号、转义与 `#` 注释。
- 加载顺序（概念）：便携配置 → 系统配置 → 用户配置 → `--config-location` 指定 → 命令行（最高优先级）。
- 常用控制：
  - `--ignore-config`：完全忽略加载
  - `--config-location PATH`：仅加载指定文件
- 示例（用户配置文件片段）：
```
# 统一输出目录与命名
-o "~/Videos/%(uploader)s/%(title)s.%(ext)s"
# 首选 vp9 + bestaudio
-f "bv*+ba/best"
# 启用字幕
--write-subs
--sub-langs "en,zh-*"
```

> 参考文档：yt-dlp README（USAGE AND OPTIONS、General Options、各分类小节）

## 配置文件位置与优先级（yt-dlp）

用于将常用选项固化，避免重复输入。配置文件内容与命令行参数一致：一行一个参数，支持引号与 `#` 注释。

### 路径（Linux / macOS）
- 便携式（与可执行文件同目录）：`./yt-dlp.conf` 或 `./yt-dlp.ini`
- 系统级：`/etc/yt-dlp.conf`
- 用户级：`~/.config/yt-dlp/config` 或 `~/.config/yt-dlp/config.txt`

### 路径（Windows）
- 便携式（与可执行文件同目录）：`yt-dlp.conf` 或 `yt-dlp.ini`
- 用户级：`%APPDATA%\yt-dlp\config.txt`

> 注：不同发行方式（pip/可执行文件）在“便携式”路径上可能略有差异；以实际安装目录为准。

### 加载顺序与优先级（从低到高）
1. 便携式配置（若存在）
2. 系统级配置
3. 用户级配置
4. `--config-location PATH` 指定的配置文件（仅加载该文件）
5. 命令行参数（最高优先级，覆盖前述所有）

### 常用控制
- 忽略全部配置：`--ignore-config`
- 仅加载指定配置：`--config-location /path/to/config`

### 配置文件示例
```
# 输出命名与目录
-o "~/Videos/%(uploader)s/%(title)s.%(ext)s"

# 首选格式：bestvideo+bestaudio，回退到 best
-f "bv*+ba/best"

# 代理与超时
--proxy "http://127.0.0.1:7890"
--socket-timeout 30

# 字幕
--write-subs
--sub-langs "en,zh-*"
```

> 参考：yt-dlp README（配置文件与路径说明、USAGE AND OPTIONS）

## 常见下载示例

```bash
# 1) 下载最佳视频+音频并自动合并（容器自动选择）
yt-dlp -f "bv*+ba/best" URL

# 2) 仅下载音频并转为 m4a（保留较高质量）
yt-dlp -x --audio-format m4a --audio-quality 0 URL

# 3) 下载整个播放列表（按顺序）
yt-dlp -f "bv*+ba/best" --yes-playlist URL_OF_PLAYLIST

# 4) 指定输出命名模板（按作者/标题存放）
yt-dlp -o "~/Videos/%(uploader)s/%(title)s.%(ext)s" URL

# 5) 下载字幕（中英文），并嵌入到媒体文件
yt-dlp --write-subs --sub-langs "en,zh-*" --embed-subs URL

# 6) 使用代理与限速（适合长任务）
yt-dlp --proxy "http://127.0.0.1:7890" -r 4M URL

# 7) 指定外部下载器参数（ffmpeg 作为 HLS 下载器）
yt-dlp --downloader "m3u8:ffmpeg" --downloader-args "ffmpeg:-loglevel warning" URL

# 8) 仅下载缩略图与信息文件
yt-dlp --write-thumbnail --write-info-json --skip-download URL

# 9) 读取批量 URL 列表
yt-dlp -a /path/to/urls.txt

# 10) 使用配置文件（已在默认路径配置好常用选项）
yt-dlp --config URL
```


