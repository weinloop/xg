import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'XG',
  description: '系统规划与管理师考试知识体系与备考方案',
  lang: 'zh-CN',
  base: '/xg/',
  head: [['link', { rel: 'icon', type: 'image/svg+xml', href: '/xg/favicon.svg' }]],

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '知识体系', link: '/01-基础篇/ch01-信息系统与信息技术发展' },
      { text: '备考方案', link: '/附录/备考方案总览' },
      { text: '论文模板', link: '/附录/论文万能框架' },
    ],

    sidebar: {
      '/01-基础篇/': [
        {
          text: '📘 第一篇 基础篇',
          collapsed: false,
          items: [
            { text: '第1章 信息系统与信息技术发展', link: '/01-基础篇/ch01-信息系统与信息技术发展' },
            { text: '第2章 数字中国与数智化发展', link: '/01-基础篇/ch02-数字中国与数智化发展' },
            { text: '第3章 系统科学与哲学方法论', link: '/01-基础篇/ch03-系统科学与哲学方法论' },
          ]
        }
      ],
      '/02-方法篇/': [
        {
          text: '📙 第二篇 方法篇',
          collapsed: false,
          items: [
            { text: '第4章 信息系统规划 ✅', link: '/02-方法篇/ch04-信息系统规划' },
            { text: '第5章 应用系统规划', link: '/02-方法篇/ch05-应用系统规划' },
            { text: '第6章 云资源规划', link: '/02-方法篇/ch06-云资源规划' },
            { text: '第7章 网络环境规划', link: '/02-方法篇/ch07-网络环境规划' },
            { text: '第8章 数据资源规划', link: '/02-方法篇/ch08-数据资源规划' },
            { text: '第9章 信息安全规划', link: '/02-方法篇/ch09-信息安全规划' },
            { text: '第10章 云原生系统规划', link: '/02-方法篇/ch10-云原生系统规划' },
          ]
        }
      ],
      '/03-能力篇/': [
        {
          text: '📗 第三篇 能力篇',
          collapsed: false,
          items: [
            { text: '第11章 信息系统治理', link: '/03-能力篇/ch11-信息系统治理' },
            { text: '第12章 信息系统服务管理', link: '/03-能力篇/ch12-信息系统服务管理' },
            { text: '第13章 人员管理', link: '/03-能力篇/ch13-人员管理' },
            { text: '第14章 规范与过程管理', link: '/03-能力篇/ch14-规范与过程管理' },
            { text: '第15章 技术与研发管理', link: '/03-能力篇/ch15-技术与研发管理' },
            { text: '第16章 资源与工具管理', link: '/03-能力篇/ch16-资源与工具管理' },
            { text: '第17章 信息系统项目管理', link: '/03-能力篇/ch17-信息系统项目管理' },
          ]
        }
      ],
      '/04-实践篇/': [
        {
          text: '📕 第四篇 实践篇',
          collapsed: false,
          items: [
            { text: '第18章 智慧城市发展规划', link: '/04-实践篇/ch18-智慧城市发展规划' },
            { text: '第19章 智慧园区发展规划', link: '/04-实践篇/ch19-智慧园区发展规划' },
            { text: '第20章 数字乡村发展规划', link: '/04-实践篇/ch20-数字乡村发展规划' },
            { text: '第21章 企业数字化转型发展规划', link: '/04-实践篇/ch21-企业数字化转型发展规划' },
            { text: '第22章 智能制造发展规划', link: '/04-实践篇/ch22-智能制造发展规划' },
            { text: '第23章 新型消费系统规划', link: '/04-实践篇/ch23-新型消费系统规划' },
            { text: '第24章 法律法规与标准规范', link: '/04-实践篇/ch24-法律法规与标准规范' },
          ]
        }
      ],
      '/附录/': [
        {
          text: '📋 附录',
          items: [
            { text: '备考方案总览', link: '/附录/备考方案总览' },
            { text: '论文万能框架', link: '/附录/论文万能框架' },
            { text: '记忆口诀汇总', link: '/附录/记忆口诀汇总' },
            { text: '首考真题复盘', link: '/附录/首考真题复盘' },
          ]
        }
      ]
    },

    socialLinks: [],

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索' },
          modal: { displayDetails: '显示详情', noResultsText: '无结果', resetButtonTitle: '重置' },
        }
      }
    },

    editLink: {
      pattern: 'https://github.com/weinloop/xg/edit/main/:path',
      text: '编辑此页'
    },

    lastUpdated: {
      text: '最后更新',
      formatOptions: { dateStyle: 'short' }
    },

    docFooter: {
      prev: '上一章',
      next: '下一章'
    },

    outline: {
      label: '目录',
      level: [2, 3]
    }
  }
})
