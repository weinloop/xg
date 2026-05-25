import DefaultTheme from 'vitepress/theme'
import { inBrowser } from 'vitepress'
import './style.css'

export default {
  extends: DefaultTheme,
  enhanceApp() {
    if (inBrowser) {
      initSidebarToggles()
    }
  }
}

function initSidebarToggles() {
  const KEY_LEFT = 'vp-sidebar-collapsed'
  const KEY_RIGHT = 'vp-aside-collapsed'

  function applyState() {
    const left = localStorage.getItem(KEY_LEFT) === 'true'
    const right = localStorage.getItem(KEY_RIGHT) === 'true'
    document.documentElement.classList.toggle('sidebar-left-collapsed', left)
    document.documentElement.classList.toggle('sidebar-right-collapsed', right)
    updateIcons()
  }

  function updateIcons() {
    const leftBtn = document.getElementById('toggle-btn-left')
    const rightBtn = document.getElementById('toggle-btn-right')
    const leftCollapsed = document.documentElement.classList.contains('sidebar-left-collapsed')
    const rightCollapsed = document.documentElement.classList.contains('sidebar-right-collapsed')

    if (leftBtn) leftBtn.innerHTML = leftCollapsed ? '&#9654;' : '&#9664;'
    if (rightBtn) rightBtn.innerHTML = rightCollapsed ? '&#9664;' : '&#9654;'
  }

  function createButton(position: 'left' | 'right') {
    const btn = document.createElement('button')
    btn.id = `toggle-btn-${position}`
    btn.className = `sidebar-toggle-btn sidebar-toggle-${position}`
    btn.setAttribute('aria-label', position === 'left' ? '切换侧边栏' : '切换目录')
    btn.title = position === 'left' ? '收起 / 展开侧边栏' : '收起 / 展开本页目录'

    btn.addEventListener('click', () => {
      const key = position === 'left' ? KEY_LEFT : KEY_RIGHT
      const cls = position === 'left' ? 'sidebar-left-collapsed' : 'sidebar-right-collapsed'
      const collapsed = document.documentElement.classList.toggle(cls)
      localStorage.setItem(key, String(collapsed))
      updateIcons()
    })

    document.body.appendChild(btn)
  }

  applyState()
  createButton('left')
  createButton('right')
}
