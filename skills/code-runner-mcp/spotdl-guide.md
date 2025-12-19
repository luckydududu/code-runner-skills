# SpotDL 使用指南

## 版本信息

- **当前版本**: SpotDL 4.4.3
- **官方文档**: [SpotDL GitHub](https://github.com/spotDL/spotify-downloader)
- **官方文档网站**: [SpotDL Documentation](https://spotdl.readthedocs.io/)

## 概述

SpotDL 是一个强大的音乐下载工具，支持从 Spotify、YouTube 等多个平台下载音乐。它能够自动搜索并下载高质量的音频文件。

## 基本用法

```bash
spotdl [选项] <Spotify链接或搜索词>
```

### 命令行参数总览（官方文档汇总）

以下参数来自官方文档的“Command line options”，已按类别整理，便于查阅与复制使用。

- 参考来源：spotDL Usage → Command line options（见文末引用链接）

#### 认证（Spotify）相关
- `--client-id CLIENT_ID`：用于登录 Spotify 的客户端 ID。
- `--client-secret CLIENT_SECRET`：用于登录 Spotify 的客户端密钥。
- `--auth-token AUTH_TOKEN`：直接使用授权 Token 登录 Spotify。
- `--cache-path CACHE_PATH`：spotipy 缓存文件存放路径。
- `--no-cache`：禁用缓存（请求与 Token 均不缓存）。
- `--max-retries MAX_RETRIES`：获取元数据时的最大重试次数。
- `--headless`：在无头模式下运行。
- `--use-cache-file`：使用本地缓存文件获取元数据（位于 `~/.spotdl/.spotify_cache` 或 Windows 对应目录）。仅缓存 Tracks，可能过期，谨慎使用。

#### FFmpeg 相关
- `--ffmpeg FFMPEG`：指定要使用的 ffmpeg 可执行文件路径。
- `--threads THREADS`：下载/处理时使用的线程数。
- `--bitrate {auto,disable,8k,16k,24k,32k,40k,48k,64k,80k,96k,112k,128k,160k,192k,224k,256k,320k,0-9}`：输出文件比特率。
  - `auto`：使用原始文件比特率；`disable`：禁用比特率参数。
  - 对于 m4a/opus：`auto`/`disable` 会跳过转码（保留源文件）。
- `--ffmpeg-args FFMPEG_ARGS`：以字符串形式传递额外的 ffmpeg 参数。

#### 输出与下载相关
- `--format {mp3,flac,ogg,opus,m4a,wav}`：选择输出格式。
- `--save-file SAVE_FILE`：将歌曲数据保存到/从文件加载（扩展名必须为 `.spotdl`）。与 `download` 一起使用时会写入该文件。`save` 可用 `-` 输出到 stdout。
- `--preload`：预加载下载 URL，以加速后续下载。
- `--output OUTPUT`：自定义输出文件命名模板，支持变量：
  `{title},{artists},{artist},{album},{album-artist},{genre},{disc-number},{disc-count},{duration},{year},{original-date},{track-number},{tracks-count},{isrc},{track-id},{publisher},{list-length},{list-position},{list-name},{output-ext}`。
- `--m3u [M3U]`：保存为 m3u 播放列表文件名。
  - 默认：`{list[0]}.m3u8`；使用 `{list}` 为每个列表生成；`{list[0]}` 取查询中的第 1 个列表。
- `--cookie-file COOKIE_FILE`：提供 cookies 文件路径（例如用于 YT Music Premium 提升音质）。
- `--overwrite {skip,metadata,force}`：处理已存在/重复文件的策略。
  - 结合 `--scan-for-songs`：`force` 移除重复；`metadata` 仅对最新文件更新元数据并移除其他重复。
- `--restrict [strict,ascii,none]`：限制文件名字符范围，提升跨平台兼容性。
- `--print-errors`：在结束时打印错误（错误匹配、下载失败等），适合长列表任务。
- `--save-errors SAVE_ERRORS`：将错误保存到指定文件。
- `--sponsor-block`：启用 SponsorBlock（用于 yt/ytm 下载裁剪广告段）。
- `--archive ARCHIVE`：指定已下载歌曲的归档文件名（避免重复下载）。
- `--playlist-numbering`：将播放列表中每首歌的专辑名设为该播放列表名，并使用播放列表图标作为封面。
- `--playlist-retain-track-cover`：同上，但保留每首曲目的原始封面。
- `--scan-for-songs`：扫描输出目录以识别已存在文件；建议与 `--overwrite` 联用控制行为。
- `--fetch-albums`：基于查询中的歌曲补拉对应专辑。
- `--id3-separator ID3_SEPARATOR`：更改 MP3 文件 ID3 标签使用的分隔符（仅 MP3 有效）。
- `--ytm-data`：当使用 ytm 链接下载时，优先使用 ytm 元数据而非 Spotify。
- `--add-unavailable`：当下载时将不可用歌曲也添加到 m3u/归档文件中。
- `--generate-lrc`：生成 LRC 歌词文件（需要在歌词提供者中包含 `synced`）。
- `--force-update-metadata`：强制更新已有文件的元数据。
- `--sync-without-deleting`：同步时不删除缺失于源列表的本地文件。
- `--max-filename-length MAX_FILENAME_LENGTH`：限制文件名最大长度（不超越操作系统限制）。
- `--yt-dlp-args YT_DLP_ARGS`：传递额外的 yt-dlp 参数。
- `--detect-formats [mp3,flac,ogg,opus,m4a,wav ...]`：检测与 `--format` 不同的已下载文件格式（与 `--m3u` 联用时，仅首个检测到的格式会写入 m3u）。
- `--redownload`：在 `meta` 操作中，使用 `--format` 指定的新格式重新下载本地歌曲。
- `--skip-album-art`：在 `meta` 操作中跳过下载专辑封面。
- `--ignore-albums [ALBUMS ...]`：忽略来自给定专辑的歌曲。
- `--skip-explicit`：跳过带有 Explicit 标签的歌曲。
- `--proxy PROXY`：为下载设置 HTTP(S) 代理，例如 `http://host:port`。
- `--create-skip-file`：为成功下载的文件创建 `.skip` 标记文件。
- `--respect-skip-file`：若存在对应 `.skip` 文件，则跳过该歌曲的下载。
- `--sync-remove-lrc`：当执行同步下载时，删除对应的 LRC 歌词文件。

#### Web（内置 Web UI）相关
- `--host HOST`：Web 服务器监听主机地址。
- `--port PORT`：Web 服务器监听端口。
- `--keep-alive`：即使没有客户端连接也保持 Web 服务器存活。
- `--allowed-origins [ALLOWED_ORIGINS ...]`：允许的跨域来源列表。
- `--web-use-output-dir`：Web UI 下载使用 `--output` 指定目录（多用户场景可能有冲突风险）。
- `--keep-sessions`：Web 服务器关闭后保留会话目录。
- `--force-update-gui`：强制刷新 Web GUI（从仓库重新拉取）。
- `--web-gui-repo WEB_GUI_REPO`：自定义 Web GUI 仓库地址（例如 `https://github.com/spotdl/web-ui/tree/master/dist`）。
- `--web-gui-location WEB_GUI_LOCATION`：指定本地 Web GUI 目录路径。
- `--enable-tls`：为 Web 服务器启用 TLS。
- `--cert-file CERT_FILE`：TLS 证书（PEM）。
- `--key-file KEY_FILE`：TLS 私钥（PEM）。
- `--ca-file CA_FILE`：TLS CA 根证书文件路径。

#### 日志与杂项
- `--log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,MATCH,DEBUG,NOTSET}`：设置日志级别。
- `--simple-tui`：使用简化的 TUI。
- `--log-format LOG_FORMAT`：自定义日志格式（参见 Python logging LogRecord 属性）。

#### 其他
- `--download-ffmpeg`：将 ffmpeg 下载到 spotdl 目录。
- `--generate-config`：生成配置文件（若已存在将覆盖）。
- `--check-for-updates`：检查是否有新版本。
- `--profile`：以性能分析模式运行（调试用途）。
- `--version`, `-v`：显示版本号并退出。

> 提示：YouTube Music Premium 用户可结合 `--cookie-file` 与指定 `--format m4a/opus` 且 `--bitrate disable` 获得更高码率的原始文件；详见官方文档说明。



## 配置文件项详解（官方文档汇总）

配置文件默认位置：`~/.spotdl/config.json`（Linux/macOS）或 `C:\Users\<user>\.spotdl\config.json`（Windows）。支持通过 `--config` 指定路径，或用 `spotdl --generate-config` 生成。可将 `load_config` 置为 `false` 以禁用自动加载。

- 参考来源：spotDL Usage → Config file、Config file location、Default config（见文末引用链接）

### 认证与会话
- `client_id`：Spotify 客户端 ID。
- `client_secret`：Spotify 客户端密钥。
- `auth_token`：直接使用的 Spotify 授权 Token。
- `user_auth`：是否启用用户授权流程（如下载“已点赞”与用户内容时需要）。
- `cache_path`：spotipy/spotify 缓存路径。
- `no_cache`：禁用缓存（请求与 Token）。
- `max_retries`：获取元数据的最大重试次数。
- `headless`：无头模式运行。
- `use_cache_file`：使用本地缓存文件获取元数据（仅缓存 Track，可能过期）。
- `load_config`：是否自动加载配置文件（设为 `false` 可阻止自动加载）。

### FFmpeg 与音频转码
- `ffmpeg`：ffmpeg 可执行文件路径。
- `threads`：并发线程数。
- `bitrate`：输出比特率，支持 `auto`、`disable`、如 `128k/320k` 或 VBR 值 `0-9`。
- `ffmpeg_args`：额外传给 ffmpeg 的参数字符串。

### 输出与下载
- `format`：输出格式，`mp3/flac/ogg/opus/m4a/wav`。
- `save_file`：保存/加载歌曲数据的 `.spotdl` 文件路径。
- `preload`：是否预加载下载 URL 加速后续下载。
- `output`：输出命名模板（支持 `{title}`、`{artist}`、`{album}`、`{track-number}` 等变量）。
- `m3u`：生成的 m3u 播放列表文件名模板（如 `{list[0]}.m3u8`）。
- `cookie_file`：cookies 文件路径（YT Music Premium 提升音质场景常用）。
- `overwrite`：处理已存在文件策略：`skip/metadata/force`。
- `restrict`：文件名字符限制：`strict/ascii/none`。
- `print_errors`：在任务结束时打印错误汇总。
- `save_errors`：将错误保存到文件。
- `sponsor_block`：启用 SponsorBlock 减少视频广告段。
- `archive`：已下载歌曲归档文件路径（避免重复下载）。
- `playlist_numbering`：将播放列表名写入专辑字段，并使用播放列表图标为封面。
- `playlist_retain_track_cover`：同上，但保留曲目原始封面。
- `scan_for_songs`：扫描输出目录识别已存在文件（建议配合 `overwrite`）。
- `fetch_albums`：根据查询歌曲补拉其专辑。
- `id3_separator`：MP3 ID3 标签分隔符。
- `ytm_data`：对 ytm 链接下载时使用 ytm 元数据。
- `add_unavailable`：将不可用歌曲也写入 m3u/归档。
- `generate_lrc`：生成 LRC 歌词（需启用 `synced` 歌词提供者）。
- `force_update_metadata`：强制更新已有文件的元数据。
- `sync_without_deleting`：同步时不删除本地多余文件。
- `max_filename_length`：文件名最大长度（不突破 OS 限制）。
- `yt_dlp_args`：传递给 yt-dlp 的附加参数。
- `detect_formats`：检测与 `format` 不同的已下载格式列表（与 `m3u` 联用时仅写入首个匹配）。
- `redownload`：在 `meta` 操作中按新 `format` 重新下载本地文件。
- `skip_album_art`：在 `meta` 操作中跳过专辑封面下载。
- `ignore_albums`：忽略指定专辑的曲目。
- `skip_explicit`：跳过 Explicit 曲目。
- `proxy`：下载代理地址，如 `http://host:port`。
- `create_skip_file`：为成功下载的文件创建 `.skip` 标记。
- `respect_skip_file`：若存在 `.skip` 文件则跳过下载。
- `sync_remove_lrc`：同步时移除对应 LRC 歌词文件。

### Web（内置 Web UI）
- `host`：Web 服务器主机地址。
- `port`：Web 服务器端口。
- `keep_alive`：无客户端连接时保持服务存活。
- `allowed_origins`：允许的跨域来源列表。
- `web_use_output_dir`：Web 下载直接使用 `output` 目录。
- `keep_sessions`：关闭后保留会话目录。
- `force_update_gui`：强制刷新 Web GUI 资源。
- `web_gui_repo`：自定义 Web GUI 仓库地址。
- `web_gui_location`：本地 Web GUI 目录路径。
- `enable_tls`：启用 TLS。
- `cert_file`：TLS 证书（PEM）。
- `key_file`：TLS 私钥（PEM）。
- `ca_file`：TLS CA 根证书路径。

### 日志与其他
- `log_level`：日志级别，`CRITICAL/FATAL/ERROR/WARN/WARNING/INFO/MATCH/DEBUG/NOTSET`。
- `simple_tui`：启用简洁 TUI。
- `log_format`：自定义日志格式（兼容 Python logging）。
- `download_ffmpeg`：将 ffmpeg 下载至 spotdl 目录。
- `check_for_updates`：检查更新。
- `profile`：性能分析模式。

> 注：配置文件项与 CLI 参数一一对应，优先级通常为命令行高于配置文件；如需临时覆盖配置，直接在命令行传参即可。


## Jellyfin 兼容性

目的：下载后的歌曲可被 Jellyfin 稳定识别与入库。

### 文件存放规则（推荐）
- **输出目录**：`/data/Music`
- **目录结构**：`{artist}/{album}/`
- **文件命名**：`{track-number:02d} - {title}.{output-ext}`
- **模板参数**：
  - 推荐 `--output-template "{artist}/{album}/{track-number:02d} - {title}"`
  - 在配置文件中设置 `output` 与 `format`，确保统一命名与格式

示例目录：
```
/data/Music/
└── 艺术家名/
    └── 专辑名/
        ├── 01 - 歌曲A.m4a
        └── 02 - 歌曲B.m4a
```

### 使用预置配置文件下载
- 已准备好默认路径下的配置文件（已指定 `format` 与 `output`），下载时直接引用：
```bash
spotdl --config "链接或搜索词"
```

### Jellyfin 导入要点（精简）
- 新建“音乐”类型媒体库，路径指向 `/data/Music`
- 开启实时监控与元数据提取
- 优先使用嵌入元数据；封面与歌词可在本工具侧嵌入

## 元数据和歌词嵌入

### 元数据保留

SpotDL 会自动保留和嵌入以下元数据信息：

- **基本信息**：艺术家、专辑、歌曲标题、曲目编号
- **时间信息**：发行年份、时长
- **分类信息**：流派、风格
- **专辑封面**：自动下载并嵌入专辑封面
- **歌词信息**：自动获取并嵌入歌词

### 歌词嵌入设置

```bash
# 手动指定歌词嵌入（Jellyfin 兼容存放 + 保留元数据）
spotdl \
  --format m4a \
  --bitrate disable \
  --lyrics-provider genius \
  --output-template "{artist}/{album}/{track-number:02d} - {title}" \
  --output /data/Music \
  --force-update-metadata \
  "歌曲名称或链接"

# 使用配置文件（推荐）
# 已在默认路径下配置好（不可修改路径），直接引用：
spotdl --config "歌曲名称或链接"
```

### 歌词格式支持

- **LRC 格式**：标准歌词格式，支持时间轴
- **嵌入到文件**：歌词直接嵌入到音频文件中
- **外部歌词文件**：同时生成独立的歌词文件

### 元数据验证

下载完成后，可以使用以下命令验证元数据：

```bash
# 查看文件元数据
ffprobe -v quiet -print_format json -show_format -show_streams "/data/Music/艺术家/专辑/01 - 歌曲名.m4a"

# 查看嵌入的歌词
ffmpeg -i "/data/Music/艺术家/专辑/01 - 歌曲名.m4a" -f null - 2>&1 | grep -i lyrics
```

### 文件存放校验

下载完成后，使用以下命令校验文件存放：

```bash
# 1. 检查目录结构
find /data/Music -type d

# 2. 检查文件命名格式
find /data/Music -name "*.m4a"

# 3. 统计下载文件数量
find /data/Music -name "*.m4a" | wc -l
```


