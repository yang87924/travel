"""產生 5 張每日行程卡（.dc.html）與兩張風格草稿、canvas.json。"""
import json
import os

OUT = os.path.dirname(os.path.abspath(__file__))

FONT_LINK = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
             'family=LXGW+WenKai+TC:wght@400;700&amp;family=Noto+Sans+TC:wght@400;500;700'
             '&amp;family=IBM+Plex+Mono:wght@500;600&amp;display=swap">')

CSS = """
body { margin: 0; background: #F4F6F8; }
a { color: #C4622D; } a:hover { color: #1E3350; }
.card {
  --ground: #F4F6F8; --tint: #E6ECF3; --ink: #1E3350; --muted: #57687D; --line: #C3CEDB;
  --hc: #C4622D; --hc-tint: #F4E1D4; --ml: #3A8A63; --ml-tint: #DAEBE1;
  width: 480px; box-sizing: border-box; padding: 26px 26px 24px;
  display: flex; flex-direction: column; gap: 20px;
  background: var(--ground); color: var(--ink);
  font-family: 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif;
}
.kai { font-family: 'LXGW WenKai TC', 'Kaiti TC', 'BiauKai', 'DFKai-SB', serif; }
.mono { font-family: 'IBM Plex Mono', 'Consolas', 'Menlo', 'Noto Sans TC', 'Microsoft JhengHei', monospace; font-variant-numeric: tabular-nums; }
.ticket { background: var(--tint); border-radius: 10px; padding: 16px 18px 14px; display: flex; flex-direction: column; gap: 6px; }
.t-top { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.eyebrow { font-size: 11px; letter-spacing: .14em; color: var(--muted); }
.chips { display: flex; gap: 6px; align-items: center; }
.chip { font-size: 12px; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
.chip.hc { background: var(--hc-tint); color: var(--hc); }
.chip.ml { background: var(--ml-tint); color: var(--ml); }
.chip-arrow { font-size: 12px; color: var(--muted); }
.t-date { display: flex; align-items: baseline; gap: 10px; font-size: 46px; line-height: 1.05; font-weight: 700; }
.t-dow { font-size: 20px; font-weight: 700; }
.t-route { font-size: 14px; line-height: 1.45; text-wrap: balance; }
.perf { position: relative; height: 0; margin: 8px -18px 6px; border-top: 1.5px dashed #A7B4C4; }
.perf::before, .perf::after { content: ''; position: absolute; top: -8px; width: 14px; height: 14px; border-radius: 50%; background: var(--ground); }
.perf::before { left: -7px; }
.perf::after { right: -7px; }
.t-stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
.stat { display: flex; flex-direction: column; gap: 1px; }
.lbl { font-size: 10.5px; letter-spacing: .08em; color: var(--muted); }
.val { font-size: 17px; font-weight: 600; }
.sub { font-size: 10.5px; line-height: 1.4; color: var(--muted); }
.line { position: relative; flex: 1; display: flex; flex-direction: column; }
.line::before {
  content: ''; position: absolute; top: 10px; bottom: 16px; left: 78px; width: 12px; opacity: .5;
  background:
    linear-gradient(90deg, var(--ink) 0 1.5px, transparent 1.5px 10.5px, var(--ink) 10.5px 12px),
    repeating-linear-gradient(180deg, var(--line) 0 2px, transparent 2px 8px);
}
.row { display: grid; grid-template-columns: 56px 28px minmax(0, 1fr); column-gap: 14px; align-items: start; }
.time { font-size: 14px; font-weight: 600; padding-top: 4px; text-align: right; }
.node {
  width: 28px; height: 28px; border-radius: 50%; box-sizing: border-box; z-index: 1;
  display: grid; place-items: center; background: var(--ground); border: 1.75px solid currentColor;
}
.node svg { width: 15px; height: 15px; fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.node.hc { color: var(--hc); }
.node.ml { color: var(--ml); }
.node.train, .node.end { background: var(--ink); color: #FFFFFF; border-color: var(--ink); }
.name { font-size: 17px; font-weight: 700; line-height: 1.3; padding-top: 2px; }
.note { font-size: 12.5px; line-height: 1.45; color: var(--muted); }
.mini .time { font-size: 12px; font-weight: 500; color: var(--muted); padding-top: 0; }
.dot { width: 10px; height: 10px; border-radius: 50%; box-sizing: border-box; justify-self: center; margin-top: 4px; z-index: 1;
  background: var(--ground); border: 1.5px solid var(--muted); }
.mini .txt { font-size: 13px; line-height: 1.45; color: var(--muted); }
.leg { flex: 1 0 20px; align-items: center; }
.leg .l { grid-column: 3; font-size: 10.5px; letter-spacing: .04em; line-height: 20px; color: var(--muted); }
.row.end-row { padding-top: 16px; }
.foot { border: 1.25px dashed var(--line); border-radius: 8px; padding: 12px 14px; display: flex; flex-direction: column; gap: 6px; }
.foot-h { display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 700; letter-spacing: .08em; }
.foot-h svg { width: 14px; height: 14px; fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.foot ul { margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 3px; }
.foot li { font-size: 12.5px; line-height: 1.45; }
"""

ICON = {
    'train': '<rect x="3.5" y="2" width="9" height="9.5" rx="2"></rect><path d="M3.5 7.2h9M6 13.8l-1.3 1.2M10 13.8l1.3 1.2"></path><path d="M6 9.6h.01M10 9.6h.01"></path>',
    'food': '<path d="M2.5 8.2h11a5.5 5.5 0 0 1-11 0z"></path><path d="M8.5 6.2l4.2-4.2M10.6 6.6l3.6-3"></path>',
    'sight': '<path d="M8 14.5s4.5-4.2 4.5-7.6a4.5 4.5 0 0 0-9 0c0 3.4 4.5 7.6 4.5 7.6z"></path><circle cx="8" cy="6.9" r="1.6"></circle>',
    'tea': '<path d="M3 6.8h8v3.2a4 4 0 0 1-8 0z"></path><path d="M11 7.6h1.1a1.8 1.8 0 0 1 0 3.6H11"></path><path d="M5.6 2.4c-.5.7.5 1.3 0 2M8.2 2.4c-.5.7.5 1.3 0 2"></path>',
    'shop': '<path d="M3.5 5.5h9l-.8 9H4.3z"></path><path d="M6 5.5V4.4a2 2 0 0 1 4 0v1.1"></path>',
    'bike': '<circle cx="4" cy="11" r="2.6"></circle><circle cx="12" cy="11" r="2.6"></circle><path d="M4 11l2.8-5h3.4l1.8 5M6.8 6H5.4M9.3 6l-1.6 5"></path>',
    'lantern': '<path d="M8 1.6V3M6 3h4"></path><path d="M5 4.4h6c1 1.2 1.5 2.7 1.5 4.3s-.5 3-1.5 4.2H5c-1-1.2-1.5-2.6-1.5-4.2S4 5.6 5 4.4z"></path><path d="M6.2 12.9v1.5h3.6v-1.5M8 4.4v8.5"></path>',
    'bed': '<path d="M2 12.8V4M2 9.6h12v3.2M14 12.8V9.6"></path><path d="M4.6 9.6V7.6h3.6v2"></path>',
    'home': '<path d="M2.5 7.6L8 3l5.5 4.6v5.9h-11z"></path><path d="M6.5 13.5v-3.6h3v3.6"></path>',
}
ALERT = '<svg viewBox="0 0 16 16"><path d="M8 2.4l6.2 11.2H1.8z"></path><path d="M8 6.6v3.2M8 11.7v.1"></path></svg>'


def svg(name):
    return f'<svg viewBox="0 0 16 16">{ICON[name]}</svg>'


def render_row(r):
    kind = r[0]
    if kind == 'leg':
        return f'<div class="row leg"><span class="l mono">{r[1]}</span></div>'
    if kind == 'mini':
        _, t, txt = r
        return (f'<div class="row mini"><div class="time mono">{t}</div><div class="dot"></div>'
                f'<div class="txt">{txt}</div></div>')
    _, t, icon, tone, name, note = r
    return (f'<div class="row stop"><div class="time mono">{t}</div>'
            f'<div class="node {tone}">{svg(icon)}</div>'
            f'<div><div class="name kai">{name}</div><div class="note">{note}</div></div></div>')


def card_body(d, web=False):
    chips = []
    for i, (label, tone) in enumerate(d['chips']):
        if i:
            chips.append('<span class="chip-arrow">→</span>')
        chips.append(f'<span class="chip {tone}">{label}</span>')
    stats = ''.join(
        f'<div class="stat"><span class="lbl">{a}</span><span class="val mono">{b}</span><span class="sub">{c}</span></div>'
        for a, b, c in d['stats'])
    rows = ''.join(render_row(r) for r in d['rows'])
    et, eicon, ename, enote = d['end']
    end = (f'<div class="row end-row"><div class="time mono">{et}</div>'
           f'<div class="node end">{svg(eicon)}</div>'
           f'<div><div class="name kai">{ename}</div><div class="note">{enote}</div></div></div>')
    checks = ''.join(f'<li>{c}</li>' for c in d['checks'])
    eyebrow = f"DAY {d['day']} / 5" if web else f"DAY {d['day']} / 5　新竹．苗栗 5 天 4 夜"
    tag, attrs = ('section', f' id="day{d["day"]}"') if web else ('div', f' style="height: {d["h"]}px;"')
    return f"""<{tag} class="card"{attrs}>
  <div class="ticket">
    <div class="t-top"><span class="eyebrow mono">{eyebrow}</span><span class="chips">{''.join(chips)}</span></div>
    <div class="t-date kai">{d['date']}<span class="t-dow">{d['dow']}</span></div>
    <div class="t-route">{d['route']}</div>
    <div class="perf"></div>
    <div class="t-stats">{stats}</div>
  </div>
  <div class="line">{rows}{end}</div>
  <div class="foot"><div class="foot-h">{ALERT}出發前確認</div><ul>{checks}</ul></div>
</{tag}>"""


def render_card(d):
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  {FONT_LINK}
  <style>{CSS}</style>
</helmet>
{card_body(d)}
</x-dc>
</body>
</html>
"""


# ===== 網頁版（GitHub Pages 首頁）=====
ITINERARY = '新竹苗栗5天4夜-20260920'

WEB_CSS = """
:root { color-scheme: light; }
body { margin: 0; background: #DCE3EB; color: #1E3350; padding-inline: 16px;
  font-family: 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif; }
.page { max-width: 480px; margin: 0 auto; padding-block: 24px 48px; display: flex; flex-direction: column; gap: 24px; }
.top { display: flex; flex-direction: column; gap: 10px; }
.top h1 { margin: 0; font-size: 30px; line-height: 1.2; font-weight: 700; text-wrap: balance; }
.top p { margin: 0; font-size: 14px; line-height: 1.5; color: #57687D; }
.links { display: flex; flex-wrap: wrap; gap: 8px; }
.links a { display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 999px; font-size: 13px; font-weight: 500;
  text-decoration: none; color: #1E3350; background: #F4F6F8; border: 1px solid #B8C4D2; }
.links a:hover { background: #1E3350; color: #FFFFFF; border-color: #1E3350; }
.links svg { width: 14px; height: 14px; fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.days { position: sticky; top: 0; z-index: 5; margin-inline: -16px; padding: 10px 16px; background: #DCE3EB;
  display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 6px; }
.days a { display: flex; flex-direction: column; align-items: center; gap: 1px; padding: 6px 0 5px; border-radius: 8px; text-decoration: none;
  font-family: 'IBM Plex Mono', 'Consolas', 'Noto Sans TC', monospace; font-size: 15px; font-weight: 600; font-variant-numeric: tabular-nums; }
.days a span { font-family: 'Noto Sans TC', 'Microsoft JhengHei', sans-serif; font-size: 11px; font-weight: 500; }
.days a.hc { background: #F4E1D4; color: #A44E20; }
.days a.ml { background: #DAEBE1; color: #2C6E4E; }
.days a.both { background: linear-gradient(90deg, #F4E1D4 50%, #DAEBE1 50%); color: #1E3350; }
.days a:hover, .days a.today { background: #1E3350; color: #FFFFFF; }
.days a:focus-visible, .links a:focus-visible { outline: 2px solid #1E3350; outline-offset: 2px; }
.card { width: 100%; height: auto; border-radius: 12px; scroll-margin-top: 72px; box-shadow: 0 1px 2px rgba(30, 51, 80, .12); }
.foot-note { margin: 0; font-size: 12px; line-height: 1.6; color: #57687D; text-align: center; }
@media (max-width: 460px) {
  .card { padding: 20px 16px; }
  .ticket { padding: 14px 12px 12px; }
  .perf { margin-inline: -12px; }
  .t-stats { gap: 8px; }
  .val { font-size: clamp(12px, 3.55vw, 17px); }
  .t-date { font-size: 40px; }
  .name { font-size: 16px; }
}
"""

LINK_ICON = {
    'doc': '<svg viewBox="0 0 16 16"><path d="M4 1.8h5.5L12.5 5v9.2H4z"></path><path d="M9.3 1.8V5h3.2M6 8.2h4.5M6 10.8h4.5"></path></svg>',
    'pdf': '<svg viewBox="0 0 16 16"><path d="M8 2v8.2M4.8 7.2L8 10.4l3.2-3.2"></path><path d="M2.8 11.4v2.6h10.4v-2.6"></path></svg>',
}


def render_web():
    from urllib.parse import quote
    months = {'9/20': '2026-09-20', '9/21': '2026-09-21', '9/22': '2026-09-22', '9/23': '2026-09-23', '9/24': '2026-09-24'}
    nav = []
    for d in DAYS:
        tones = [tone for _, tone in d['chips']]
        cls = 'both' if len(set(tones)) > 1 else tones[0]
        nav.append(f'<a class="{cls}" href="#day{d["day"]}" data-date="{months[d["date"]]}">{d["date"]}<span>{d["dow"]}</span></a>')
    cards = chr(10).join(card_body(d, web=True) for d in DAYS)
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>新竹苗栗每日行程卡</title>
<meta name="description" content="新竹・苗栗 5 天 4 夜（2026/9/20–9/24）每日行程卡">
{FONT_LINK}
<style>{CSS}{WEB_CSS}</style>
</head>
<body>
<div class="page">
  <header class="top">
    <h1 class="kai">新竹．苗栗 5 天 4 夜</h1>
    <p>2026/9/20（日）– 9/24（四）・彰化出發・自強3000＋出站租機車・機車每段 30 分鐘內</p>
    <div class="links">
      <a href="{quote(ITINERARY)}.html">{LINK_ICON['doc']}完整行程</a>
      <a href="{quote(ITINERARY)}.pdf">{LINK_ICON['pdf']}PDF 版</a>
    </div>
  </header>
  <nav class="days" aria-label="選擇日期">{''.join(nav)}</nav>
{cards}
  <p class="foot-note">費用都是兩人合計；營業時間以出發前查到的為準。<br>最後更新：2026/9/13</p>
</div>
<script>
(function () {{
  try {{
    var today = new Intl.DateTimeFormat('en-CA', {{ timeZone: 'Asia/Taipei', year: 'numeric', month: '2-digit', day: '2-digit' }}).format(new Date());
    var tab = document.querySelector('.days a[data-date="' + today + '"]');
    if (!tab) return;
    tab.classList.add('today');
    if (!location.hash) document.querySelector(tab.getAttribute('href')).scrollIntoView();
  }} catch (e) {{}}
}})();
</script>
</body>
</html>
"""

DAYS = [
    {
        'file': 'Main.dc.html', 'day': 1, 'date': '9/20', 'dow': '週日',
        'chips': [('新竹', 'hc')],
        'route': '新竹公園 → 城隍廟 → 竹北新瓦屋 → 竹北夜市',
        'stats': [('機車', '50 分', '每段 15 分內'), ('兩人花費', '3,720–4,120', '含住宿、已扣補助'), ('住宿補助', '−800', '你的第 1 晚')],
        'rows': [
            ('stop', '08:18', 'train', 'train', '108 次 自強3000', '彰化 08:18 → 新竹 09:29'),
            ('leg', '步行 3 分'),
            ('mini', '09:32', '出站左轉，源豐機車行取車'),
            ('leg', '機車 5 分'),
            ('mini', '09:52', '承攜中央館寄放行李'),
            ('leg', '機車 5 分'),
            ('stop', '10:05', 'sight', 'hc', '新竹公園＋玻璃工藝博物館', '玻工館 60 分・門票 50；湖畔料亭日式建築'),
            ('leg', '機車 5 分・經過東門城'),
            ('stop', '11:30', 'food', 'hc', '城隍廟＋廟口小吃', '柳家肉燥飯・炒米粉・貢丸湯；13:00 後買周家燒麻糬'),
            ('leg', '機車 15 分'),
            ('stop', '14:05', 'sight', 'hc', '新瓦屋客家文化保存區', '15:00 免費定時導覽；老屋書店、紅瓦紫藤咖啡'),
            ('leg', '機車 11 分'),
            ('stop', '16:45', 'lantern', 'hc', '竹北夜市', '17:00 開始擺攤・晚餐分食 4–5 樣'),
        ],
        'end': ('18:45', 'bed', '承攜行旅新竹中央館', '機車 12 分回來・16:00 後入住'),
        'checks': ['新瓦屋重點是 15:00 免費導覽；走累了，導覽完就去夜市', '竹北夜市出發前看臉書粉專有沒有休市', '早上先寄放行李，晚上回來再入住'],
    },
    {
        'file': 'Day2.dc.html', 'day': 2, 'date': '9/21', 'dow': '週一',
        'chips': [('新竹', 'hc')],
        'route': '北埔老街 → 水井茶堂 → 峨眉湖',
        'stats': [('機車', '1 時 55 分', '每段 25 分內・休息 2 次'), ('兩人花費', '2,370–2,770', '含住宿、已扣補助'), ('住宿補助', '−1,200', '你的第 2 晚')],
        'rows': [
            ('stop', '08:30', 'food', 'hc', '郭家潤餅', '城隍廟口・一人一捲'),
            ('leg', '機車 25 分'),
            ('mini', '09:25', '竹東 中途休息 10 分'),
            ('leg', '機車 13 分'),
            ('stop', '09:48', 'sight', 'hc', '北埔老街', '慈天宮・客家鹹豬肉・黑糖發糕'),
            ('leg', '步行'),
            ('stop', '11:15', 'food', 'hc', '老店客家菜', '薑絲炒大腸＋客家小炒，單點兩道配白飯'),
            ('leg', '步行 3 分'),
            ('stop', '12:05', 'tea', 'hc', '水井茶堂', '天水堂後院的百年老屋，喝北埔膨風茶'),
            ('leg', '步行'),
            ('mini', '12:55', '隆源餅行買伴手禮：番薯餅、柿餅'),
            ('leg', '機車 20 分'),
            ('stop', '13:35', 'sight', 'hc', '峨眉湖', '細茅埔吊橋・環湖步道・72 m 彌勒大佛'),
            ('leg', '機車 25 分'),
            ('mini', '15:25', '寶山 中途休息 10 分'),
            ('leg', '機車 17 分'),
            ('mini', '15:52', '回旅館休息'),
            ('leg', '機車 5 分'),
            ('stop', '17:15', 'food', 'hc', '鴨肉許（許二姊）', '炒鴨肉麵・鴨肉飯・炒鴨血'),
        ],
        'end': ('18:40', 'bed', '承攜行旅新竹中央館', '機車 5 分回來・續住'),
        'checks': ['週一北埔部分店家休：前一天打給水井茶堂 03-580-5122', '彌勒殿週一休館，大佛從吊橋和湖邊看', '鴨肉許排太久，改西市汕頭館沙茶牛肉炒麵'],
    },
    {
        'file': 'Day3.dc.html', 'day': 3, 'date': '9/22', 'dow': '週二',
        'chips': [('新竹', 'hc'), ('苗栗', 'ml')],
        'route': '早上慢慢來 → 自強號 → 苗栗火車頭園區',
        'stats': [('機車', '35 分', '每段 8 分內'), ('兩人花費', '4,870–5,170', '含住宿、已扣補助'), ('住宿補助', '−800', '媽媽的第 1 晚')],
        'rows': [
            ('stop', '09:05', 'food', 'hc', '阿忠肉圓', '紅糟肉圓＋貢丸湯・前兩天累了，睡飽再出門'),
            ('leg', '步行'),
            ('mini', '09:50', '淵明餅舖伴手禮：水蒸蛋糕、竹塹餅、貢丸'),
            ('leg', '機車 5 分'),
            ('mini', '10:30', '承攜退房，10:45 站前還機車'),
            ('leg', '步行 3 分'),
            ('stop', '11:25', 'train', 'train', '117 次 自強3000', '新竹 11:25 → 苗栗 11:50'),
            ('leg', '步行 2 分'),
            ('mini', '11:55', '出站就到建泰機車行取車'),
            ('leg', '機車 8 分・繞到後站'),
            ('mini', '12:20', '禾家商旅寄放行李'),
            ('leg', '機車 3 分'),
            ('stop', '12:30', 'food', 'ml', '文化麵食館', '葫瓜鮮肉水餃・香辣老虎麵'),
            ('leg', '機車 3 分'),
            ('stop', '13:15', 'sight', 'ml', '苗栗火車頭園區', '12 列經典火車頭・門票 100（含 50 元折抵）'),
            ('leg', '機車 3 分'),
            ('mini', '15:05', '禾家入住、休息、洗衣服'),
            ('leg', '機車 8 分'),
            ('stop', '17:40', 'food', 'ml', '貢鍋共鍋', '老洋宅・小份客家小炒鍋＋水晶餃、蛋餃'),
        ],
        'end': ('19:10', 'bed', '禾家商旅', '機車 8 分回來・含早餐'),
        'checks': ['文化麵食館公休日不明，沒開改林家鴨香飯', '貢鍋先打電話訂位 037-276727', '火車頭園區平日 17:00 關門'],
    },
    {
        'file': 'Day4.dc.html', 'day': 4, 'date': '9/23', 'dow': '週三',
        'chips': [('苗栗・三義', 'ml')],
        'route': '木雕博物館 → 鐵道自行車 → 卓也小屋 → 英才夜市',
        'stats': [('機車', '2 時 15 分', '每段 27 分內・休息 2 次'), ('兩人花費', '4,530–4,830', '含住宿、已扣補助'), ('住宿補助', '−1,200', '媽媽的第 2 晚')],
        'rows': [
            ('mini', '08:57', '銅鑼 中途休息 10 分（08:30 從禾家出發）'),
            ('leg', '機車 18 分'),
            ('stop', '09:25', 'sight', 'ml', '三義木雕博物館', '09:00 開門・門票 80'),
            ('leg', '機車 9 分'),
            ('stop', '10:25', 'sight', 'ml', '勝興車站・勝興老街', '西部鐵路最高的百年木造車站'),
            ('leg', '步行 5 分'),
            ('stop', '11:20', 'bike', 'ml', '舊山線鐵道自行車 A', '10:50 報到・經魚藤坪鐵橋看斷橋・275'),
            ('leg', '步行'),
            ('stop', '12:45', 'food', 'ml', '七姊八弟山城小店', '客家菜兩人套餐'),
            ('leg', '機車 15 分'),
            ('stop', '13:55', 'sight', 'ml', '卓也小屋', '14:00 藍染 DIY 方巾 300・入園 200'),
            ('leg', '機車 15 分'),
            ('stop', '15:55', 'shop', 'ml', '三義木雕街', '水美街・木雕小物'),
            ('leg', '機車 16 分'),
            ('mini', '16:51', '銅鑼 中途休息 10 分'),
            ('leg', '機車 26 分'),
            ('mini', '17:27', '回禾家休息'),
            ('leg', '機車 5 分'),
            ('stop', '18:15', 'lantern', 'ml', '英才觀光夜市', '苗栗最大・炸臭豆腐、微豆豆花'),
        ],
        'end': ('19:55', 'bed', '禾家商旅', '機車 5 分回來・續住'),
        'checks': ['鐵道自行車 11:20 班要先在官網訂好', '卓也的蔬食餐廳週三休，只玩園區和藍染', '英才夜市出發前看臉書粉專'],
    },
    {
        'file': 'Day5.dc.html', 'day': 5, 'date': '9/24', 'dow': '週四',
        'chips': [('苗栗', 'ml'), ('彰化', 'hc')],
        'route': '客家文化園區 → 南苗老店 → 功維敘隧道 → 回家',
        'stats': [('機車', '1 時 10 分', '每段 27 分內'), ('兩人花費', '約 1,030', '車票＋午餐＋油錢'), ('抵達彰化', '15:18', '125 次 自強3000')],
        'rows': [
            ('mini', '08:15', '禾家退房、寄放行李（早餐 07:30）'),
            ('leg', '機車 27 分'),
            ('stop', '09:00', 'sight', 'ml', '苗栗客家文化園區', '臺灣客家文化館・免費・週二休'),
            ('leg', '機車 22 分'),
            ('stop', '11:25', 'food', 'ml', '湯家大肉圓', '大肉圓分著吃・苗栗熱狗・肉羹湯'),
            ('leg', '步行 5–10 分'),
            ('stop', '12:00', 'food', 'ml', '江技舊記', '70 年餛飩、水晶餃；最後買冷凍水晶餃'),
            ('leg', '機車 5 分'),
            ('stop', '12:55', 'sight', 'ml', '功維敘隧道＋貓貍山公園', '百年鐵道隧道 LED 光廊'),
            ('leg', '機車 10 分'),
            ('mini', '13:50', '禾家取行李，14:00 建泰還車'),
            ('leg', '步行 5 分'),
            ('stop', '14:30', 'train', 'train', '125 次 自強3000', '苗栗 14:30 → 彰化 15:18'),
        ],
        'end': ('15:18', 'home', '抵達彰化站', '回鹿港，連假前一天避開晚上人潮'),
        'checks': ['125 次是全趟最急的票，今天就訂', '買冷凍水晶餃，請店家加保冷袋', '想晚點回家就改搭 139 次 18:32'],
    },
]

def estimate_height(d):
    def lines(s, per):
        return max(1, -(-len(s) // per))
    h = 50 + 40 + 240 + 24 + 20
    h += sum(18 * lines(c, 28) + 3 for c in d['checks'])
    for r in d['rows']:
        if r[0] == 'leg':
            h += 20
        elif r[0] == 'mini':
            h += 19 * lines(r[2], 23)
        else:
            h += max(28, 24 + 18 * lines(r[5], 24))
    h += 16 + 24 + 18
    return -(-int(h * 1.05) // 20) * 20


def main():
    names = []
    for d in DAYS:
        d['h'] = estimate_height(d)
        with open(os.path.join(OUT, d['file']), 'w', encoding='utf-8') as fh:
            fh.write(render_card(d))
        names.append(d['file'])
    titles = ['DAY 1｜9/20（日）新竹', 'DAY 2｜9/21（一）新竹', 'DAY 3｜9/22（二）新竹→苗栗',
              'DAY 4｜9/23（三）苗栗三義', 'DAY 5｜9/24（四）苗栗→彰化']
    boards = [{'file': d['file'], 'x': i * 560, 'y': 0, 'w': 480, 'h': d['h'], 'title': ti}
              for i, (d, ti) in enumerate(zip(DAYS, titles))]
    canvas = {'artboards': boards, 'launch': {'view': 'canvas'}}
    with open(os.path.join(OUT, 'canvas.json'), 'w', encoding='utf-8') as fh:
        json.dump(canvas, fh, ensure_ascii=False, indent=2)
    print('wrote', len(names), 'artboards:', [(d['file'], d['h']) for d in DAYS])
    with open(os.path.join(OUT, '..', 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(render_web())
    print('wrote ../index.html')


if __name__ == '__main__':
    main()
