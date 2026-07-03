import argparse
import datetime as dt
import gzip
import html
import json
import os
import re
import ssl
import time
import urllib.parse
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CACHE_FILE = ROOT / "data_cache.json"
CACHE_SECONDS = 30 * 60
DEFAULT_PORT = 8765

MEM_STATS_URL = "https://www.mem.gov.cn/gk/tjsj/"
MEM_ACCIDENT_URL = "https://www.mem.gov.cn/xw/zhsgxx/"
EARTHQUAKE_URL = "https://data.earthquake.cn/"
MEM_STATS_PAGES = 10
MEM_ACCIDENT_PAGES = 10
MEM_STATS_ARTICLE_LIMIT = 120
MEM_ACCIDENT_ARTICLE_LIMIT = 90

SOURCE_NOTES = [
    "应急管理部统计数据和灾害事故信息已按分页列表抓取历史公告",
    "应急管理部统计栏目中的全国自然灾害情况按自然灾害汇总口径入库",
    "应急管理部网页为公告/新闻口径，服务端按关键词和正则抽取统计字段",
    "国际灾害数据库公开表需要注册登录后下载表格，不能匿名直连抓取"
]

MEM_KEYWORDS = [
    "自然灾害",
    "灾情",
    "洪涝",
    "暴雨",
    "强降雨",
    "山洪",
    "地震",
    "地质灾害",
    "滑坡",
    "泥石流",
    "倒塌房屋",
    "直接经济损失",
]

TYPE_KEYWORDS = {
    "洪涝和地质灾害": ["洪涝和地质灾害", "严重洪涝和地质灾害"],
    "洪涝": ["洪涝", "洪水", "暴雨", "强降雨", "山洪", "内涝"],
    "地质灾害": ["地质灾害", "滑坡", "泥石流", "崩塌"],
    "地震": ["地震", "震灾"],
}

PROVINCES = [
    "北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省",
    "上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省",
    "湖北省", "湖南省", "广东省", "广西壮族自治区", "海南省", "重庆市", "四川省",
    "贵州省", "云南省", "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区",
    "新疆维吾尔自治区", "台湾省", "香港特别行政区", "澳门特别行政区",
]

PROVINCE_ALIASES = {
    "北京": "北京市",
    "天津": "天津市",
    "河北": "河北省",
    "山西": "山西省",
    "内蒙古": "内蒙古自治区",
    "辽宁": "辽宁省",
    "吉林": "吉林省",
    "黑龙江": "黑龙江省",
    "上海": "上海市",
    "江苏": "江苏省",
    "浙江": "浙江省",
    "安徽": "安徽省",
    "福建": "福建省",
    "江西": "江西省",
    "山东": "山东省",
    "河南": "河南省",
    "湖北": "湖北省",
    "湖南": "湖南省",
    "广东": "广东省",
    "广西": "广西壮族自治区",
    "海南": "海南省",
    "重庆": "重庆市",
    "四川": "四川省",
    "贵州": "贵州省",
    "云南": "云南省",
    "西藏": "西藏自治区",
    "陕西": "陕西省",
    "甘肃": "甘肃省",
    "青海": "青海省",
    "宁夏": "宁夏回族自治区",
    "新疆": "新疆维吾尔自治区",
    "台湾": "台湾省",
    "香港": "香港特别行政区",
    "澳门": "澳门特别行政区",
}

MEMORY_CACHE = {
    "records": [],
    "errors": [],
    "updated_at": "",
    "timestamp": 0,
}


def now_text():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def fetch_text(url, timeout=18):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 DisasterDataSystem/1.0"
            )
        },
    )

    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        raw = response.read()
        charset = response.headers.get_content_charset()
        content_encoding = response.headers.get("Content-Encoding", "").lower()

    if raw.startswith(b"\x1f\x8b") or content_encoding == "gzip":
        raw = gzip.decompress(raw)

    if not charset:
        match = re.search(br"charset=['\"]?([a-zA-Z0-9_-]+)", raw[:3000], re.I)
        if match:
            charset = match.group(1).decode("ascii", errors="ignore")

    for encoding in [charset, "utf-8", "gb18030", "gbk"]:
        if not encoding:
            continue
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue

    return raw.decode("utf-8", errors="replace")


def clean_html(fragment):
    fragment = re.sub(r"(?is)<script.*?</script>", " ", fragment)
    fragment = re.sub(r"(?is)<style.*?</style>", " ", fragment)
    fragment = re.sub(r"(?is)<!--.*?-->", " ", fragment)
    text = re.sub(r"(?is)<[^>]+>", " ", fragment)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def extract_title(page_html, fallback=""):
    for pattern in [
        r"(?is)<h1[^>]*>(.*?)</h1>",
        r"(?is)<title[^>]*>(.*?)</title>",
    ]:
        match = re.search(pattern, page_html)
        if match:
            title = clean_html(match.group(1))
            title = re.sub(r"[-_].*$", "", title).strip()
            if title:
                return title
    return fallback


def extract_publish_date(page_html, fallback=""):
    text = clean_html(page_html[:12000])
    for pattern in [
        r"(20\d{2})[-/.年](\d{1,2})[-/.月](\d{1,2})",
        r"(20\d{2})年(\d{1,2})月(\d{1,2})日",
    ]:
        match = re.search(pattern, text)
        if match:
            year, month, day = match.groups()
            return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    return fallback


def extract_paragraphs(page_html):
    paragraphs = [clean_html(item) for item in re.findall(r"(?is)<p[^>]*>(.*?)</p>", page_html)]
    paragraphs = [item for item in paragraphs if len(item) >= 8]
    if paragraphs:
        return paragraphs

    text = clean_html(page_html)
    return [item.strip() for item in re.split(r"[。；;]\s*", text) if len(item.strip()) >= 8]


def extract_links(list_html, base_url, limit=25):
    links = []
    seen = set()

    for match in re.finditer(r"(?is)<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", list_html):
        href = html.unescape(match.group(1)).strip()
        if not href or href.startswith("#") or href.lower().startswith("javascript:"):
            continue

        title = clean_html(match.group(2))
        if len(title) < 6:
            continue

        if not any(keyword in title for keyword in MEM_KEYWORDS):
            continue

        url = urllib.parse.urljoin(base_url, href)
        if url in seen:
            continue

        nearby = list_html[max(0, match.start() - 120): match.end() + 160]
        date_value = extract_event_date(clean_html(nearby)) or ""

        links.append({"title": title, "url": url, "date": date_value})
        seen.add(url)

        if len(links) >= limit:
            break

    return links


def build_list_page_urls(base_url, page_count):
    urls = [base_url]

    for index in range(1, page_count):
        urls.append(urllib.parse.urljoin(base_url, f"index_{index}.shtml"))

    return urls


def extract_links_from_pages(base_url, page_count, limit):
    links = []
    seen = set()

    for page_url in build_list_page_urls(base_url, page_count):
        try:
            page_html = fetch_text(page_url)
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and links:
                break
            raise
        except Exception:
            if links:
                break
            raise

        page_links = extract_links(page_html, page_url, limit=limit)

        for link in page_links:
            if link["url"] in seen:
                continue
            links.append(link)
            seen.add(link["url"])

            if len(links) >= limit:
                return links

        time.sleep(0.08)

    return links


def extract_event_date(text, fallback=""):
    text = text or ""

    match = re.search(r"(20\d{2})\s*[-/.年]\s*(\d{1,2})\s*[-/.月]\s*(\d{1,2})", text)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    match = re.search(r"(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日", text)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    fallback_year = re.search(r"(20\d{2})", fallback or "")
    match = re.search(r"(\d{1,2})\s*月\s*(\d{1,2})\s*日", text)
    if match and fallback_year:
        month, day = match.groups()
        return f"{int(fallback_year.group(1)):04d}-{int(month):02d}-{int(day):02d}"

    match = re.search(r"(20\d{2})\s*年\s*(\d{1,2})\s*月", text)
    if match:
        year, month = match.groups()
        return f"{int(year):04d}-{int(month):02d}-01"

    match = re.search(r"(20\d{2})\s*年", text)
    if match:
        return f"{int(match.group(1)):04d}-01-01"

    return fallback


def classify_disaster_types(title, body):
    combined = f"{title} {body}"
    types = []

    if any(keyword in combined for keyword in TYPE_KEYWORDS["洪涝和地质灾害"]):
        types.append("洪涝和地质灾害")
    else:
        for disaster_type in ["洪涝", "地质灾害"]:
            if any(keyword in combined for keyword in TYPE_KEYWORDS[disaster_type]):
                types.append(disaster_type)

    if any(keyword in combined for keyword in TYPE_KEYWORDS["地震"]):
        types.append("地震")

    if not types and "自然灾害" in combined:
        types.append("自然灾害")

    return types


def select_snippet(disaster_type, paragraphs):
    keywords = TYPE_KEYWORDS.get(disaster_type, [])
    if disaster_type == "洪涝和地质灾害":
        keywords = TYPE_KEYWORDS["洪涝"] + TYPE_KEYWORDS["地质灾害"] + TYPE_KEYWORDS["洪涝和地质灾害"]

    if keywords:
        matches = [item for item in paragraphs if any(keyword in item for keyword in keywords)]
    else:
        matches = []

    selected = matches[:4] if matches else paragraphs[:4]
    return "。".join(selected)[:900]


def extract_location(text, source_name=""):
    if "全国" in text or "应急管理部-统计数据" in source_name:
        return "全国"

    province_matches = []

    for province in PROVINCES:
        for match in re.finditer(re.escape(province), text):
            province_matches.append((match.start(), province))

    for alias, full_name in PROVINCE_ALIASES.items():
        for match in re.finditer(re.escape(alias), text):
            province_matches.append((match.start(), full_name))

    if province_matches:
        locations = []
        seen = set()

        for _, location in sorted(province_matches, key=lambda item: item[0]):
            if location in seen:
                continue
            locations.append(location)
            seen.add(location)

        return "、".join(locations)

    match = re.search(r"([\u4e00-\u9fa5]{2,12}(?:市|县|区|州|盟))", text)
    return match.group(1) if match else "未标明"


def amount_to_person(value, unit):
    number = float(value)
    if unit == "万":
        number *= 10000
    return int(round(number))


def amount_to_hectare(value, unit):
    number = float(value)
    if unit == "千公顷":
        number *= 1000
    elif unit == "万公顷":
        number *= 10000
    elif unit == "万亩":
        number = number * 10000 / 15
    elif unit == "亩":
        number = number / 15
    return int(round(number))


def amount_to_yuan(value, unit):
    number = float(value)
    if unit == "亿元":
        number *= 100000000
    elif unit == "万元":
        number *= 10000
    return int(round(number))


def find_person_metric(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return amount_to_person(match.group(1), match.group(2) or "")
    return None


def find_deaths_missing(text):
    match = re.search(r"(?:因灾)?死亡\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?人[，,、和 ]+失踪\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?人", text)
    if match:
        death = amount_to_person(match.group(1), match.group(2) or "")
        missing = amount_to_person(match.group(3), match.group(4) or "")
        return death + missing

    return find_person_metric(
        text,
        [
            r"(?:因灾)?死亡失踪\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?人",
            r"(?:因灾)?死亡\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?人",
            r"失踪\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?人",
        ],
    )


def extract_metrics(text):
    affected = find_person_metric(
        text,
        [
            r"([0-9]+(?:\.[0-9]+)?)\s*(万)?人次?(?:不同程度)?受灾",
            r"受灾(?:人口|人次)?(?:达|约|近|为)?\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?人",
        ],
    )

    relocated = find_person_metric(
        text,
        [
            r"紧急(?:转移安置|转移|避险转移)(?:人口)?\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?人",
            r"需紧急生活救助\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?人",
        ],
    )

    collapsed_houses = None
    for pattern in [
        r"倒塌房屋\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?\s*(?:余)?(?:间|户)",
        r"房屋倒塌\s*([0-9]+(?:\.[0-9]+)?)\s*(万)?\s*(?:余)?(?:间|户)",
    ]:
        match = re.search(pattern, text)
        if match:
            collapsed_houses = amount_to_person(match.group(1), match.group(2) or "")
            break

    crop_affected_area = None
    match = re.search(r"农作物受灾面积\s*([0-9]+(?:\.[0-9]+)?)\s*(千公顷|万公顷|公顷|万亩|亩)", text)
    if match:
        crop_affected_area = amount_to_hectare(match.group(1), match.group(2))

    direct_economic_loss = None
    match = re.search(r"直接经济损失(?:达|约|近|为)?\s*([0-9]+(?:\.[0-9]+)?)\s*(亿元|万元|元)", text)
    if match:
        direct_economic_loss = amount_to_yuan(match.group(1), match.group(2))

    return {
        "affected_population": affected,
        "deaths_missing": find_deaths_missing(text),
        "emergency_relocated": relocated,
        "collapsed_houses": collapsed_houses,
        "crop_affected_area": crop_affected_area,
        "direct_economic_loss": direct_economic_loss,
    }


def compact_description(title, snippet):
    text = re.sub(r"\s+", " ", f"{title}。{snippet}").strip()
    return text[:240]


def parse_mem_article(page_html, link, source_name):
    title = extract_title(page_html, link["title"])
    publish_date = extract_publish_date(page_html, link.get("date", ""))
    paragraphs = extract_paragraphs(page_html)
    body = " ".join(paragraphs[:20])
    if "全国自然灾害情况" in title:
        disaster_types = ["自然灾害"]
    else:
        disaster_types = classify_disaster_types(title, body)
    records = []

    for disaster_type in disaster_types:
        snippet = select_snippet(disaster_type, paragraphs)
        metric_text = f"{title}。{snippet}"
        metrics = extract_metrics(metric_text)
        start_time = extract_event_date(metric_text, publish_date) or publish_date

        records.append({
            "disaster_type": disaster_type,
            "start_time": start_time,
            "location": extract_location(metric_text, source_name),
            **metrics,
            "damage_description": compact_description(title, snippet),
            "source_name": source_name,
            "source_url": link["url"],
            "source_publish_time": publish_date,
        })

    return records


def collect_mem_records(list_url, source_name, article_limit, page_count=1):
    links = extract_links_from_pages(list_url, page_count=page_count, limit=article_limit)
    records = []

    for link in links:
        try:
            article_html = fetch_text(link["url"])
            records.extend(parse_mem_article(article_html, link, source_name))
            time.sleep(0.15)
        except Exception as exc:
            records.append({
                "disaster_type": "未分类",
                "start_time": link.get("date", ""),
                "location": "未标明",
                "affected_population": None,
                "deaths_missing": None,
                "emergency_relocated": None,
                "collapsed_houses": None,
                "crop_affected_area": None,
                "direct_economic_loss": None,
                "damage_description": f"{link['title']}。文章读取失败：{exc}",
                "source_name": source_name,
                "source_url": link["url"],
                "source_publish_time": link.get("date", ""),
            })

    return records


def normalize_time(text):
    match = re.search(r"(20\d{2})-(\d{1,2})-(\d{1,2})(?:\s+(\d{1,2}):(\d{1,2}):(\d{1,2}))?", text)
    if not match:
        return ""

    year, month, day, hour, minute, second = match.groups()
    if hour:
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d} {int(hour):02d}:{int(minute):02d}:{int(second):02d}"
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"


def parse_earthquake_rows(page_html):
    records = []

    table_rows = re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", page_html)
    for row_html in table_rows:
        cells = [clean_html(cell) for cell in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", row_html)]
        if len(cells) < 7:
            continue

        quake_time = normalize_time(cells[1])
        if not quake_time:
            continue

        try:
            longitude = float(cells[2])
            latitude = float(cells[3])
            depth = float(cells[4])
            magnitude = float(cells[5])
        except ValueError:
            continue

        location = cells[6]
        records.append(make_earthquake_record(quake_time, longitude, latitude, depth, magnitude, location))

    if records:
        return records

    text = clean_html(page_html)
    pattern = (
        r"(20\d{2}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2})\s+"
        r"(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+"
        r"(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+"
        r"(.{2,80}?)(?=\s+20\d{2}-\d{1,2}-\d{1,2}\s+\d{1,2}:|\s+共\d+|\s*$)"
    )

    for match in re.finditer(pattern, text):
        quake_time = normalize_time(match.group(1))
        longitude = float(match.group(2))
        latitude = float(match.group(3))
        depth = float(match.group(4))
        magnitude = float(match.group(5))
        location = match.group(6).strip()
        records.append(make_earthquake_record(quake_time, longitude, latitude, depth, magnitude, location))

    current_year = dt.datetime.now().year
    chinese_pattern = (
        r"(\d{1,2})月(\d{1,2})日(\d{1,2})时(\d{1,2})分"
        r"([\u4e00-\u9fa5A-Za-z0-9·（）()、\-]{2,45}?)"
        r"(?:发生)?(\d+(?:\.\d+)?)级地震"
    )
    for match in re.finditer(chinese_pattern, text):
        month, day, hour, minute, location, magnitude = match.groups()
        quake_time = f"{current_year:04d}-{int(month):02d}-{int(day):02d} {int(hour):02d}:{int(minute):02d}:00"
        records.append(make_simple_earthquake_record(quake_time, float(magnitude), location.strip()))

    records = dedupe_records(records)
    return records


def make_earthquake_record(quake_time, longitude, latitude, depth, magnitude, location):
    return {
        "disaster_type": "地震",
        "start_time": quake_time,
        "location": location,
        "affected_population": None,
        "deaths_missing": None,
        "emergency_relocated": None,
        "collapsed_houses": None,
        "crop_affected_area": None,
        "direct_economic_loss": None,
        "damage_description": (
            f"地震速报：{location}发生M{magnitude:g}级地震，"
            f"震源深度{depth:g}千米，经度{longitude:g}，纬度{latitude:g}。"
        ),
        "source_name": "国家地震科学数据中心",
        "source_url": EARTHQUAKE_URL,
        "source_publish_time": quake_time,
    }


def make_simple_earthquake_record(quake_time, magnitude, location):
    return {
        "disaster_type": "地震",
        "start_time": quake_time,
        "location": location,
        "affected_population": None,
        "deaths_missing": None,
        "emergency_relocated": None,
        "collapsed_houses": None,
        "crop_affected_area": None,
        "direct_economic_loss": None,
        "damage_description": f"地震速报：{location}发生M{magnitude:g}级地震。",
        "source_name": "国家地震科学数据中心",
        "source_url": EARTHQUAKE_URL,
        "source_publish_time": quake_time,
    }


def collect_earthquake_records():
    return parse_earthquake_rows(fetch_text(EARTHQUAKE_URL))


def dedupe_records(records):
    result = []
    seen = set()

    for record in records:
        key = (
            record.get("source_url", ""),
            record.get("disaster_type", ""),
            record.get("start_time", ""),
            record.get("location", ""),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(record)

    return result


def collect_records():
    records = []
    errors = []
    adapters = [
        (
            "应急管理部-统计数据",
            lambda: collect_mem_records(
                MEM_STATS_URL,
                "应急管理部-统计数据",
                MEM_STATS_ARTICLE_LIMIT,
                page_count=MEM_STATS_PAGES,
            ),
        ),
        (
            "应急管理部-灾害事故信息",
            lambda: collect_mem_records(
                MEM_ACCIDENT_URL,
                "应急管理部-灾害事故信息",
                MEM_ACCIDENT_ARTICLE_LIMIT,
                page_count=MEM_ACCIDENT_PAGES,
            ),
        ),
        ("国家地震科学数据中心", collect_earthquake_records),
    ]

    for name, adapter in adapters:
        try:
            records.extend(adapter())
        except Exception as exc:
            errors.append(f"{name}: {exc}")

    records = dedupe_records(records)
    records.sort(key=lambda item: (item.get("start_time") or "", item.get("source_name") or ""), reverse=True)
    return records, errors


def read_cache_file():
    if not CACHE_FILE.exists():
        return None
    try:
        with CACHE_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return None


def write_cache_file(payload):
    with CACHE_FILE.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def get_payload(force_refresh=False):
    now = time.time()

    if (
        not force_refresh
        and MEMORY_CACHE["records"]
        and now - MEMORY_CACHE["timestamp"] < CACHE_SECONDS
    ):
        return {
            "records": MEMORY_CACHE["records"],
            "errors": MEMORY_CACHE["errors"],
            "updated_at": MEMORY_CACHE["updated_at"],
            "source_notes": SOURCE_NOTES,
        }

    cached = read_cache_file()
    if not force_refresh and cached and CACHE_FILE.exists() and now - CACHE_FILE.stat().st_mtime < CACHE_SECONDS:
        MEMORY_CACHE.update({
            "records": cached.get("records", []),
            "errors": cached.get("errors", []),
            "updated_at": cached.get("updated_at", ""),
            "timestamp": now,
        })
        cached["source_notes"] = SOURCE_NOTES
        return cached

    records, errors = collect_records()
    updated_at = now_text()

    if records:
        MEMORY_CACHE.update({
            "records": records,
            "errors": errors,
            "updated_at": updated_at,
            "timestamp": now,
        })
        payload = {
            "records": records,
            "errors": errors,
            "updated_at": updated_at,
            "source_notes": SOURCE_NOTES,
        }
        write_cache_file(payload)
        return payload

    if cached:
        cached_errors = cached.get("errors", [])
        cached_errors.append("当前抓取失败，已返回本地缓存")
        cached["errors"] = errors + cached_errors
        cached["source_notes"] = SOURCE_NOTES
        return cached

    return {
        "records": [],
        "errors": errors or ["未抓取到记录"],
        "updated_at": updated_at,
        "source_notes": SOURCE_NOTES,
    }


class DisasterHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/disasters":
            query = urllib.parse.parse_qs(parsed.query)
            force_refresh = query.get("refresh", ["0"])[0] == "1"
            self.send_json(get_payload(force_refresh=force_refresh))
            return

        super().do_GET()

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(host, port):
    server = ThreadingHTTPServer((host, port), DisasterHandler)
    print(f"灾害信息查询下载系统已启动: http://{host}:{port}/")
    print("按 Ctrl+C 停止服务")
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="灾害信息查询下载系统本地服务")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", DEFAULT_PORT)))
    parser.add_argument("--fetch-test", action="store_true", help="只抓取并打印记录数量，不启动服务")
    args = parser.parse_args()

    if args.fetch_test:
        payload = get_payload(force_refresh=True)
        print(json.dumps({
            "records": len(payload["records"]),
            "errors": payload["errors"],
            "updated_at": payload["updated_at"],
            "first": payload["records"][:2],
        }, ensure_ascii=False, indent=2))
        return

    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
