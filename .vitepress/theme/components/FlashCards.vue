<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { chapters } from './cardsData'

const props = withDefaults(defineProps<{ chapter: string }>(), {
  chapter: 'ch04'
})

const cards = computed(() => {
  const data = chapters[props.chapter]
  return data ? data.cards : []
})
const title = computed(() => {
  const data = chapters[props.chapter]
  return data ? data.title : '学习卡片'
})

const currentIndex = ref(0)
const revealed = ref(false)

const tagStyleMap: Record<string, { bg: string; color: string }> = {
  '否定辨析': { bg: '#fef2f2', color: '#dc2626' },
  '特征归因': { bg: '#eff6ff', color: '#2563eb' },
  '排序分级': { bg: '#f5f3ff', color: '#7c3aed' },
  '场景匹配': { bg: '#ecfdf5', color: '#059669' },
  '方法匹配': { bg: '#fffbeb', color: '#d97706' },
  '内容产出物': { bg: '#fdf2f8', color: '#db2777' },
  '步骤默写': { bg: '#f0f9ff', color: '#0284c7' },
  '计算应用': { bg: '#fefce8', color: '#ca8a04' },
  '综合辨析': { bg: '#faf5ff', color: '#9333ea' },
  '必须掌握': { bg: '#fef2f2', color: '#dc2626' },
  '高频考点': { bg: '#eff6ff', color: '#2563eb' },
  '五星重要': { bg: '#fffbeb', color: '#d97706' },
}

const currentCard = computed(() => cards.value[currentIndex.value])
const progressText = computed(() => `第 ${currentIndex.value + 1} / ${cards.value.length} 题`)

const tagStyle = computed(() => {
  const tag = currentCard.value?.tag || ''
  return tagStyleMap[tag] || { bg: '#f1f5f9', color: '#475569' }
})

function nextCard() {
  if (currentIndex.value < cards.value.length - 1) {
    revealed.value = false
    currentIndex.value++
  }
}

function prevCard() {
  if (currentIndex.value > 0) {
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

function onSwipeEnd(delta: number) {
  if (deckRef.value) {
    const card = deckRef.value.querySelector('.flashcard.is-current') as HTMLElement
    if (!card) return
    card.style.transition = 'transform 0.3s ease'
    if (delta < -SWIPE_THRESHOLD && currentIndex.value < cards.value.length - 1) {
      card.style.transform = 'translateX(-120%) rotate(-8deg)'
      setTimeout(() => {
        nextCard()
        card.style.transition = 'none'
        card.style.transform = ''
        setTimeout(() => { card.style.transition = '' }, 50)
      }, 200)
    } else if (delta > SWIPE_THRESHOLD && currentIndex.value > 0) {
      card.style.transform = 'translateX(120%) rotate(8deg)'
      setTimeout(() => {
        prevCard()
        card.style.transition = 'none'
        card.style.transform = ''
        setTimeout(() => { card.style.transition = '' }, 50)
      }, 200)
    } else {
      card.style.transform = ''
      setTimeout(() => { card.style.transition = '' }, 300)
    }
  }
}

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
    if (card) card.style.transform = `translateX(${delta}px) rotate(${delta * 0.03}deg)`
  }
}

function onTouchEnd() {
  if (!isDragging) return
  isDragging = false
  onSwipeEnd(currentX - startX)
}

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
    if (card) card.style.transform = `translateX(${delta}px) rotate(${delta * 0.03}deg)`
  }
}

function onMouseUp() {
  document.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseup', onMouseUp)
  if (!isDragging) return
  isDragging = false
  onSwipeEnd(currentX - startX)
}

function onKeyDown(e: KeyboardEvent) {
  if (e.key === 'ArrowRight' || e.key === ' ') {
    e.preventDefault()
    if (revealed.value) nextCard()
    else revealed.value = true
  } else if (e.key === 'ArrowLeft') {
    e.preventDefault()
    prevCard()
  }
}

onMounted(() => window.addEventListener('keydown', onKeyDown))
onUnmounted(() => window.removeEventListener('keydown', onKeyDown))
</script>

<template>
  <div class="flashcards-container">
    <div class="flashcards-header">
      <span class="flashcards-title">🎯 {{ title }} 学习卡片</span>
      <span class="flashcards-progress">{{ progressText }}</span>
    </div>

    <div class="flashcards-deck" ref="deckRef"
         @touchstart.passive="onTouchStart"
         @touchmove.passive="onTouchMove"
         @touchend="onTouchEnd"
         @mousedown="onMouseDown">

      <div class="flashcard is-current">
        <div class="flashcard-inner">
          <div class="flashcard-tag" :style="{ background: tagStyle.bg, color: tagStyle.color }">{{ currentCard?.tag }}</div>
          <div class="flashcard-question">{{ currentCard?.question }}</div>
          <div class="flashcard-answer-wrapper" :class="{ 'is-revealed': revealed }">
            <button class="flashcard-reveal-btn" @click="revealed = true" v-if="!revealed">
              <span class="reveal-icon">💡</span>
              <span>显示答案</span>
            </button>
            <div class="flashcard-answer" v-else>
              <div class="flashcard-answer-title">答案</div>
              <div class="flashcard-answer-content" v-html="currentCard?.answer"></div>
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
      <span v-for="(_, i) in cards" :key="i" class="dot"
            :class="{ active: i === currentIndex }"
            @click="currentIndex = i; revealed = false" />
    </div>

    <div class="flashcards-controls">
      <button class="ctrl-btn" @click="prevCard" :disabled="currentIndex === 0">◀ 上一题</button>
      <button class="ctrl-btn primary" @click="revealed = !revealed">{{ revealed ? '隐藏答案' : '显示答案' }}</button>
      <button class="ctrl-btn" @click="nextCard" :disabled="currentIndex === cards.length - 1">下一题 ▶</button>
    </div>
  </div>
</template>

<style scoped>
.flashcards-container {
  --fc-card-bg: var(--vp-c-bg-soft, #ffffff);
  --fc-border: var(--vp-c-divider, #e2e8f0);
  --fc-text: var(--vp-c-text-1, #1e293b);
  --fc-text-2: var(--vp-c-text-2, #64748b);
  --fc-brand: var(--vp-c-brand-1, #3b82f6);
  --fc-brand-soft: var(--vp-c-brand-soft, #eff6ff);
  --fc-answer-bg: #f0f7ff;
  --fc-radius: 16px;
  max-width: 680px;
  margin: 0 auto;
  padding: 16px 8px;
  user-select: none;
}
.flashcards-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding: 0 4px; }
.flashcards-title { font-size: 16px; font-weight: 700; color: var(--fc-text); }
.flashcards-progress { font-size: 13px; color: var(--fc-text-2); background: var(--fc-card-bg); border: 1px solid var(--fc-border); padding: 4px 12px; border-radius: 20px; font-weight: 500; }
.flashcards-deck { position: relative; min-height: 320px; touch-action: pan-y; }
.flashcard { position: absolute; top: 0; left: 0; right: 0; will-change: transform; }
.flashcard-inner { background: var(--fc-card-bg); border: 1px solid var(--fc-border); border-radius: var(--fc-radius); padding: 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); min-height: 300px; max-height: 600px; display: flex; flex-direction: column; overflow: hidden; }
.flashcard-tag { display: inline-block; align-self: flex-start; font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 8px; transition: background 0.2s, color 0.2s; margin-bottom: 12px; flex-shrink: 0; }
.flashcard-question { font-size: 17px; font-weight: 600; line-height: 1.7; color: var(--fc-text); margin-bottom: 16px; flex-shrink: 0; }
.flashcard-answer-wrapper { flex: 1; display: flex; flex-direction: column; justify-content: center; min-height: 80px; overflow: hidden; }
.flashcard-reveal-btn { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; max-width: 200px; margin: 0 auto; padding: 14px 24px; font-size: 15px; font-weight: 600; color: var(--fc-brand); background: var(--fc-brand-soft); border: 1.5px solid var(--fc-brand); border-radius: 12px; cursor: pointer; transition: all 0.2s ease; }
.flashcard-reveal-btn:hover { background: var(--fc-brand); color: #fff; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(59,130,246,0.25); }
.reveal-icon { font-size: 18px; }
.flashcard-answer { background: var(--fc-answer-bg); border-radius: 12px; padding: 14px 18px; animation: fadeSlideDown 0.3s ease; max-height: 100%; display: flex; flex-direction: column; overflow: hidden; }
@keyframes fadeSlideDown { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }
.flashcard-answer-title { font-size: 14px; font-weight: 700; color: var(--fc-brand); margin-bottom: 8px; flex-shrink: 0; }
.flashcard-answer-content { font-size: 14px; line-height: 1.8; color: var(--fc-text); overflow-y: auto; overflow-x: hidden; }
.flashcard-answer-content :deep(ul), .flashcard-answer-content :deep(ol) { margin: 6px 0; padding-left: 20px; }
.flashcard-answer-content :deep(li) { margin: 3px 0; }
.flashcard-answer-content :deep(strong) { color: var(--fc-text); font-weight: 600; }
.flashcard-answer-content :deep(p) { margin: 6px 0; }
/* Table containment */
.flashcard-answer-content :deep(table) { width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 13px; }
.flashcard-answer-content :deep(th), .flashcard-answer-content :deep(td) { border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }
.flashcard-answer-content :deep(th) { background: #e2e8f0; font-weight: 600; }
.flashcard-answer-content :deep(tr:nth-child(even)) { background: rgba(241,245,249,0.5); }
.flashcard-answer-content :deep(blockquote) { margin: 8px 0; padding: 8px 12px; border-left: 3px solid #f59e0b; background: #fffbeb; border-radius: 0 8px 8px 0; font-size: 13px; }
.flashcards-hint { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; padding: 0 4px; font-size: 12px; color: var(--fc-text-2); }
.flashcards-dots { display: flex; justify-content: center; align-items: center; gap: 6px; margin-top: 16px; flex-wrap: wrap; }
.dot { width: 7px; height: 7px; border-radius: 50%; background: var(--fc-border); cursor: pointer; transition: all 0.2s ease; }
.dot:hover { background: var(--fc-text-2); }
.dot.active { background: var(--fc-brand); width: 20px; border-radius: 4px; }
.flashcards-controls { display: flex; justify-content: center; align-items: center; gap: 12px; margin-top: 20px; }
.ctrl-btn { padding: 10px 20px; font-size: 14px; font-weight: 500; border-radius: 10px; border: 1px solid var(--fc-border); background: var(--fc-card-bg); color: var(--fc-text); cursor: pointer; transition: all 0.2s ease; }
.ctrl-btn:hover:not(:disabled) { border-color: var(--fc-brand); color: var(--fc-brand); }
.ctrl-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.ctrl-btn.primary { background: var(--fc-brand); color: #fff; border-color: var(--fc-brand); }
.ctrl-btn.primary:hover { background: #2563eb; border-color: #2563eb; }
@media (max-width: 480px) {
  .flashcards-container { padding: 12px 4px; }
  .flashcard-inner { padding: 16px; min-height: 260px; max-height: 520px; }
  .flashcard-question { font-size: 15px; margin-bottom: 12px; }
  .flashcard-answer-content { font-size: 13px; }
  .flashcard-answer { padding: 12px 14px; }
  .flashcard-tag { margin-bottom: 10px; }
  .flashcards-controls { gap: 8px; }
  .ctrl-btn { padding: 8px 14px; font-size: 13px; }
  .flashcards-header { flex-direction: column; align-items: flex-start; gap: 8px; }
  .flashcards-deck { min-height: 260px; }
}
</style>
