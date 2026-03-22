#!/usr/bin/env python3
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

CHAT_ID = "o9cq804na37GPmeaMD5IOWO5y1D8@im.wechat"
CHANNEL = "openclaw-weixin"
MAX_AI = 6
MAX_WORLD = 6

AI_FEEDS = [
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("BBC Tech", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
    ("MIT Tech Review AI", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
]

WORLD_FEEDS = [
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
    ("Reuters World", "https://feeds.reuters.com/Reuters/worldNews"),
]


def fetch_titles(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=20).read()
    root = ET.fromstring(data)
    titles = []
    for item in root.findall('.//item'):
        title = (item.findtext('title') or '').strip()
        if not title or title in titles:
            continue
        titles.append(title)
    return titles


def collect_titles(feeds, limit):
    out = []
    seen = set()
    for _source, url in feeds:
        try:
            titles = fetch_titles(url)
        except Exception:
            continue
        for title in titles:
            if title in seen:
                continue
            seen.add(title)
            out.append(title)
            if len(out) >= limit:
                return out
    return out


def has_any(t: str, words):
    tl = t.lower()
    return any(w in tl for w in words)


def summarize_ai(titles):
    if not titles:
        return ["- 今天 AI 源站抓取不太稳定，我稍后会补。"]

    buckets = {
        "大厂与产品": [],
        "Agent与落地": [],
        "监管与风险": [],
        "内容与创作": [],
        "基础设施": [],
        "其他": [],
    }

    for title in titles:
        if has_any(title, ["openai", "anthropic", "google", "gemini", "meta", "xai", "microsoft", "amazon", "apple"]):
            buckets["大厂与产品"].append(title)
        elif has_any(title, ["agent", "assistant", "copilot", "workflow", "automation"]):
            buckets["Agent与落地"].append(title)
        elif has_any(title, ["copyright", "lawsuit", "regulation", "policy", "safety", "misuse", "privacy", "ban"]):
            buckets["监管与风险"].append(title)
        elif has_any(title, ["image", "video", "voice", "creator", "content", "media"]):
            buckets["内容与创作"].append(title)
        elif has_any(title, ["chip", "gpu", "infrastructure", "data center", "compute", "nvidia"]):
            buckets["基础设施"].append(title)
        else:
            buckets["其他"].append(title)

    lines = ["【AI资讯】"]
    used = 0
    if buckets["大厂与产品"]:
        lines.append("- 大厂和产品动作还会是主线，市场盯的不是单次发布，而是谁在抢入口和用户习惯。")
        for t in buckets["大厂与产品"][:2]:
            lines.append(f"  - 参考：{t}")
        used += 1
    if buckets["Agent与落地"] and used < 3:
        lines.append("- Agent 和工作流落地还在推进，重点越来越偏向能不能真正替人干活。")
        for t in buckets["Agent与落地"][:2]:
            lines.append(f"  - 参考：{t}")
        used += 1
    if buckets["监管与风险"] and used < 3:
        lines.append("- 监管、版权和安全问题不会退场，AI 公司一边扩张，一边继续被追问边界。")
        for t in buckets["监管与风险"][:2]:
            lines.append(f"  - 参考：{t}")
        used += 1
    if buckets["内容与创作"] and used < 3:
        lines.append("- 内容生成和创作链路仍在被 AI 改造，平台竞争会继续往创作者端挤压。")
        for t in buckets["内容与创作"][:2]:
            lines.append(f"  - 参考：{t}")
        used += 1
    if used == 0:
        for t in titles[:3]:
            lines.append(f"- 参考：{t}")
    lines.append("- 判断：今天 AI 线大概率还是“大厂推进 + 产品落地 + 风险治理”并行。")
    return lines


def summarize_world(titles):
    if not titles:
        return ["【国际新闻】", "- 今天国际新闻源抓取不太稳定，我稍后补。"]

    buckets = {
        "战争与地缘": [],
        "宏观与经济": [],
        "科技与产业": [],
        "其他": [],
    }

    for title in titles:
        if has_any(title, ["iran", "israel", "ukraine", "gaza", "missile", "attack", "war", "military", "trump"]):
            buckets["战争与地缘"].append(title)
        elif has_any(title, ["inflation", "oil", "fed", "ecb", "economy", "tariff", "market", "rates", "gas"]):
            buckets["宏观与经济"].append(title)
        elif has_any(title, ["ai", "technology", "apple", "tesla", "chip", "nvidia"]):
            buckets["科技与产业"].append(title)
        else:
            buckets["其他"].append(title)

    lines = ["", "【国际新闻】"]
    used = 0
    if buckets["战争与地缘"]:
        lines.append("- 国际线优先看地缘冲突，尤其是中东和大国博弈，这通常直接影响风险偏好和能源价格。")
        for t in buckets["战争与地缘"][:2]:
            lines.append(f"  - 参考：{t}")
        used += 1
    if buckets["宏观与经济"] and used < 3:
        lines.append("- 宏观层面重点盯油价、通胀和央行预期，很多市场波动最后都会回到这条线上。")
        for t in buckets["宏观与经济"][:2]:
            lines.append(f"  - 参考：{t}")
        used += 1
    if buckets["科技与产业"] and used < 3:
        lines.append("- 科技和产业新闻更多是观察长期竞争格局，短线情绪还是会让位给地缘与宏观。")
        for t in buckets["科技与产业"][:2]:
            lines.append(f"  - 参考：{t}")
        used += 1
    if used == 0:
        for t in titles[:3]:
            lines.append(f"- 参考：{t}")
    lines.append("- 判断：今天国际市场若继续围绕战争、能源、通胀交易，风险资产大概率还是偏谨慎。")
    return lines


def build_message():
    now = datetime.now().strftime('%m-%d %H:%M')
    ai_titles = collect_titles(AI_FEEDS, MAX_AI)
    world_titles = collect_titles(WORLD_FEEDS, MAX_WORLD)
    lines = [
        "早上好，苏总。今天 8 点简报来了。🦁",
        f"时间：{now}",
        "",
    ]
    lines.extend(summarize_ai(ai_titles))
    lines.extend(summarize_world(world_titles))
    return "\n".join(lines).strip()


def main():
    msg = build_message()
    subprocess.run([
        "openclaw", "message", "send",
        "--channel", CHANNEL,
        "--target", CHAT_ID,
        "--message", msg,
        "--silent"
    ], check=False)


if __name__ == "__main__":
    main()
