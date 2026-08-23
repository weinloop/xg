#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文分段配音生成器
- 将论文按段落切分，每段生成男声 MP3（edge-tts 云扬男声 zh-CN-YunyangNeural，语速+10%）
- 生成 index.html：每段卡片含配音播放器 + 展开/收起按钮（同一按钮），全局展开/收起按钮
"""
import os
import re
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
EDGE_TTS = "/Users/aus/.workbuddy/binaries/python/envs/default/bin/edge-tts"
VOICE = "zh-CN-YunyangNeural"
RATE = "+10%"

os.makedirs(AUDIO_DIR, exist_ok=True)

# ============ 段落定义 ============
# (标题, 朗读前缀, 正文, 是否有表格(显示用), 表格HTML)
SEGMENTS = [
    {
        "title": "开头段 · 项目全貌",
        "prefix": "开头段。",
        "text": "某航空集团为加速推进数字化转型，于2024年8月正式启动数据资产智能管理平台项目建设。"
                "该项目旨在全面打通集团总部、5大区域中心和23家分公司的数据壁垒，实现数据资产治理一体化管理平台。"
                "项目投资580万元/年，服务期1年，服务内容包括数据资产目录管理、数据质量管理、数据共享管理、"
                "数据安全管控、数据血缘图谱、智能问答、运维监控中心7大功能模块。"
                "客户明确要求：系统可用性≥99.99%，页面查询响应时间≤2秒，支持5000并发用户，年数据服务调用≥10亿次，"
                "数据资产目录≥10万项，质量规则≥5000条。"
                "我作为中标方系统规划与管理师，全面负责项目的服务体系建设与信息系统服务设计实现工作。"
                "我依据ITSS标准，组建了一支12人的运维团队，包括系统规划与管理师1人、数据管家2人、运维工程师3人、"
                "安全工程师2人、数据库工程师2人、综合岗2人，实行A/B角与定期轮岗机制，确保服务连续性。"
                "安排3名运维工程师常驻总部数据中心，提供7×24现场运维；综合岗负责服务台调度与远程监控，"
                "另配1名技术专家提供远程协助，形成“现场+远程”双线联动模式。"
                "项目运行期间，系统可用性达99.995%，无重大数据安全事件，运维数据备份完整率100%，SLA指标全面达成，"
                "2025年9月平台正式上线并通过验收，赢得集团数据治理委员会高度认可。",
    },
    {
        "title": "过渡段 · 论述方向",
        "prefix": "过渡段。",
        "text": "本项目涉及航班客运、旅客服务、机务维修、地面服务等多个高耦合业务域，"
                "120余套核心系统数据汇聚，一旦服务中断将直接影响该集团8万员工的日常运营和数千万旅客的出行服务。"
                "因此，我将信息系统服务设计实现摆在核心位置。结合项目实践，从服务模式设计、人员要素设计、"
                "资源要素设计、技术要素设计、过程要素设计五个方面，论述信息系统服务设计实现的重要性。",
    },
    {
        "title": "一、服务模式设计",
        "prefix": "一、服务模式设计。",
        "text": "服务模式设计是指信息系统服务供方结合服务需求分析结果，对服务模式进行设计，"
                "根据客户需求和服务内容提供不同模式的服务。常见的信息系统服务模式分为远程服务"
                "（远程集中监控、远程技术支持）和现场服务（上门技术支持、驻场技术支持）两类。"
                "在项目初期，我充分评估了集团可用性≥99.99%、连续性和安全性等高要求的服务需求，"
                "设计了“驻场+远程”双线联动服务模式。安排3名运维工程师常驻总部数据中心，提供7×24现场驻场技术支持，"
                "确保核心业务系统故障能在第一时间现场响应；综合岗通过Prometheus+Grafana监控平台实施远程集中监控，"
                "实时掌握5大区域中心和23家分公司的系统运行状态；另配1名数据库技术专家提供远程技术支持，处理复杂技术问题。"
                "2024年11月，华东区域中心数据库主从切换异常，远程监控平台在30秒内自动告警，驻场工程师5分钟内到达机房现场，"
                "远程技术专家同步接入排查，15分钟内完成主从重建，未影响任何前端业务。"
                "该模式经6个月试运行验证，事件平均响应时间9.6分钟，远优于15分钟的目标值，充分验证了多模式协同设计的有效性。",
    },
    {
        "title": "二、人员要素设计",
        "prefix": "二、人员要素设计。",
        "text": "人员要素设计是服务设计实现阶段必不可少的一环，通过对人员岗位和职责、人员绩效、人员培训三方面的设计，"
                "确保服务团队组织架构与服务需求和服务模式相适应，确保服务人员的能力持续满足服务需求。"
                "我在项目中建立了管理岗、技术支持岗、操作岗三类岗位体系：管理岗由我担任系统规划与管理师，统筹服务需求管理和过程控制；"
                "技术支持岗包括数据管家2人、运维工程师3人、安全工程师2人、数据库工程师2人共9人，负责专业技术支持；"
                "操作岗由综合岗2人担任，负责服务台调度和远程监控。"
                "在绩效方案设计方面，我针对不同岗位定义了差异化绩效指标，例如一线运维工程师以事件解决率和响应时间为核心指标，"
                "数据管家以数据质量闭环率和资产目录完整率为核心指标，每季度考核一次。"
                "在培训方案设计方面，我制定了涵盖管理培训、技术培训、工具培训、过程培训、交付和应急培训五类内容的培训计划。"
                "2024年9月，一名新任数据管家因不熟悉数据脱敏规则导致核心航班号字段误脱敏，引发业务投诉。"
                "我立即暂停其高危操作权限，组织专项过程培训和工具培训，编制《数据操作红线手册》，并实施“双人复核”机制。"
                "三个月后该人员通过考核返岗，团队操作规范性显著提升，培训效果评价满意度从72%提升至91%。",
    },
    {
        "title": "三、资源要素设计",
        "prefix": "三、资源要素设计。",
        "text": "资源要素设计是确保服务供方具备提供足够资源能力的关键环节，主要包括服务工具、服务台、备件库和知识库四类资源的设计。"
                "在服务工具设计方面，我部署了监控类工具（Prometheus+Grafana实现资源指标采集与可视化）和过程管理类工具"
                "（ITSM平台实现事件、问题、变更全流程管理），并根据团队技术水平编写了工具使用规范手册。"
                "在服务台设计方面，我建立了统一服务联络点，配置了热线电话、企业微信服务群和邮件工单系统三种沟通渠道，"
                "设定综合岗专人负责服务请求受理、记录和跟踪反馈。"
                "在备件库设计方面，我为核心数据库服务器和网络交换机配置了关键备件，制定了备件出入库管理流程和定期巡检制度。"
                "在知识库设计方面，初期我鼓励运维人员主动记录经验，但3个月仅积累60条知识，远低于500条目标。"
                "随后我将知识条目纳入运维KPI考核，要求每人每月至少贡献5条有效条目，并设置质量评审机制。"
                "试运行结束时知识库已积累520条，涵盖常见故障处理、数据质量规则校验、应急预案操作步骤等内容，"
                "知识库日均查询量达45次，有效提升了事件一线解决率从62%提升至85%。",
    },
    {
        "title": "四、技术要素设计",
        "prefix": "四、技术要素设计。",
        "text": "技术要素设计是保障服务供方具备发现和解决问题、风险控制能力的关键，系统规划与管理师应从技术研发、"
                "发现问题的技术、解决问题的技术三个方面进行考量。"
                "在技术研发方面，我在设计阶段组织团队开发了数据质量规则引擎，支持5000条以上规则的动态加载与执行，"
                "并预留了智能问答模块的技术研发预算。"
                "在发现问题的技术方面，我制定了覆盖CPU、内存、磁盘IO、网络带宽、数据库连接数等42项监控指标的监控指标及阈值表，"
                "并搭建了仿真测试环境，模拟120套核心系统数据并发接入场景，提前发现并修复了3处性能瓶颈。"
                "在解决问题的技术方面，我针对数据备份恢复、数据库主从切换、核心API熔断等12类高频技术活动编写了标准操作流程（SOP），"
                "并制定了数据误删恢复、API服务熔断切换、敏感数据泄露应急等5项应急预案。"
                "2024年12月，数据血缘扫描任务因资源隔离不足导致CPU飙升，触发数据库查询超时。"
                "因初期采用固定告警阈值未能及时预警，我随即改用“动态基线”策略，基于历史7天数据自动计算告警阈值，"
                "异常波动即时预警，主动发现率从60%提升至95%，技术要素设计从被动响应转向了主动防御。",
    },
    {
        "title": "五、过程要素设计 · 关键指标表",
        "prefix": "五、过程要素设计。",
        "text": "过程要素设计是服务需求实现的保障，通过规范的流程使服务更加轨道化、标准化、规范化。"
                "常见的信息系统服务管理过程包括服务级别管理、服务报告管理、事件管理、问题管理、配置管理、变更管理、"
                "发布管理和信息安全管理共8大过程。我在项目中逐一设计了这8大过程的活动、顺序和考核指标，"
                "以下选取4个核心过程展示关键指标设计。",
        "table_html": (
            "<table class=\"data-table\"><thead><tr>"
            "<th>过程名称</th><th>关键指标</th><th>预订目标值</th><th>实际达成值</th><th>考核评价</th>"
            "</tr></thead><tbody>"
            "<tr><td rowspan=\"3\">事件管理</td><td>平均响应时间</td><td>≤15.0分钟</td><td>9.6分钟</td><td>达标</td></tr>"
            "<tr><td>平均解决时间</td><td>≤8.0小时</td><td>5.2小时</td><td>达标</td></tr>"
            "<tr><td>事件及时解决率</td><td>≥95.0%</td><td>97.3%</td><td>达标</td></tr>"
            "<tr><td rowspan=\"2\">问题管理</td><td>重复故障发生率</td><td>≤5.0%</td><td>1.8%</td><td>达标</td></tr>"
            "<tr><td>问题平均解决时间</td><td>≤72.0小时</td><td>48.6小时</td><td>达标</td></tr>"
            "<tr><td rowspan=\"2\">变更管理</td><td>变更成功率</td><td>≥98.0%</td><td>99.2%</td><td>达标</td></tr>"
            "<tr><td>未经批准变更占比</td><td>≤2.0%</td><td>0.5%</td><td>达标</td></tr>"
            "<tr><td rowspan=\"2\">配置管理</td><td>配置项准确率</td><td>≥95.0%</td><td>97.8%</td><td>达标</td></tr>"
            "<tr><td>配置信息更新及时率</td><td>≥90.0%</td><td>94.5%</td><td>达标</td></tr>"
            "</tbody></table>"
        ),
        "table_spoken": "以下选取4个核心过程展示关键指标设计。事件管理方面，平均响应时间，预订目标值为不超过15分钟，"
                "实际达成9.6分钟，考核评价达标；平均解决时间，目标不超过8小时，实际5.2小时，达标；"
                "事件及时解决率，目标不低于95%，实际97.3%，达标。问题管理方面，重复故障发生率，目标不超过5%，"
                "实际1.8%，达标；问题平均解决时间，目标不超过72小时，实际48.6小时，达标。"
                "变更管理方面，变更成功率，目标不低于98%，实际99.2%，达标；未经批准变更占比，目标不超过2%，"
                "实际0.5%，达标。配置管理方面，配置项准确率，目标不低于95%，实际97.8%，达标；"
                "配置信息更新及时率，目标不低于90%，实际94.5%，达标。",
    },
    {
        "title": "五、过程要素设计 · 执行闭环",
        "prefix": "过程要素执行闭环。",
        "text": "在过程执行过程中，我建立了闭环验证机制：事件关闭后自动触发满意度调查，"
                "问题解决后必须导入知识库形成经验沉淀，变更实施后48小时内完成配置数据库同步更新。"
                "2025年2月，一次数据库版本升级变更因未充分考虑与数据血缘图谱模块的兼容性导致血缘解析异常，"
                "触发问题管理流程，经调查诊断后回退变更并优化变更评估清单，补充了“跨模块兼容性验证”检查项，"
                "此后变更成功率始终保持在99%以上。过程要素设计的规范化使服务管理从经验驱动转向标准驱动，"
                "为SLA全面达标提供了坚实的流程保障。",
    },
    {
        "title": "结尾段 · 总结展望",
        "prefix": "结尾段。",
        "text": "2025年9月，项目顺利通过验收并成功续签合同，平台各项SLA指标全部达标，赢得了集团数据治理委员会的高度称赞。"
                "本项目的成功，一方面来自于团队高效的协作与专业的技术实力，另一方面更得益于我在项目中对信息系统服务设计实现的有效运用。"
                "作为系统规划与管理师，我深刻体会到：只有将服务设计实现贯穿服务全生命周期，从服务模式选择到人员、资源、技术、"
                "过程四要素逐层设计，才能真正筑牢运维防线，保障核心业务稳定运行。"
                "当然，项目过程中也存在不足，例如初期知识库建设进展缓慢导致运维经验无法有效沉淀，"
                "以及固定告警阈值未能及时发现资源异常波动，这些问题给项目带来一定压力，但都被我有效解决。"
                "未来，我将持续学习ITSS标准，不断提升专业能力，沉淀系统规划管理经验，助力该航空集团数字化高质量发展。",
    },
]


def spoken_text(seg: dict) -> str:
    """生成朗读文本：前缀 + 正文（≥/≤ 转口语，去除引号等）"""
    text = seg["prefix"] + seg["text"]
    if seg.get("table_spoken"):
        text += seg["table_spoken"]
    # 口语化处理
    text = text.replace("≥", "不低于").replace("≤", "不超过")
    text = text.replace("“", "").replace("”", "").replace("‘", "").replace("’", "")
    text = text.replace("A/B角", "A B角")
    # 规整空白
    text = re.sub(r"\s+", " ", text).strip()
    return text


def render_para_html(seg: dict) -> str:
    """渲染段落正文 HTML（含表格）"""
    # 正文按句拆分为 <p> 便于阅读
    para = seg["text"].replace("\n", "")
    # 先按中文标点分句
    sentences = re.findall(r"[^。！？]*[。！？]", para)
    if not sentences:
        sentences = [para]
    body = "".join(f"<p>{s.strip()}</p>" for s in sentences if s.strip())
    if seg.get("table_html"):
        body += seg["table_html"]
    return body


def gen_mp3(text: str, out_path: str) -> bool:
    """调用 edge-tts 生成 MP3，失败自动重试一次"""
    txt_path = out_path.replace(".mp3", ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    for attempt in (1, 2):
        try:
            r = subprocess.run(
                [EDGE_TTS, "-f", txt_path, "--voice", VOICE, "--rate", RATE,
                 "--write-media", out_path],
                capture_output=True, text=True, timeout=120,
            )
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                return True
            print(f"  [尝试{attempt}] 输出为空: {r.stderr.strip()[:200]}")
        except Exception as e:
            print(f"  [尝试{attempt}] 异常: {e}")
    return False


def build_html() -> str:
    segs = []
    for i, seg in enumerate(SEGMENTS, 1):
        audio = f"audio/{i:02d}-{seg['title'].split('·')[0].strip()}.mp3"
        segs.append({
            "num": i,
            "title": seg["title"],
            "audio": audio,
            "body": render_para_html(seg),
        })
    return render_index(segs)


def render_index(segs) -> str:
    cards = []
    for s in segs:
        cards.append(f"""
      <section class="card" data-idx="{s['num']}">
        <div class="card-head">
          <button class="toggle" onclick="toggleCard({s['num']})" title="展开/收起" aria-expanded="true">
            <svg class="tgl-icon" viewBox="0 0 24 24" width="16" height="16"><path d="M7 10l5 5 5-5z" fill="currentColor"/></svg>
          </button>
          <div class="card-title" onclick="toggleCard({s['num']})">
            <span class="num-badge">{s['num']}</span>
            <span class="title-text">{s['title']}</span>
          </div>
          <div class="player" data-audio="{s['audio']}">
            <button class="play-btn" onclick="togglePlay(this)" title="播放/暂停">▶</button>
            <div class="prog" onclick="seek(event)">
              <div class="prog-fill"></div>
            </div>
            <span class="time">0:00 / 0:00</span>
          </div>
        </div>
        <div class="card-body" id="body-{s['num']}">
          {s['body']}
        </div>
      </section>""")
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>论文 · 论信息系统服务设计实现（分段配音）</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang SC','Microsoft YaHei',sans-serif;
  background:linear-gradient(180deg,#f7f9fc 0%,#eef1f6 100%);color:#2c3e50;line-height:1.75;min-height:100vh}}
.container{{max-width:880px;margin:0 auto;padding:20px 16px 60px}}

/* 头部 */
.page-head{{background:#fff;border:1px solid #e3e8f0;border-radius:16px;padding:22px 24px;margin-bottom:18px;
  box-shadow:0 2px 10px rgba(30,50,90,.05)}}
.page-head h1{{font-size:22px;color:#1a2b4a;margin-bottom:6px}}
.page-head .sub{{font-size:13px;color:#7a8aa0}}
.toolbar{{display:flex;gap:10px;margin-top:14px;flex-wrap:wrap}}
.toolbar button{{border:1px solid #d4dce8;background:#fff;color:#2c5fae;font-size:13px;font-weight:600;
  padding:8px 16px;border-radius:10px;cursor:pointer;transition:all .2s;display:flex;align-items:center;gap:6px}}
.toolbar button:hover{{background:#eef4ff;border-color:#2c5fae}}
.toolbar .hint{{margin-left:auto;font-size:12px;color:#9aa8bc;align-self:center}}

/* 卡片 */
.card{{background:#fff;border:1px solid #e3e8f0;border-radius:16px;margin-bottom:14px;overflow:hidden;
  box-shadow:0 2px 10px rgba(30,50,90,.05);transition:box-shadow .2s}}
.card:hover{{box-shadow:0 4px 16px rgba(30,50,90,.10)}}
.card-head{{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid #eef1f6}}
.card.collapsed .card-head{{border-bottom:none}}
.toggle{{width:30px;height:30px;flex-shrink:0;border:none;background:#eef4ff;color:#2c5fae;border-radius:8px;
  cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .25s}}
.card.collapsed .tgl-icon{{transform:rotate(-90deg)}}
.card-title{{flex:1;min-width:0;display:flex;align-items:center;gap:10px;cursor:pointer;user-select:none}}
.num-badge{{width:26px;height:26px;flex-shrink:0;background:#2c5fae;color:#fff;border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700}}
.title-text{{font-size:16px;font-weight:600;color:#1a2b4a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}

/* 播放器 */
.player{{display:flex;align-items:center;gap:10px;min-width:230px;max-width:46%;flex-shrink:0}}
.play-btn{{width:36px;height:36px;flex-shrink:0;border:none;border-radius:50%;background:#2c5fae;color:#fff;
  font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s}}
.play-btn:hover{{background:#1e4a92}}
.play-btn.playing{{background:#e2574c}}
.play-btn.playing::before{{content:'⏸';}}
.play-btn span{{display:block}}
.prog{{flex:1;height:5px;background:#e6ebf3;border-radius:3px;cursor:pointer;position:relative;min-width:50px}}
.prog-fill{{position:absolute;left:0;top:0;bottom:0;width:0%;background:#2c5fae;border-radius:3px;transition:width .1s linear}}
.time{{font-size:12px;color:#8a97ad;font-variant-numeric:tabular-nums;white-space:nowrap}}

/* 正文 */
.card-body{{padding:16px 20px 18px;display:block}}
.card.collapsed .card-body{{display:none}}
.card-body p{{margin-bottom:10px;text-align:justify;font-size:15px;color:#34495e}}
.card-body p:last-child{{margin-bottom:0}}
.data-table{{width:100%;border-collapse:collapse;margin-top:12px;font-size:14px;border:1px solid #e3e8f0;border-radius:10px;overflow:hidden}}
.data-table th{{background:#2c5fae;color:#fff;padding:9px 12px;text-align:left;font-weight:600;white-space:nowrap}}
.data-table td{{padding:8px 12px;border-bottom:1px solid #eef1f6;color:#34495e}}
.data-table tr:last-child td{{border-bottom:none}}
.data-table td[rowspan]{{background:#f7f9fc;font-weight:600;color:#1a2b4a}}

/* 脚注 */
.page-foot{{text-align:center;font-size:12px;color:#9aa8bc;margin-top:18px}}

/* 移动端 */
@media(max-width:640px){{
  .card-head{{flex-wrap:wrap}}
  .player{{max-width:100%;width:100%;order:3;padding-top:8px;border-top:1px dashed #eef1f6}}
  .title-text{{font-size:15px}}
  .page-head h1{{font-size:19px}}
}}
</style>
</head>
<body>
<div class="container">
  <header class="page-head">
    <h1>📄 论信息系统服务设计实现</h1>
    <div class="sub">分段男声配音 · 云扬男声（+10%语速） · 共 {len(segs)} 段 · 点击 ▶ 播放，点箭头或标题展开/收起</div>
    <div class="toolbar">
      <button onclick="expandAll()">⤵ 全部展开</button>
      <button onclick="collapseAll()">⤴ 全部收起</button>
      <span class="hint">每段卡片内：箭头按钮 = 展开/收起，▶ = 播放配音</span>
    </div>
  </header>
{''.join(cards)}
  <footer class="page-foot">依据《论文-论信息系统服务设计实现.md》生成 · 点击"全部展开"可整篇通读，逐段播放可跟读背诵</footer>
</div>

<script>
const audios = {{}};
let currentAudio = null;
let currentBtn = null;

function initAudio(){{
  document.querySelectorAll('.player').forEach(p => {{
    const src = p.dataset.audio;
    const a = new Audio(src);
    a.preload = 'metadata';
    a.addEventListener('loadedmetadata', () => {{
      const t = p.querySelector('.time');
      t.textContent = '0:00 / ' + fmt(a.duration);
    }});
    a.addEventListener('timeupdate', () => {{
      p.querySelector('.prog-fill').style.width = (a.currentTime/a.duration*100) + '%';
      const t = p.querySelector('.time');
      t.textContent = fmt(a.currentTime) + ' / ' + fmt(a.duration);
    }});
    a.addEventListener('ended', () => {{
      const btn = p.querySelector('.play-btn');
      btn.classList.remove('playing');
      btn.textContent = '▶';
      p.querySelector('.prog-fill').style.width = '0%';
      if(currentAudio === a){{ currentAudio = null; currentBtn = null; }}
    }});
    audios[src] = a;
  }});
}}

function togglePlay(btn){{
  const p = btn.closest('.player');
  const src = p.dataset.audio;
  const a = audios[src];
  if(!a) return;
  if(currentAudio && currentAudio !== a){{
    currentAudio.pause();
    if(currentBtn){{
      currentBtn.classList.remove('playing');
      currentBtn.textContent = '▶';
    }}
  }}
  if(a.paused){{
    a.play();
    btn.classList.add('playing');
    btn.textContent = '';
    currentAudio = a;
    currentBtn = btn;
  }}else{{
    a.pause();
    btn.classList.remove('playing');
    btn.textContent = '▶';
    if(currentAudio === a){{ currentAudio = null; currentBtn = null; }}
  }}
}}

function seek(e){{
  const prog = e.currentTarget;
  const a = audios[prog.closest('.player').dataset.audio];
  if(!a || !a.duration) return;
  const rect = prog.getBoundingClientRect();
  const pct = Math.max(0, Math.min(1, (e.clientX-rect.left)/rect.width));
  a.currentTime = pct * a.duration;
}}

function fmt(s){{
  s = Math.floor(s || 0);
  const m = Math.floor(s/60);
  const r = s%60;
  return m + ':' + String(r).padStart(2,'0');
}}

function toggleCard(n){{
  const card = document.querySelector('.card[data-idx="'+n+'"]');
  if(!card) return;
  const collapsed = card.classList.toggle('collapsed');
  const btn = card.querySelector('.toggle');
  btn.setAttribute('aria-expanded', String(!collapsed));
}}

function expandAll(){{
  document.querySelectorAll('.card').forEach(c => c.classList.remove('collapsed'));
  document.querySelectorAll('.toggle').forEach(b => b.setAttribute('aria-expanded','true'));
}}
function collapseAll(){{
  document.querySelectorAll('.card').forEach(c => c.classList.add('collapsed'));
  document.querySelectorAll('.toggle').forEach(b => b.setAttribute('aria-expanded','false'));
}}

initAudio();
</script>
</body>
</html>"""


def main():
    print(f"输出目录: {BASE_DIR}")
    for i, seg in enumerate(SEGMENTS, 1):
        fname = f"{i:02d}-{seg['title'].split('·')[0].strip()}"
        mp3 = os.path.join(AUDIO_DIR, fname + ".mp3")
        txt = spoken_text(seg)
        print(f"[{i:02d}/{len(SEGMENTS):02d}] 生成 {fname}.mp3 ({len(txt)}字)")
        if not gen_mp3(txt, mp3):
            print(f"  !! 失败: {fname}")
            sys.exit(1)
        print(f"  OK 大小 {os.path.getsize(mp3)} B")

    html = build_html()
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html 已生成")


if __name__ == "__main__":
    main()
