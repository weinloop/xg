import DefaultTheme from 'vitepress/theme'
import { inBrowser } from 'vitepress'
import './style.css'

const KEY_LEFT = 'vp-sidebar-collapsed'
const KEY_RIGHT = 'vp-aside-collapsed'

function applyState() {
  const left = localStorage.getItem(KEY_LEFT) === 'true'
  const right = localStorage.getItem(KEY_RIGHT) === 'true'
  document.documentElement.classList.toggle('sb-left-collapsed', left)
  document.documentElement.classList.toggle('sb-right-collapsed', right)
}

function updateIcons() {
  const left = document.documentElement.classList.contains('sb-left-collapsed')
  const right = document.documentElement.classList.contains('sb-right-collapsed')
  const lb = document.getElementById('sb-btn-left')
  const rb = document.getElementById('sb-btn-right')
  if (lb) lb.textContent = left ? '\u25B6' : '\u25C0'
  if (rb) rb.textContent = right ? '\u25C0' : '\u25B6'
}

function calcPositions() {
  const lb = document.getElementById('sb-btn-left')
  const rb = document.getElementById('sb-btn-right')
  if (!lb || !rb) return

  const sidebar = document.querySelector('aside.VPSidebar') as HTMLElement | null
  const aside = document.querySelector('aside.VPDocAsideOutline, div.VPDocAside, aside.VPDocAside') as HTMLElement | null
  const isLeftCollapsed = document.documentElement.classList.contains('sb-left-collapsed')
  const isRightCollapsed = document.documentElement.classList.contains('sb-right-collapsed')

  // Left button position
  if (isLeftCollapsed) {
    lb.style.left = '4px'
  } else if (sidebar) {
    const rect = sidebar.getBoundingClientRect()
    lb.style.left = rect.right - 10 + 'px'
  }

  // Right button position
  if (isRightCollapsed) {
    rb.style.right = '4px'
  } else if (aside) {
    const rect = aside.getBoundingClientRect()
    rb.style.right = (window.innerWidth - rect.left) - 10 + 'px'
  }
}

function injectButtons() {
  // Remove any stale duplicates
  document.querySelectorAll('.sb-toggle').forEach(el => el.remove())

  const lb = document.createElement('button')
  lb.id = 'sb-btn-left'
  lb.className = 'sb-toggle'
  lb.title = '收起 / 展开侧边栏'
  lb.addEventListener('click', () => {
    const collapsed = document.documentElement.classList.toggle('sb-left-collapsed')
    localStorage.setItem(KEY_LEFT, String(collapsed))
    updateIcons()
    calcPositions()
  })

  const rb = document.createElement('button')
  rb.id = 'sb-btn-right'
  rb.className = 'sb-toggle'
  rb.title = '收起 / 展开本页目录'
  rb.addEventListener('click', () => {
    const collapsed = document.documentElement.classList.toggle('sb-right-collapsed')
    localStorage.setItem(KEY_RIGHT, String(collapsed))
    updateIcons()
    calcPositions()
  })

  document.body.appendChild(lb)
  document.body.appendChild(rb)

  updateIcons()
  calcPositions()

  // Recalc on resize
  window.addEventListener('resize', calcPositions)
  // Recalc after scroll (VitePress may lazy-load sidebar)
  window.addEventListener('scroll', calcPositions, { passive: true })
}

export default {
  extends: DefaultTheme,
  enhanceApp({ router }) {
    if (!inBrowser) return
    applyState()

    const attempts = [100, 300, 500, 800, 1200, 2000]
    let injected = false

    const tryOnce = () => {
      const sidebar = document.querySelector('aside.VPSidebar')
      if (sidebar && !injected) {
        injected = true
        injectButtons()
        return true
      }
      return false
    }

    attempts.forEach(ms => {
      setTimeout(() => {
        if (!injected) {
          if (tryOnce()) return
          // fallback observer for last attempt
          if (ms === attempts[attempts.length - 1]) {
            const obs = new MutationObserver(() => {
              if (tryOnce()) obs.disconnect()
            })
            obs.observe(document.body, { childList: true, subtree: true })
            setTimeout(() => obs.disconnect(), 8000)
          }
        }
      }, ms)
    })

    if (router) {
      router.onAfterRouteChanged = () => {
        setTimeout(() => {
          calcPositions()
        }, 300)
      }
    }
  }
}
