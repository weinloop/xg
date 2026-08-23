#!/usr/bin/env python3
"""
将案例背诵方便打印版.md按章节拆分并生成每章MP3音频。
使用edge-tts（zh-CN-YunyangNeural，+10%语速）。
"""
import re
import os
import subprocess
import sys

SOURCE = os.path.join(os.path.dirname(__file__), "案例背诵方便打印版.md")
OUT_DIR = os.path.join(os.path.dirname(__file__), "案例语音")
EDGE_TTS = "/Users/aus/.workbuddy/binaries/python/envs/default/bin/edge-tts"
VOICE = "zh-CN-YunyangNeural"
RATE = "+10%"


def clean_markdown_for_tts(text):
    """将markdown文本清理为适合语音朗读的纯文本。"""
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        stripped = line.strip()

        # 空行保留（作为停顿）
        if not stripped:
            cleaned.append("")
            continue

        # 跳过水平分割线
        if stripped in ("---", "***", "==="):
            continue

        # 去掉标题井号
        if stripped.startswith("####"):
            stripped = stripped.lstrip("#").strip()
        elif stripped.startswith("###"):
            stripped = stripped.lstrip("#").strip()
        elif stripped.startswith("##"):
            stripped = stripped.lstrip("#").strip()
        elif stripped.startswith("#"):
            stripped = stripped.lstrip("#").strip()

        # 去掉引用标记
        if stripped.startswith(">"):
            stripped = stripped.lstrip(">").strip()

        # 去掉列表标记
        if stripped.startswith("- "):
            stripped = stripped[2:]
        elif stripped.startswith("-"):
            stripped = stripped[1:].strip()

        # 去掉粗体/斜体标记
        stripped = stripped.replace("**", "")
        stripped = stripped.replace("__", "")

        # 处理表格行
        if stripped.startswith("|"):
            # 提取单元格
            parts = stripped.split("|")
            cells = [c.strip() for c in parts if c.strip()]
            # 跳过分隔行（全由-和:组成）
            if cells and all(re.match(r"^[-:]+$", c) for c in cells):
                continue
            if cells:
                cleaned.append("，".join(cells) + "。")
                continue

        cleaned.append(stripped)

    # 合并多余空行
    result = "\n".join(cleaned)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def split_chapters(md_text):
    """按 ## 章节标题拆分，返回 [(chapter_num, chapter_title, content), ...]。"""
    # 用正则匹配 ## N. 标题行
    pattern = re.compile(r"^## (\d+)\.\s*(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(md_text))

    chapters = []
    for i, m in enumerate(matches):
        num = int(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        content = md_text[start:end].strip()
        chapters.append((num, title, content))

    return chapters


def split_long_text(text, max_chars=5000):
    """将超长文本按段落边界拆分为多段，每段不超过max_chars字符。"""
    paragraphs = text.split("\n\n")
    parts = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars and current:
            parts.append(current.strip())
            current = para
        else:
            current = current + "\n\n" + para if current else para
    if current.strip():
        parts.append(current.strip())
    return parts


def generate_mp3(txt_path, mp3_path, chapter_title, timeout=600):
    """用edge-tts生成MP3，失败时重试一次。"""
    cmd = [
        EDGE_TTS,
        "-f", txt_path,
        "--voice", VOICE,
        "--rate", RATE,
        "--write-media", mp3_path,
    ]
    for attempt in range(2):
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0 and os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 0:
            return True
        print(f"  尝试 {attempt + 1} 失败: {result.stderr[:200] if result.stderr else '未知错误'}")
    return False


def main():
    # 读取源文件
    with open(SOURCE, "r", encoding="utf-8") as f:
        md_text = f.read()

    chapters = split_chapters(md_text)
    print(f"共解析到 {len(chapters)} 个章节\n")

    os.makedirs(OUT_DIR, exist_ok=True)

    success = 0
    failed = []

    for num, title, content in chapters:
        # 清理文本
        cleaned = clean_markdown_for_tts(content)
        # 在内容前加上章节标题
        full_text = f"{title}。\n\n{cleaned}"

        prefix = f"{num:02d}"
        safe_title = title.replace("/", "_")

        # 如果文本过长，拆分为多段生成
        if len(full_text) > 6000:
            parts = split_long_text(full_text, max_chars=5000)
            part_suffixes = ["上", "中", "下", "续1", "续2", "续3"]
            print(f"[{prefix}] {title} ({len(full_text)} 字符, 拆分为 {len(parts)} 段)")
            all_ok = True
            for idx, part in enumerate(parts):
                suffix = part_suffixes[idx] if idx < len(part_suffixes) else f"续{idx}"
                txt_name = f"{prefix}{suffix}-{safe_title}.txt"
                mp3_name = f"{prefix}{suffix}-{safe_title}.mp3"
                txt_path = os.path.join(OUT_DIR, txt_name)
                mp3_path = os.path.join(OUT_DIR, mp3_name)

                # 跳过已完成的
                if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 0:
                    print(f"  [{suffix}] 已存在, 跳过")
                    success += 1
                    continue

                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(part)
                if generate_mp3(txt_path, mp3_path, title):
                    mp3_size = os.path.getsize(mp3_path)
                    print(f"  [{suffix}] MP3 生成成功 ({mp3_size} 字节)")
                    success += 1
                else:
                    print(f"  [{suffix}] MP3 生成失败!")
                    all_ok = False
                    failed.append(f"{prefix}{suffix}-{title}")
            if not all_ok:
                pass
        else:
            txt_name = f"{prefix}-{safe_title}.txt"
            mp3_name = f"{prefix}-{safe_title}.mp3"
            txt_path = os.path.join(OUT_DIR, txt_name)
            mp3_path = os.path.join(OUT_DIR, mp3_name)

            # 跳过已完成的
            if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 0:
                print(f"[{prefix}] {title} 已存在, 跳过")
                success += 1
                continue

            # 写txt
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            txt_size = os.path.getsize(txt_path)
            print(f"[{prefix}] {title} ({txt_size} 字节文本)")

            # 生成MP3
            if generate_mp3(txt_path, mp3_path, title):
                mp3_size = os.path.getsize(mp3_path)
                print(f"  -> MP3 生成成功 ({mp3_size} 字节)")
                success += 1
            else:
                print(f"  -> MP3 生成失败!")
                failed.append(f"{prefix}-{title}")

        sys.stdout.flush()

    print(f"\n完成: {success} 个文件生成成功")
    if failed:
        print("失败:")
        for f in failed:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
