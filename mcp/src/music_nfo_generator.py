"""音乐 NFO 文件生成模块

提供从音乐文件提取元数据、查询 MusicBrainz API 和生成 Jellyfin 兼容的 NFO 文件的功能。
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from xml.dom import minidom

try:
    from mutagen import File as MutagenFile
    from mutagen.id3 import ID3NoHeaderError
    import musicbrainzngs
    MUSICBRAINZ_AVAILABLE = True
except ImportError:
    MUSICBRAINZ_AVAILABLE = False


def is_available() -> bool:
    """检查必要的库是否可用"""
    return MUSICBRAINZ_AVAILABLE


def extract_audio_metadata(file_path: Path) -> dict[str, Any]:
    """从音频文件中提取元数据
    
    Args:
        file_path: 音频文件路径
        
    Returns:
        包含元数据的字典，如果出错则包含 'error' 键
    """
    if not MUSICBRAINZ_AVAILABLE:
        raise ImportError("mutagen library is not available")
    
    try:
        audio_file = MutagenFile(str(file_path))
        if audio_file is None:
            return {}
        
        metadata = {}
        
        # 通用标签映射（支持 ID3、Vorbis、MP4 等格式）
        tag_mapping = {
            "title": ["TIT2", "TITLE", "\xa9nam"],
            "artist": ["TPE1", "ARTIST", "\xa9ART"],
            "album": ["TALB", "ALBUM", "\xa9alb"],
            "albumartist": ["TPE2", "ALBUMARTIST", "ALBUM ARTIST", "aART"],
            "tracknumber": ["TRCK", "TRACKNUMBER", "TRACK", "trkn"],
            "date": ["TDRC", "DATE", "YEAR", "\xa9day"],
            "musicbrainz_trackid": ["TXXX:MusicBrainz Track Id", "MUSICBRAINZ_TRACKID"],
            "musicbrainz_artistid": ["TXXX:MusicBrainz Artist Id", "MUSICBRAINZ_ARTISTID"],
            "musicbrainz_albumid": ["TXXX:MusicBrainz Album Id", "MUSICBRAINZ_ALBUMID"],
            "musicbrainz_albumartistid": ["TXXX:MusicBrainz Album Artist Id", "MUSICBRAINZ_ALBUMARTISTID"],
        }
        
        for key, tag_names in tag_mapping.items():
            for tag_name in tag_names:
                if tag_name in audio_file:
                    value = audio_file[tag_name]
                    if isinstance(value, list) and len(value) > 0:
                        # 处理 MP4 的 trkn 标签（元组格式）
                        if key == "tracknumber" and isinstance(value[0], tuple):
                            metadata[key] = str(value[0][0])
                        else:
                            metadata[key] = str(value[0])
                        break
        
        return metadata
    except ID3NoHeaderError:
        # 文件没有 ID3 标签，尝试其他格式
        return {}
    except Exception as e:
        return {"error": str(e)}


def query_musicbrainz(title: str, artist: str, album: str) -> dict[str, Any] | None:
    """查询 MusicBrainz API 获取 MusicBrainz ID
    
    Args:
        title: 歌曲标题
        artist: 艺术家名称
        album: 专辑名称
        
    Returns:
        包含 MusicBrainz ID 的字典，如果查询失败则返回 None
    """
    if not MUSICBRAINZ_AVAILABLE:
        return None
    
    try:
        # 配置 MusicBrainz API
        musicbrainzngs.set_useragent("code-runner-mcp", "1.0", "dev@qiaobo.me")
        
        # 搜索 recording（歌曲）
        result = musicbrainzngs.search_recordings(
            recording=title,
            artist=artist,
            release=album,
            limit=1
        )
        
        if not result.get("recording-list"):
            return None
        
        recording = result["recording-list"][0]
        recording_id = recording.get("id")
        
        # 获取艺术家 ID
        artist_id = None
        if recording.get("artist-credit") and len(recording["artist-credit"]) > 0:
            artist_credit = recording["artist-credit"][0]
            if isinstance(artist_credit, dict) and "artist" in artist_credit:
                artist_id = artist_credit["artist"].get("id")
        
        # 获取专辑信息
        album_id = None
        album_artist_id = None
        if recording.get("release-list") and len(recording["release-list"]) > 0:
            release = recording["release-list"][0]
            album_id = release.get("id")
            
            # 获取专辑艺术家 ID
            if release.get("artist-credit") and len(release["artist-credit"]) > 0:
                album_artist_credit = release["artist-credit"][0]
                if isinstance(album_artist_credit, dict) and "artist" in album_artist_credit:
                    album_artist_id = album_artist_credit["artist"].get("id")
        
        return {
            "recording_id": recording_id,
            "artist_id": artist_id,
            "album_id": album_id,
            "album_artist_id": album_artist_id,
        }
    except Exception:
        # 查询失败，返回 None
        return None


def generate_nfo_file(metadata: dict[str, Any], output_path: Path) -> None:
    """生成 Jellyfin 兼容的 XML NFO 文件
    
    Args:
        metadata: 包含专辑元数据的字典
        output_path: NFO 文件输出路径
    """
    # 创建根元素
    album_elem = ET.Element("album")
    
    # 添加基本字段
    if metadata.get("title"):
        title_elem = ET.SubElement(album_elem, "title")
        title_elem.text = metadata["title"]
    
    if metadata.get("artist") or metadata.get("albumartist"):
        artist_elem = ET.SubElement(album_elem, "artist")
        artist_elem.text = metadata.get("albumartist") or metadata.get("artist", "")
    
    if metadata.get("musicbrainz_albumid"):
        mb_album_elem = ET.SubElement(album_elem, "musicbrainzalbumid")
        mb_album_elem.text = metadata["musicbrainz_albumid"]
    
    if metadata.get("musicbrainz_albumartistid"):
        mb_album_artist_elem = ET.SubElement(album_elem, "musicbrainzalbumartistid")
        mb_album_artist_elem.text = metadata["musicbrainz_albumartistid"]
    
    if metadata.get("date"):
        date_elem = ET.SubElement(album_elem, "releasedate")
        # 处理日期格式（支持 YYYY、YYYY-MM、YYYY-MM-DD）
        date_str = str(metadata["date"]).strip()
        # 提取年份（前4位数字）
        year_match = re.search(r"(\d{4})", date_str)
        if year_match:
            year = year_match.group(1)
            # 尝试提取月份和日期
            month_match = re.search(r"\d{4}-(\d{2})", date_str)
            day_match = re.search(r"\d{4}-\d{2}-(\d{2})", date_str)
            if day_match:
                date_elem.text = f"{year}-{month_match.group(1) if month_match else '01'}-{day_match.group(1)}"
            elif month_match:
                date_elem.text = f"{year}-{month_match.group(1)}"
            else:
                date_elem.text = year
    
    # 创建 XML 树
    tree = ET.ElementTree(album_elem)
    
    # 格式化 XML（Python 3.9+ 支持 ET.indent）
    try:
        ET.indent(tree, space="  ")
    except AttributeError:
        # Python 3.8 及以下版本不支持 ET.indent，手动格式化
        pass
    
    # 写入文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 手动格式化 XML 输出（确保兼容性）
    xml_str = ET.tostring(album_elem, encoding="utf-8")
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
    
    # 移除 minidom 添加的额外空行
    lines = [line for line in pretty_xml.split("\n") if line.strip()]
    formatted_xml = "\n".join(lines)
    
    # 确保 XML 声明在第一行
    if not formatted_xml.startswith("<?xml"):
        formatted_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + formatted_xml
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(formatted_xml)


def process_music_files(
    music_files: list[Path],
    album_dir: Path
) -> tuple[dict[str, Any], list[str], list[str]]:
    """处理音乐文件并生成专辑元数据
    
    Args:
        music_files: 音乐文件路径列表
        album_dir: 专辑目录路径
        
    Returns:
        元组包含：
        - 专辑元数据字典
        - 已处理文件列表
        - 错误列表
    """
    album_metadata = {}
    processed_files = []
    errors = []
    mb_ids_found = {}  # 用于收集所有找到的 MusicBrainz ID
    
    for music_file in music_files:
        try:
            # 提取文件元数据
            file_metadata = extract_audio_metadata(music_file)
            if "error" in file_metadata:
                errors.append(f"{music_file.name}: {file_metadata['error']}")
                continue
            
            # 查询 MusicBrainz
            title = file_metadata.get("title", "")
            artist = file_metadata.get("artist", "")
            album = file_metadata.get("album", "")
            
            mb_data = None
            if title and artist:
                mb_data = query_musicbrainz(title, artist, album)
            
            # 合并元数据（优先使用 MusicBrainz 数据，如果没有则使用文件元数据）
            if not album_metadata:
                # 初始化专辑元数据（使用第一个有效文件的元数据）
                album_metadata = {
                    "title": album or "Unknown Album",
                    "artist": file_metadata.get("albumartist") or artist or "Unknown Artist",
                    "date": file_metadata.get("date", ""),
                }
            else:
                # 如果当前文件的专辑信息更完整，更新元数据
                current_album = album or ""
                if current_album and current_album != "Unknown Album" and album_metadata.get("title") == "Unknown Album":
                    album_metadata["title"] = current_album
                current_artist = file_metadata.get("albumartist") or artist or ""
                if current_artist and current_artist != "Unknown Artist" and album_metadata.get("artist") == "Unknown Artist":
                    album_metadata["artist"] = current_artist
                if file_metadata.get("date") and not album_metadata.get("date"):
                    album_metadata["date"] = file_metadata.get("date", "")
            
            # 收集 MusicBrainz ID（优先使用查询到的，其次使用文件中的）
            if mb_data:
                if mb_data.get("album_id"):
                    mb_ids_found["album_id"] = mb_data["album_id"]
                if mb_data.get("album_artist_id"):
                    mb_ids_found["album_artist_id"] = mb_data["album_artist_id"]
            else:
                # 使用文件中的 MusicBrainz ID（如果存在）
                if file_metadata.get("musicbrainz_albumid") and "album_id" not in mb_ids_found:
                    mb_ids_found["album_id"] = file_metadata.get("musicbrainz_albumid", "")
                if file_metadata.get("musicbrainz_albumartistid") and "album_artist_id" not in mb_ids_found:
                    mb_ids_found["album_artist_id"] = file_metadata.get("musicbrainz_albumartistid", "")
            
            processed_files.append(str(music_file))
        except Exception as e:
            errors.append(f"{music_file.name}: {str(e)}")
    
    # 将收集到的 MusicBrainz ID 添加到专辑元数据
    if mb_ids_found.get("album_id"):
        album_metadata["musicbrainz_albumid"] = mb_ids_found["album_id"]
    if mb_ids_found.get("album_artist_id"):
        album_metadata["musicbrainz_albumartistid"] = mb_ids_found["album_artist_id"]
    
    return album_metadata, processed_files, errors

