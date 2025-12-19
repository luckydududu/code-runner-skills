"""MCP server implemented in Python, providing shell and Python execution tools."""

from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Iterable, Sequence

import anyio
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

MODE = (os.getenv("MCP_MODE") or "http").lower()
PORT = int(os.getenv("MCP_PORT") or 8080)

# 目录结构定义（硬编码）
DEPLOY_ROOT = Path("/data")  # 最终部署产物目录
CONFIG_ROOT = Path("/config")  # 配置文件目录
TEMP_ROOT = Path("/temp")  # 临时文件目录（会被定期清理）

# SHELL_WHITELIST 先从环境变量读取，如果没有则使用默认值
DEFAULT_SHELL_WHITELIST = "ls,cat,echo,pwd,whoami,ffmpeg,magick,spotdl,yt-dlp,cp,mv,mkdir,touch,grep,sed,awk,sort,uniq,head,tail,wc,cut,tr,tar,gzip,gunzip,zip,unzip,curl,wget,ping,nslookup,df,du,free,ps,top,uptime,date,uname,find,which,type,file,stat,basename,dirname"
SHELL_WHITELIST = [cmd.strip() for cmd in (os.getenv("SHELL_WHITELIST") or DEFAULT_SHELL_WHITELIST).split(",") if cmd.strip()]
SUPPORTED_LANGS = ["python3"]

DEFAULT_ROUTE = {
    "Book": [".pdf", ".epub", ".mobi", ".txt"],
    "Image": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff"],
    "Movie": [".mp4", ".mov", ".mkv", ".webm", ".avi"],
    "Music": [".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"],
    "Shows": [".mp4", ".mkv", ".webm"],
}

try:
    ROUTE: dict[str, list[str]] = DEFAULT_ROUTE.copy()
    if os.getenv("BUCKET_MAP"):
        custom = json.loads(os.environ["BUCKET_MAP"])
        if isinstance(custom, dict):
            ROUTE = {
                str(bucket): [str(ext).lower() for ext in value] if isinstance(value, Iterable) else []
                for bucket, value in custom.items()
            }
except Exception:
    ROUTE = DEFAULT_ROUTE.copy()

# 使用自定义的临时目录
TMP_ROOT = TEMP_ROOT


def safe_join(base: Path, target: str | None) -> Path:
    relative = Path(target or "")
    candidate = (base / relative).resolve()
    base_resolved = base.resolve()
    if candidate != base_resolved and not str(candidate).startswith(str(base_resolved) + os.sep):
        raise ValueError("Path traversal detected")
    return candidate


def make_job_dir() -> Path:
    """创建临时工作目录，位于 /temp 目录下"""
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="mcp-job-", dir=TEMP_ROOT))


async def run_process(cmd: str, args: Sequence[str], *, cwd: Path) -> dict[str, Any]:
    proc = await asyncio.create_subprocess_exec(
        cmd,
        *args,
        cwd=str(cwd),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return {
        "code": proc.returncode,
        "stdout": stdout.decode(),
        "stderr": stderr.decode(),
    }


def ensure_deploy_dirs() -> None:
    """确保部署目录结构存在"""
    DEPLOY_ROOT.mkdir(parents=True, exist_ok=True)
    for bucket in list(ROUTE) + ["others"]:
        (DEPLOY_ROOT / bucket).mkdir(parents=True, exist_ok=True)


def ensure_config_dirs() -> None:
    """确保配置目录结构存在"""
    CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)


def pick_bucket(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    for bucket, extensions in ROUTE.items():
        if ext in extensions:
            return bucket
    return "others"


def to_content(payload: dict[str, Any]) -> list[types.ContentBlock]:
    return [types.TextContent(type="text", text=json.dumps(payload, indent=2))]


def validate_args(args: Any) -> list[str]:
    if args is None:
        return []
    if not isinstance(args, list) or not all(isinstance(item, str) for item in args):
        raise ValueError("args must be a list of strings")
    pattern = re.compile(r"[|;&><`$]")
    for item in args:
        if pattern.search(item):
            raise ValueError("Disallowed special characters in args")
    return args


async def handle_capabilities() -> list[types.ContentBlock]:
    """返回系统能力信息，包括目录结构说明"""
    payload = {
        "shell_whitelist": SHELL_WHITELIST,
        "supported_languages": SUPPORTED_LANGS,
        "deploy_root": str(DEPLOY_ROOT),
        "config_root": str(CONFIG_ROOT),
        "temp_root": str(TEMP_ROOT),
        "buckets": list(ROUTE) + ["others"],
        "route": ROUTE,
        "directory_structure": {
            "/data": "最终部署产物目录 - 存储处理完成的文件，按类型分类",
            "/config": "配置文件目录 - 存储各种配置文件和说明文档",
            "/temp": "临时文件目录 - 存储临时文件，会被定期清理"
        }
    }
    return to_content(payload)


async def handle_run_shell(arguments: dict[str, Any]) -> list[types.ContentBlock]:
    cmd = arguments.get("cmd")
    if not isinstance(cmd, str):
        raise ValueError("cmd must be provided as a string")
    if cmd not in SHELL_WHITELIST:
        return to_content({"error": f"Command '{cmd}' not allowed", "allowed": SHELL_WHITELIST})

    args = validate_args(arguments.get("args"))
    job = make_job_dir()
    cwd_value = arguments.get("cwd")
    workdir = safe_join(job, cwd_value if isinstance(cwd_value, str) else None)
    workdir.mkdir(parents=True, exist_ok=True)
    result = await run_process(cmd, args, cwd=workdir)
    result["workdir"] = str(workdir)
    return to_content(result)


async def handle_run_python(arguments: dict[str, Any]) -> list[types.ContentBlock]:
    code = arguments.get("code")
    if not isinstance(code, str):
        raise ValueError("code must be provided as a string")

    job = make_job_dir()
    cwd_value = arguments.get("cwd")
    workdir = safe_join(job, cwd_value if isinstance(cwd_value, str) else None)
    workdir.mkdir(parents=True, exist_ok=True)
    result = await run_process("python3", ["-c", code], cwd=workdir)
    result["workdir"] = str(workdir)
    return to_content(result)


async def handle_deploy(arguments: dict[str, Any]) -> list[types.ContentBlock]:
    """部署文件到最终产物目录 /data"""
    workdir = arguments.get("workdir")
    if not isinstance(workdir, str):
        raise ValueError("workdir must be provided as a string")
    source = Path(workdir).resolve()
    if str(source) == str(TMP_ROOT):
        raise ValueError("workdir must be a job directory")
    if not str(source).startswith(str(TMP_ROOT)):
        raise ValueError("workdir must be created by this server")
    if not source.is_dir():
        raise ValueError("workdir does not exist")

    requested_files = arguments.get("files")
    files_to_copy: list[Path]
    if requested_files is None:
        files_to_copy = [p for p in source.iterdir() if p.is_file()]
    else:
        if not isinstance(requested_files, list) or not all(isinstance(item, str) for item in requested_files):
            raise ValueError("files must be a list of strings")
        files_to_copy = []
        for rel_path in requested_files:
            files_to_copy.append(safe_join(source, rel_path))

    ensure_deploy_dirs()

    deployed = []
    for src in files_to_copy:
        if not src.is_file():
            continue
        dest_dir = DEPLOY_ROOT / pick_bucket(src.name)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        shutil.copy2(src, dest)
        deployed.append({"src": str(src), "dest": str(dest), "bucket": dest_dir.name})

    return to_content({"deploy_root": str(DEPLOY_ROOT), "deployed": deployed})


async def handle_read_config(arguments: dict[str, Any]) -> list[types.ContentBlock]:
    """读取配置文件内容"""
    config_file = arguments.get("file")
    if not isinstance(config_file, str):
        raise ValueError("file must be provided as a string")
    
    # 确保配置文件路径在 /config 目录内
    config_path = safe_join(CONFIG_ROOT, config_file)
    
    if not config_path.exists():
        return to_content({"error": f"Config file not found: {config_file}"})
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return to_content({
            "file": str(config_path),
            "content": content,
            "size": config_path.stat().st_size
        })
    except Exception as e:
        return to_content({"error": f"Failed to read config file: {str(e)}"})


async def handle_list_files(arguments: dict[str, Any]) -> list[types.ContentBlock]:
    """列出指定目录下的文件"""
    target_dir = arguments.get("directory")
    if not isinstance(target_dir, str):
        raise ValueError("directory must be provided as a string")
    
    # 允许列出 /data, /config, /temp 目录
    allowed_roots = [DEPLOY_ROOT, CONFIG_ROOT, TEMP_ROOT]
    target_path = Path(target_dir).resolve()
    
    # 检查是否在允许的根目录下
    is_allowed = False
    for root in allowed_roots:
        root_resolved = root.resolve()
        if str(target_path) == str(root_resolved) or str(target_path).startswith(str(root_resolved) + os.sep):
            is_allowed = True
            break
    
    if not is_allowed:
        return to_content({"error": f"Directory must be under /data, /config, or /temp"})
    
    if not target_path.exists():
        return to_content({"error": f"Directory not found: {target_dir}"})
    
    if not target_path.is_dir():
        return to_content({"error": f"Path is not a directory: {target_dir}"})
    
    try:
        files = []
        dirs = []
        for item in sorted(target_path.iterdir()):
            item_info = {
                "name": item.name,
                "path": str(item),
                "size": item.stat().st_size if item.is_file() else None,
                "type": "file" if item.is_file() else "directory"
            }
            if item.is_file():
                files.append(item_info)
            else:
                dirs.append(item_info)
        
        return to_content({
            "directory": str(target_path),
            "files": files,
            "directories": dirs,
            "total_files": len(files),
            "total_directories": len(dirs)
        })
    except Exception as e:
        return to_content({"error": f"Failed to list directory: {str(e)}"})


async def handle_check_file(arguments: dict[str, Any]) -> list[types.ContentBlock]:
    """检查文件是否存在并返回文件信息"""
    file_path = arguments.get("file")
    if not isinstance(file_path, str):
        raise ValueError("file must be provided as a string")
    
    # 允许检查 /data, /config, /temp 目录下的文件
    allowed_roots = [DEPLOY_ROOT, CONFIG_ROOT, TEMP_ROOT]
    target_path = Path(file_path).resolve()
    
    # 检查是否在允许的根目录下
    is_allowed = False
    for root in allowed_roots:
        root_resolved = root.resolve()
        if str(target_path).startswith(str(root_resolved) + os.sep) or str(target_path) == str(root_resolved):
            is_allowed = True
            break
    
    if not is_allowed:
        return to_content({"error": f"File must be under /data, /config, or /temp"})
    
    if not target_path.exists():
        return to_content({
            "exists": False,
            "file": str(target_path)
        })
    
    try:
        stat = target_path.stat()
        return to_content({
            "exists": True,
            "file": str(target_path),
            "size": stat.st_size,
            "type": "file" if target_path.is_file() else "directory",
            "modified": stat.st_mtime,
            "bucket": pick_bucket(target_path.name) if target_path.is_file() else None
        })
    except Exception as e:
        return to_content({"error": f"Failed to check file: {str(e)}"})


app = Server("mcp-code-runner", version="0.5.0")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="capabilities",
            description="List allowed shell commands, supported languages, deploy root, and buckets.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="run_shell",
            description="Run a whitelisted shell command with args (no pipes/redirection).",
            inputSchema={
                "type": "object",
                "properties": {
                    "cmd": {"type": "string", "description": f"Allowed: {', '.join(SHELL_WHITELIST)}"},
                    "args": {"type": "array", "items": {"type": "string"}, "default": []},
                    "cwd": {"type": "string", "description": "Optional working dir relative to a temp job dir"},
                },
                "required": ["cmd"],
            },
        ),
        types.Tool(
            name="run_python",
            description="Execute Python3 code. Print/write files into a temp job dir.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "cwd": {"type": "string"},
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="deploy_artifacts",
            description="Deploy files from a job directory into the fixed deploy root.",
            inputSchema={
                "type": "object",
                "properties": {
                    "workdir": {"type": "string", "description": "Absolute job path returned by run_* tools."},
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Relative paths under workdir. If omitted, deploy all top-level files.",
                    },
                },
                "required": ["workdir"],
            },
        ),
        types.Tool(
            name="read_config",
            description="Read configuration files from /config directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Relative path to config file under /config directory."},
                },
                "required": ["file"],
            },
        ),
        types.Tool(
            name="list_files",
            description="List files and directories in /data, /config, or /temp directories.",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Absolute path to directory (must be under /data, /config, or /temp)."},
                },
                "required": ["directory"],
            },
        ),
        types.Tool(
            name="check_file",
            description="Check if a file exists and return file information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "Absolute path to file (must be under /data, /config, or /temp)."},
                },
                "required": ["file"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.ContentBlock]:
    arguments = arguments or {}
    try:
        if name == "capabilities":
            return await handle_capabilities()
        if name == "run_shell":
            return await handle_run_shell(arguments)
        if name == "run_python":
            return await handle_run_python(arguments)
        if name == "deploy_artifacts":
            return await handle_deploy(arguments)
        if name == "read_config":
            return await handle_read_config(arguments)
        if name == "list_files":
            return await handle_list_files(arguments)
        if name == "check_file":
            return await handle_check_file(arguments)
        raise ValueError(f"Unknown tool: {name}")
    except Exception as exc:  # surfacing any error as JSON content
        return to_content({"error": str(exc)})


async def run_stdio() -> None:
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())


async def run_http() -> None:
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import JSONResponse, PlainTextResponse
    from starlette.routing import Mount, Route
    import uvicorn

    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request):
        async with sse.connect_sse(request.scope, request.receive, request._send) as streams:  # type: ignore[attr-defined]
            await app.run(streams[0], streams[1], app.create_initialization_options())
        return PlainTextResponse("")

    async def health(_: Request):
        return JSONResponse({"status": "ok"})

    starlette_app = Starlette(
        debug=False,
        routes=[
            Route("/", endpoint=health, methods=["GET"]),
            Route("/sse", endpoint=handle_sse, methods=["GET"]),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    config = uvicorn.Config(starlette_app, host="0.0.0.0", port=PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


def main() -> int:
    if MODE == "stdio":
        anyio.run(run_stdio)
    else:
        anyio.run(run_http)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
