<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface Card {
  id: number
  tag: string
  question: string
  answer: string
}

const cards: Card[] = [
  {
    id: 1,
    tag: '必须掌握',
    question: '信息系统规划的定义是什么？由谁负责、用什么方法、输出什么？',
    answer: '<p>组织<strong>决策层</strong>任主要负责人，<strong>管理层</strong>为工作主体，使用<strong>自顶向下分解</strong> / <strong>自底向上聚合</strong>，确定信息系统的整体<strong>发展战略</strong>、<strong>总体框架</strong>、<strong>演进路径</strong>和<strong>资源分配策略</strong>。</p>'
  },
  {
    id: 2,
    tag: '必须掌握',
    question: '信息系统规划的六大原则是什么？请说出记忆口诀。',
    answer: '<p>口诀：<strong>战整先指柔遵</strong></p><ul><li><strong>战略性</strong>：与组织战略保持一致，驱动引领组织建设</li><li><strong>整体性</strong>：业务赋能、系统框架、建设实施、集成融合四个方面</li><li><strong>先进性</strong>：考虑技术趋势，融合内外部最佳实践</li><li><strong>指导性</strong>：从业务需求、技术方案、实施管理、成本控制等方面给出框架性要求</li><li><strong>柔性</strong>：满足对内外部环境变化的适应性</li><li><strong>遵从性</strong>：法律法规、标准规范、组织战略与数字能力发展需求</li></ul>'
  },
  {
    id: 3,
    tag: '必须掌握',
    question: '信息系统规划七大体系有哪些？请说出记忆口诀。',
    answer: '<p>口诀：<strong>发框组技任资保</strong></p><ul><li><strong>发展战略</strong>（发）：目标树 / 5级成熟度 / 发展路径</li><li><strong>系统框架</strong>（框）：应用功能→平台能力→互联网主线</li><li><strong>组织体系</strong>（组）：中小型 / 集中式 / 分权式 / 平衡矩阵</li><li><strong>技术体系</strong>（技）：6原则 / 技术蓝图两种图</li><li><strong>任务体系</strong>（任）：拆解→目标→组织→策略→计划→监控</li><li><strong>资源体系</strong>（资）：识别评估→关系控制→分配调度→风险优化</li><li><strong>保障体系</strong>（保）：组织 / 人员 / 技术 / 资源 / 数据 / 安全</li></ul>'
  },
  {
    id: 4,
    tag: '高频考点',
    question: '五个发展阶段（成熟度5级）分别是什么？请说出记忆口诀和每级核心。',
    answer: '<p>口诀：<strong>打提做强构</strong></p><ul><li><strong>一级·打基础</strong>：业务规范化、数字化意识、局部系统建设</li><li><strong>二级·提效率</strong>：团队/部门职能、工作效率、全面推进系统建设</li><li><strong>三级·做协同</strong>：数据共治共享、数据流优化业务流、多元协同</li><li><strong>四级·强决策</strong>：数据模型开发利用、决策效率效能、治理模式变革</li><li><strong>五级·构生态</strong>：跨组织融合、云和互联网模式、广域协同</li></ul>'
  },
  {
    id: 5,
    tag: '高频考点',
    question: '三种框架演进路径的适用阶段和核心理念分别是什么？',
    answer: '<ul><li><strong>以应用功能为主线</strong>：适用中小型/信息化初期，"拿来主义"、成套软件、按部门职能建设，局限是系统间集成困难</li><li><strong>以平台能力为主线</strong>：适用规模扩大/个性化需求，平层化建设、数据共享、双态IT（稳态+敏态），局限是无法包容生态伙伴差异</li><li><strong>以互联网为主线</strong>：适用产业链/生态链阶段，App化微服务、能力封装、成熟度差异适配，局限是技术复杂度高</li></ul>'
  },
  {
    id: 6,
    tag: '高频考点',
    question: '四种组织体系模式及其适用对象是什么？',
    answer: '<ul><li><strong>中小型</strong>：中小企业，信息化管理委员会 + 信息化团队</li><li><strong>集中式</strong>：大型单位，专业信息部门、最高管理者第一责任人、专职架构/质量/测试人员</li><li><strong>分权式</strong>：业务单元差异大，各业务单元自行建设、设统筹负责人或虚拟团队</li><li><strong>平衡矩阵式</strong>：成熟度较高，稳态集中建设 + 敏态分权管理，业务侧重数据开发</li></ul>'
  },
  {
    id: 7,
    tag: '高频考点',
    question: '技术体系定义的六大原则是什么？请说出记忆口诀。',
    answer: '<p>口诀：<strong>用安靠灵扩驾</strong></p><ul><li><strong>可用性</strong>：不是二元（行/不行），是可用程度的问题，需多维度排序</li><li><strong>安全性</strong>：安全漏洞认知 + 故障影响最小 + 与信息安全管理体系匹配</li><li><strong>可靠性</strong>：三方面考察——成熟性、技术整体性、技术风险性</li><li><strong>灵活性</strong>：技术组件化 + 技术组合架构，少量变化满足新需求</li><li><strong>可扩展性</strong>：韧性拓展，适应更多用户/业务/数据/交互</li><li><strong>可驾驭性</strong>：直接/间接/混合方式，确保充分掌控关键技术</li></ul>'
  },
  {
    id: 8,
    tag: '高频考点',
    question: '任务体系部署的六步过程是什么？口诀和三层目标原则？',
    answer: '<p>口诀：<strong>任明匹制定监</strong></p><p>六步：<strong>任务拆解</strong> → <strong>明确目标</strong> → <strong>匹配组织</strong> → <strong>制定策略</strong> → <strong>定义计划</strong> → <strong>监控实施</strong></p><p>三层目标原则：<strong>S</strong>pecific 具体 + <strong>M</strong>easurable 可测量 + <strong>A</strong>chievable 可实现</p>'
  },
  {
    id: 9,
    tag: '高频考点',
    question: '资源体系调度的四步过程是什么？资源识别可基于哪些要素？',
    answer: '<p>口诀：<strong>识关分风</strong></p><p>四步：<strong>资源识别与评估</strong> → <strong>资源关系与控制</strong> → <strong>资源分配与调度</strong> → <strong>资源风险与优化</strong></p><p>资源识别：可基于能力要素（人员/技术/流程/软硬件），也可基于「人机料法环测」六要素。</p>'
  },
  {
    id: 10,
    tag: '高频考点',
    question: '保障体系设定的六个方面分别是什么？',
    answer: '<ul><li><strong>组织</strong>：决策层承诺、组织变革支持、思想认识一致性</li><li><strong>人员</strong>：全员数字能力培养、变革接受预期、碎片化时间利用</li><li><strong>技术</strong>：储备预研、微创新鼓励、标准化驱动</li><li><strong>资源</strong>：软实力建设、云服务获取硬资源、优先级提升</li><li><strong>数据</strong>：数据治理能力、数据质量、数据标准化、数据开发</li><li><strong>安全</strong>：安全意识、安全知识技能、安全管理体系</li></ul>'
  },
  {
    id: 11,
    tag: '五星重要',
    question: '信息系统规划工作要点（五步法）是什么？请说出记忆口诀。',
    answer: '<p>口诀：<strong>内场深整持</strong></p><p>五步递进：<strong>内外部需求挖掘</strong> → <strong>场景化模型分析</strong> → <strong>深度诊断与评估</strong> → <strong>整体与专项规划</strong> → <strong>持续改进</strong></p><p>⚠️ 5个工作要点构成一个完整闭环，是案例题的高频考点。</p>'
  },
  {
    id: 12,
    tag: '高频考点',
    question: '内部需求挖掘的五项任务和五项注意事项分别是什么？',
    answer: '<p>五项任务（口诀：<strong>理熟收评感</strong>）：理解组织战略 / 熟悉业务流程 / 收集用户需求 / 评估现有系统 / 感知数字环境</p><p>五项注意事项（口诀：<strong>原避培谨隐</strong>）：以原始信息获取为主 / 避免直接给出解决方案 / 及时开展引导性培训 / 谨慎信息交叉传递 / 关注隐性需求的推演</p>'
  },
  {
    id: 13,
    tag: '高频考点',
    question: '外部需求挖掘的六项任务和三项注意事项分别是什么？',
    answer: '<p>六项任务（口诀：<strong>国行技竞客标</strong>）：国家战略导入 / 行业趋势分析 / 技术趋势研究 / 竞争环境分析 / 客户期望调研 / 标准与规范引用</p><p>三项注意事项（口诀：<strong>国定避</strong>）：国家战略与政策引用 / 定性内容转定量对比 / 避免信息安全事件</p>'
  },
  {
    id: 14,
    tag: '高频考点',
    question: '场景化模型分析的八维度是什么？请说出记忆口诀。',
    answer: '<p>口诀：<strong>场角业数技组风政</strong></p><ul><li><strong>场景</strong>定义：目标、范围、业务背景、利益相关者</li><li><strong>角色</strong>分析：职责、需求、行为、作用与影响</li><li><strong>业务</strong>分析：业务模式、流程、需求、发展</li><li><strong>数据</strong>分析：数据流、数据来源/类型/结构、开发利用价值</li><li><strong>技术</strong>分析：管理/工艺/决策/信息技术现状与发展</li><li><strong>组织</strong>分析：组织文化、人员技能、组织流程</li><li><strong>风险</strong>分析：技术/安全/管理风险与应对策略</li><li><strong>政策与法律</strong>分析：合规性分析</li></ul>'
  },
  {
    id: 15,
    tag: '高频考点',
    question: '深度诊断与评估的核心工具是什么？诊断评估实施有哪三步？',
    answer: '<p>核心工具：<strong>成熟度模型（5级）</strong></p><p>相关国标：GB/T 43439（数字转型成熟度）、GB/T 39116（智能制造成熟度）</p><p>诊断评估实施三步：</p><ol><li><strong>计划与打分</strong>：0分/0.5分/0.8分/1分四级打分，由低到高逐级</li><li><strong>权重与计算</strong>：参考标准或自动设定</li><li><strong>记录与确认</strong>：形成底稿，标注不满足项，获得干系人确认</li></ol><p>木桶原理：组织整体能力水平 = 最短板的能力水平状态</p>'
  },
  {
    id: 16,
    tag: '五星重要',
    question: '五种规划方法的名字、提出者、年份、核心思想分别是什么？请说出记忆口诀。',
    answer: '<p>口诀：<strong>战企关价扎</strong></p><ul><li><strong>SST</strong> 战略目标集转移：William King · 1978，组织战略集→信息系统战略集的转换</li><li><strong>BSP</strong> 企业系统规划：IBM · 1970s，自顶向下分析需求，自底向上设计结构</li><li><strong>CSF</strong> 关键成功因素：Zani/Rockart · 1970，少数关键成功因素决定信息需求</li><li><strong>VCA</strong> 价值链分析：Porter · 1985，价值链上识别战略环节优先部署IT</li><li><strong>Zachman</strong> 框架：John Zachman · 1987，6W×6层 = 36格的企业架构分类</li></ul>'
  },
  {
    id: 17,
    tag: '高频考点',
    question: 'BSP企业系统规划法的四个基本步骤是什么？核心理念是什么？',
    answer: '<p>口诀：<strong>目功数构</strong></p><ol><li><strong>定义管理目标</strong>：采访各级管理层，绘制目标树</li><li><strong>定义管理功能</strong>：基于资源的生命周期识别（产生/获得/服务/归宿）</li><li><strong>定义数据类</strong>：实体法 + 功能法，归纳10~20个数据类</li><li><strong>定义信息结构</strong>：功能/数据类矩阵→C-U矩阵→聚类分组→子系统划分</li></ol><p>核心理念：<strong>管理功能应独立于组织机构</strong>（组织变动不影响系统设计）</p>'
  },
  {
    id: 18,
    tag: '高频考点',
    question: 'CSF关键成功因素法的四个主要来源和四类CSF分别是什么？',
    answer: '<p>四个主要来源（口诀：<strong>产竞环暂</strong>）：①个别产业结构 ②竞争策略与产业地位 ③环境因素 ④暂时因素</p><p>四类CSF：<strong>内部型</strong> / <strong>外部型</strong> / <strong>监控型</strong> / <strong>建立型</strong></p><p>四步实施：①确定战略目标 → ②识别所有成功因素 → ③确定关键成功因素 → ④识别绩效指标</p>'
  },
  {
    id: 19,
    tag: '高频考点',
    question: 'VCA价值链分析法的四个基本观点和四步应用分别是什么？',
    answer: '<p>四个基本观点：</p><ul><li>价值核心</li><li>基本活动 + 支持活动</li><li>相互依存</li><li>竞争优势来自优化</li></ul><p>四步应用：①识别价值链 → ②确定关键价值<strong>增加</strong>环节 → ③确定关键价值<strong>减少</strong>环节 → ④明确IT支持</p>'
  },
  {
    id: 20,
    tag: '高频考点',
    question: 'Zachman框架的结构是什么？横向6W和纵向6层分别对应什么？',
    answer: '<p>结构：<strong>6行（纵向）× 6列（横向）= 36格</strong></p><p>横向<strong>6W</strong>：What（数据）/ How（功能）/ Where（网络）/ Who（人员）/ When（时间）/ Why（动机）</p><p>纵向<strong>6层</strong>：范围模型 → 企业模型 → 系统模型 → 技术模型 → 详细模型 → 功能模型</p>'
  },
]

const currentIndex = ref(0)
const revealed = ref(false)
const direction = ref(0) // -1 left, 1 right

const currentCard = computed(() => cards[currentIndex.value])
const progressText = computed(() => `第 ${currentIndex.value + 1} / ${cards.length} 题`)

function nextCard() {
  if (currentIndex.value < cards.length - 1) {
    direction.value = 1
    revealed.value = false
    currentIndex.value++
  }
}

function prevCard() {
  if (currentIndex.value > 0) {
    direction.value = -1
    revealed.value = false
    currentIndex.value--
  }
}

// Swipe handling
const deckRef = ref<HTMLElement | null>(null)
let startX = 0
let currentX = 0
let isDragging = false

const SWIPE_THRESHOLD = 80

function onTouchStart(e: TouchEvent) {
  startX = e.touches[0].clientX
  currentX = startX
  isDragging = true
}

function onTouchMove(e: TouchEvent) {
  if (!isDragging) return
  currentX = e.touches[0].clientX
  const delta = currentX - startX
  if (deckRef.value) {
    const card = deckRef.value.querySelector('.flashcard.is-current') as HTMLElement
    if (card) {
      card.style.transform = `translateX(${delta}px) rotate(${delta * 0.03}deg)`
    }
  }
}

function onTouchEnd() {
  if (!isDragging) return
  isDragging = false
  const delta = currentX - startX
  if (deckRef.value) {
    const card = deckRef.value.querySelector('.flashcard.is-current') as HTMLElement
    if (card) {
      card.style.transition = 'transform 0.3s ease'
      if (delta < -SWIPE_THRESHOLD && currentIndex.value < cards.length - 1) {
        card.style.transform = 'translateX(-120%) rotate(-8deg)'
        setTimeout(() => {
          nextCard()
          card.style.transition = 'none'
          card.style.transform = ''
          setTimeout(() => { card.style.transition = '' }, 50)
        }, 200)
        return
      } else if (delta > SWIPE_THRESHOLD && currentIndex.value > 0) {
        card.style.transform = 'translateX(120%) rotate(8deg)'
        setTimeout(() => {
          prevCard()
          card.style.transition = 'none'
          card.style.transform = ''
          setTimeout(() => { card.style.transition = '' }, 50)
        }, 200)
        return
      }
      card.style.transform = ''
      setTimeout(() => { card.style.transition = '' }, 300)
    }
  }
}

// Mouse drag support
function onMouseDown(e: MouseEvent) {
  startX = e.clientX
  currentX = startX
  isDragging = true
  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
}

function onMouseMove(e: MouseEvent) {
  if (!isDragging) return
  currentX = e.clientX
  const delta = currentX - startX
  if (deckRef.value) {
    const card = deckRef.value.querySelector('.flashcard.is-current') as HTMLElement
    if (card) {
      card.style.transform = `translateX(${delta}px) rotate(${delta * 0.03}deg)`
    }
  }
}

function onMouseUp() {
  document.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseup', onMouseUp)
  if (!isDragging) return
  isDragging = false
  const delta = currentX - startX
  if (deckRef.value) {
    const card = deckRef.value.querySelector('.flashcard.is-current') as HTMLElement
    if (card) {
      card.style.transition = 'transform 0.3s ease'
      if (delta < -SWIPE_THRESHOLD && currentIndex.value < cards.length - 1) {
        card.style.transform = 'translateX(-120%) rotate(-8deg)'
        setTimeout(() => {
          nextCard()
          card.style.transition = 'none'
          card.style.transform = ''
          setTimeout(() => { card.style.transition = '' }, 50)
        }, 200)
        return
      } else if (delta > SWIPE_THRESHOLD && currentIndex.value > 0) {
        card.style.transform = 'translateX(120%) rotate(8deg)'
        setTimeout(() => {
          prevCard()
          card.style.transition = 'none'
          card.style.transform = ''
          setTimeout(() => { card.style.transition = '' }, 50)
        }, 200)
        return
      }
      card.style.transform = ''
      setTimeout(() => { card.style.transition = '' }, 300)
    }
  }
}

// Keyboard navigation
function onKeyDown(e: KeyboardEvent) {
  if (e.key === 'ArrowRight' || e.key === ' ') {
    e.preventDefault()
    if (revealed.value) {
      nextCard()
    } else {
      revealed.value = true
    }
  } else if (e.key === 'ArrowLeft') {
    e.preventDefault()
    prevCard()
  }
}

onMounted(() => {
  window.addEventListener('keydown', onKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeyDown)
})
</script>

<template>
  <div class="flashcards-container">
    <div class="flashcards-header">
      <span class="flashcards-title">🎯 第4章 学习卡片</span>
      <span class="flashcards-progress">{{ progressText }}</span>
    </div>

    <div class="flashcards-deck" ref="deckRef"
         @touchstart.passive="onTouchStart"
         @touchmove.passive="onTouchMove"
         @touchend="onTouchEnd"
         @mousedown="onMouseDown">

      <div class="flashcard is-current">
        <div class="flashcard-inner">
          <div class="flashcard-tag">{{ currentCard.tag }}</div>

          <div class="flashcard-question">{{ currentCard.question }}</div>

          <div class="flashcard-answer-wrapper" :class="{ 'is-revealed': revealed }">
            <button class="flashcard-reveal-btn" @click="revealed = true" v-if="!revealed">
              <span class="reveal-icon">💡</span>
              <span>显示答案</span>
            </button>
            <div class="flashcard-answer" v-else>
              <div class="flashcard-answer-title">答案</div>
              <div class="flashcard-answer-content" v-html="currentCard.answer"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="flashcards-hint">
      <span>← 左右滑动切换 →</span>
      <span>或按空格/方向键</span>
    </div>

    <div class="flashcards-dots">
      <span
        v-for="(_, i) in cards"
        :key="i"
        class="dot"
        :class="{ active: i === currentIndex }"
        @click="currentIndex = i; revealed = false"
      />
    </div>

    <div class="flashcards-controls">
      <button class="ctrl-btn" @click="prevCard" :disabled="currentIndex === 0">
        ◀ 上一题
      </button>
      <button class="ctrl-btn primary" @click="revealed = !revealed">
        {{ revealed ? '隐藏答案' : '显示答案' }}
      </button>
      <button class="ctrl-btn" @click="nextCard" :disabled="currentIndex === cards.length - 1">
        下一题 ▶
      </button>
    </div>
  </div>
</template>

<style scoped>
.flashcards-container {
  --fc-bg: var(--vp-c-bg);
  --fc-card-bg: var(--vp-c-bg-soft, #ffffff);
  --fc-border: var(--vp-c-divider, #e2e8f0);
  --fc-text: var(--vp-c-text-1, #1e293b);
  --fc-text-2: var(--vp-c-text-2, #64748b);
  --fc-brand: var(--vp-c-brand-1, #3b82f6);
  --fc-brand-soft: var(--vp-c-brand-soft, #eff6ff);
  --fc-tag-bg: #fef2f2;
  --fc-tag-text: #dc2626;
  --fc-answer-bg: #f0f7ff;
  --fc-radius: 16px;

  max-width: 680px;
  margin: 0 auto;
  padding: 16px 8px;
  user-select: none;
}

.flashcards-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 4px;
}

.flashcards-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--fc-text);
}

.flashcards-progress {
  font-size: 13px;
  color: var(--fc-text-2);
  background: var(--fc-card-bg);
  border: 1px solid var(--fc-border);
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 500;
}

.flashcards-deck {
  position: relative;
  min-height: 420px;
  touch-action: pan-y;
}

.flashcard {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  will-change: transform;
}

.flashcard-inner {
  background: var(--fc-card-bg);
  border: 1px solid var(--fc-border);
  border-radius: var(--fc-radius);
  padding: 24px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  min-height: 380px;
  display: flex;
  flex-direction: column;
}

.flashcard-tag {
  display: inline-block;
  align-self: flex-start;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 8px;
  background: var(--fc-tag-bg);
  color: var(--fc-tag-text);
  margin-bottom: 16px;
}

.flashcard-question {
  font-size: 17px;
  font-weight: 600;
  line-height: 1.7;
  color: var(--fc-text);
  margin-bottom: 20px;
  flex-shrink: 0;
}

.flashcard-answer-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 120px;
}

.flashcard-reveal-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  max-width: 200px;
  margin: 0 auto;
  padding: 14px 24px;
  font-size: 15px;
  font-weight: 600;
  color: var(--fc-brand);
  background: var(--fc-brand-soft);
  border: 1.5px solid var(--fc-brand);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.flashcard-reveal-btn:hover {
  background: var(--fc-brand);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.reveal-icon {
  font-size: 18px;
}

.flashcard-answer {
  background: var(--fc-answer-bg);
  border-radius: 12px;
  padding: 16px 20px;
  animation: fadeSlideDown 0.3s ease;
}

@keyframes fadeSlideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.flashcard-answer-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--fc-brand);
  margin-bottom: 10px;
}

.flashcard-answer-content {
  font-size: 14px;
  line-height: 1.8;
  color: var(--fc-text);
}

.flashcard-answer-content :deep(ul),
.flashcard-answer-content :deep(ol) {
  margin: 8px 0;
  padding-left: 20px;
}

.flashcard-answer-content :deep(li) {
  margin: 4px 0;
}

.flashcard-answer-content :deep(strong) {
  color: var(--fc-text);
  font-weight: 600;
}

.flashcard-answer-content :deep(p) {
  margin: 8px 0;
}

.flashcards-hint {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding: 0 4px;
  font-size: 12px;
  color: var(--fc-text-2);
}

.flashcards-dots {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  margin-top: 16px;
  flex-wrap: wrap;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--fc-border);
  cursor: pointer;
  transition: all 0.2s ease;
}

.dot:hover {
  background: var(--fc-text-2);
}

.dot.active {
  background: var(--fc-brand);
  width: 20px;
  border-radius: 4px;
}

.flashcards-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.ctrl-btn {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  border-radius: 10px;
  border: 1px solid var(--fc-border);
  background: var(--fc-card-bg);
  color: var(--fc-text);
  cursor: pointer;
  transition: all 0.2s ease;
}

.ctrl-btn:hover:not(:disabled) {
  border-color: var(--fc-brand);
  color: var(--fc-brand);
}

.ctrl-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.ctrl-btn.primary {
  background: var(--fc-brand);
  color: #fff;
  border-color: var(--fc-brand);
}

.ctrl-btn.primary:hover {
  background: #2563eb;
  border-color: #2563eb;
}

/* Mobile adjustments */
@media (max-width: 480px) {
  .flashcards-container {
    padding: 12px 4px;
  }

  .flashcard-inner {
    padding: 18px;
    min-height: 340px;
  }

  .flashcard-question {
    font-size: 15px;
  }

  .flashcard-answer-content {
    font-size: 13px;
  }

  .flashcards-controls {
    gap: 8px;
  }

  .ctrl-btn {
    padding: 8px 14px;
    font-size: 13px;
  }

  .flashcards-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
