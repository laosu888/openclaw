#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
from datetime import datetime

FEEDS = [
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("BBC Tech", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
]

TARGET = "channel:1470395395233419357"
CHANNEL = "discord"
MAX_ITEMS = 6


def fetch_titles(url):
    data = urllib.request.urlopen(url, timeout=20).read()
    root = ET.fromstring(data)
    titles = []
    for item in root.findall('.//item'):
        title = (item.findtext('title') or '').strip()
        if not title:
            continue
        if title in titles:
            continue
        titles.append(title)
    return titles


def classify_topic(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ["openai", "anthropic", "google", "gemini", "meta", "xai", "microsoft", "amazon"]):
        return "大厂动作"
    if any(k in t for k in ["copyright", "lawsuit", "regulation", "policy", "ban", "safety", "misuse", "privacy"]):
        return "监管与风险"
    if any(k in t for k in ["agent", "assistant", "copilot", "automation", "workflow"]):
        return "Agent与产品落地"
    if any(k in t for k in ["chip", "gpu", "nvidia", "infrastructure", "data center", "compute"]):
        return "算力与基础设施"
    if any(k in t for k in ["video", "image", "voice", "creator", "content", "media"]):
        return "内容与创作"
    return "行业动态"


def build_chinese_takeaways(all_titles):
    buckets = {}
    for title in all_titles:
        topic = classify_topic(title)
        buckets.setdefault(topic, []).append(title)

    priority = ["大厂动作", "Agent与产品落地", "监管与风险", "内容与创作", "算力与基础设施", "行业动态"]
    lines = []

    if not all_titles:
        return ["- 今天早上源站抓取异常，我晚点补一版中文简报。"]

    lines.append("今天 AI 简报先看三件事：")
    count = 0
    for topic in priority:
        if topic not in buckets:
            continue
        count += 1
        sample = buckets[topic][:2]
        if topic == "大厂动作":
            lines.append(f"- **大厂动作**：今天外媒重点仍在头部公司动作，说明行业主线还是平台级竞争和产品节奏。")
        elif topic == "Agent与产品落地":
            lines.append(f"- **Agent与产品落地**：AI 正继续从演示走向真实工作流，重点不只是模型更强，而是工具开始更能干活。")
        elif topic == "监管与风险":
            lines.append(f"- **监管与风险**：版权、滥用、安全和责任问题还在持续抬头，AI 公司一边扩张，一边也在被追着问边界。")
        elif topic == "内容与创作":
            lines.append(f"- **内容与创作**：今天内容生产和创作者相关信号偏多，说明 AI 对媒体、视频、图像和创作链路的改造还在加速。")
        elif topic == "算力与基础设施":
            lines.append(f"- **算力与基础设施**：底层算力和基础设施依旧是这轮 AI 竞争的硬骨头，谁能稳住供给，谁就更有主动权。")
        else:
            lines.append(f"- **行业动态**：今天还有一些杂项更新，但核心没有变，AI 竞争已经越来越像系统战，不只是模型战。")

        for s in sample:
            lines.append(f"  - 参考原题：{s}")
        if count >= 3:
            break

    lines.append("")
    lines.append("一句话判断：今天 AI 圈依旧是 **大厂推进 + 产品落地 + 监管跟进** 三条线一起走。")
    return lines


def build_message():
    lines = ["[[reply_to_current]]早上 AI 简报来了。🦁", "", f"时间：{datetime.now().strftime('%m-%d %H:%M')}", ""]
    all_titles = []

    for _source, url in FEEDS:
        try:
            titles = fetch_titles(url)
        except Exception:
            continue
        all_titles.extend(titles[:3])
        if len(all_titles) >= MAX_ITEMS:
            break

    all_titles = all_titles[:MAX_ITEMS]
    lines.extend(build_chinese_takeaways(all_titles))
    return "\n".join(lines).strip()


def main():
    msg = build_message()
    subprocess.run([
        "openclaw", "message", "send",
        "--channel", CHANNEL,
        "--target", TARGET,
        "--message", msg,
        "--silent"
    ], check=False)


if __name__ == "__main__":
    main()
