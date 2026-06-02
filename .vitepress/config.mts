import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'XG',
  description: '知识体系',
  lang: 'zh-CN',
  base: '/xg/',
  head: [['link', { rel: 'icon', type: 'image/svg+xml', href: '/xg/favicon.svg' }]],

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '基础篇', link: '/01-基础篇/ch01-信息系统与信息技术发展' },
      { text: '方法篇', link: '/02-方法篇/' },
      { text: '能力篇', link: '/03-能力篇/ch11-信息系统治理' },
      { text: '论文', link: '/07-论文篇/' },
      { text: '模拟题', link: '/09-模拟题/' },
      { text: '备考方案', link: '/附录/备考方案总览' },
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
          link: '/02-方法篇/',
          collapsed: false,
          items: [
            {
              text: '第4章 信息系统规划 ✅',
              link: '/02-方法篇/ch04/',
              collapsed: true,
              items: [
                { text: '📖 精炼笔记', link: '/02-方法篇/ch04/ch04-信息系统规划' },
                { text: '🎴 学习卡片', link: '/02-方法篇/ch04/ch04-学习卡片' },
                { text: '🎤 语音复习脚本', link: '/02-方法篇/ch04/ch04-语音复习脚本' },
              ]
            },
            {
              text: '第5章 应用系统规划 ✅',
              link: '/02-方法篇/ch05/',
              collapsed: true,
              items: [
                { text: '📖 精炼笔记', link: '/02-方法篇/ch05/ch05-应用系统规划' },
                { text: '🎤 语音复习脚本', link: '/02-方法篇/ch05/ch05-语音复习脚本' },
              ]
            },
            {
              text: '第6章 云资源规划 ✅',
              link: '/02-方法篇/ch06/',
              collapsed: true,
              items: [
                { text: '📖 精炼笔记', link: '/02-方法篇/ch06/ch06-云资源规划' },
                { text: '🎤 语音复习脚本', link: '/02-方法篇/ch06/ch06-语音复习脚本' },
              ]
            },
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
            { text: '首考真题（2025年11月）', link: '/附录/首考真题-2025年11月' },
          ]
        }
      ],
      '/05-综合篇/': [
        {
          text: '🧩 第五篇 综合篇',
          collapsed: false,
          items: [
            { text: '综合知识整合', link: '/05-综合篇/' },
          ]
        }
      ],
      '/06-案例篇/': [
        {
          text: '📝 第六篇 案例篇',
          collapsed: false,
          items: [
            { text: '案例分析专题', link: '/06-案例篇/' },
          ]
        }
      ],
      '/07-论文篇/': [
        {
          text: '✍️ 第七篇 论文篇',
          collapsed: false,
          items: [
            { text: '论文写作专题', link: '/07-论文篇/' },
            { text: '论文万能框架', link: '/07-论文篇/论文万能框架' },
            { text: '华航招标书（基准素材）', link: '/07-论文篇/华航集团数据资产智能管理平台项目招标书' },
            { text: '14主题预测论文框架', link: '/07-论文篇/系统规划与管理师-14主题预测论文框架' },
            { text: '范文：服务持续改进与监督', link: '/07-论文篇/论文-论信息系统服务持续改进与监督' },
            { text: '真题存档：2025年11月', link: '/07-论文篇/真题存档-2025年11月-论信息系统服务持续改进与监督' },
            { text: '高分参考：医保系统运维', link: '/07-论文篇/高分参考-医保系统运维-持续改进与监督' },
          ]
        }
      ],
      '/08-英语篇/': [
        {
          text: '🔤 第八篇 英语篇',
          collapsed: false,
          items: [
            { text: '专业英语备考', link: '/08-英语篇/' },
            { text: '专业英语备考指南', link: '/08-英语篇/专业英语备考指南' },
          ]
        }
      ],
      '/09-模拟题/': [
        {
          text: '📝 第九篇 模拟题',
          collapsed: false,
          items: [
            { text: '模拟题总览', link: '/09-模拟题/' },
            {
              text: '第4章 信息系统规划',
              collapsed: false,
              items: [
                { text: '模拟题（含答案）', link: '/09-模拟题/第4章-信息系统规划/模拟题-第4章信息系统规划' },
                { text: '模拟题（无答案）', link: '/09-模拟题/第4章-信息系统规划/模拟题-第4章信息系统规划-无答案版' },
                { text: '错题本（6道错题）', link: '/09-模拟题/第4章-信息系统规划/错题本-第4章选择题' },
                { text: '论文范文：信息系统规划方法与应用', link: '/09-模拟题/第4章-信息系统规划/论文范文-论信息系统规划方法与应用' },
              ]
            }
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
