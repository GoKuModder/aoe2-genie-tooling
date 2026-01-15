import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "GenieTooling",
  description: "Python tools for Age of Empires II DAT file editing",
  base: "/aoe2-genie-tooling/",
  
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],

  themeConfig: {
    nav: [
      { text: 'Docs', link: '/getting-started' },
      { text: 'GitHub', link: 'https://github.com/GoKuModder/aoe2-genie-tooling' },
      { text: 'Discord', link: '#' }
    ],

    sidebar: [
      {
        text: 'General',
        collapsed: false,
        items: [
          { text: 'Introduction', link: '/' },
          { text: 'Getting Started', link: '/getting-started' },
          { text: 'Datasets Reference', link: '/datasets' }
        ]
      },
      {
        text: 'Units',
        collapsed: false,
        items: [
          { text: 'Units Overview', link: '/units' },
          { text: 'Methods', link: '/units/methods' },
          { text: 'Attributes', link: '/units/attributes' },
          { text: 'Tasks & TaskBuilder', link: '/units/tasks' },
          { text: 'Attacks & Armours', link: '/units/attacks-armours' },
          { text: 'Train Locations', link: '/units/train-locations' }
        ]
      },
      {
        text: 'Effects',
        collapsed: false,
        items: [
          { text: 'Effects Overview', link: '/effects' },
          { text: 'Methods', link: '/effects/methods' },
          { text: 'Command Reference', link: '/effects/effect-commands' }
        ]
      },
      {
        text: 'Technologies',
        collapsed: false,
        items: [
          { text: 'Techs Overview', link: '/techs' },
          { text: 'Methods', link: '/techs/methods' },
          { text: 'Attributes', link: '/techs/attributes' },
          { text: 'Research Locations', link: '/techs/research-locations' }
        ]
      },
      {
        text: 'Graphics',
        collapsed: false,
        items: [
          { text: 'Graphics Overview', link: '/graphics' },
          { text: 'Methods', link: '/graphics/methods' },
          { text: 'Attributes', link: '/graphics/attributes' },
          { text: 'Deltas & Layers', link: '/graphics/deltas' }
        ]
      },
      {
        text: 'Sounds',
        collapsed: false,
        items: [
          { text: 'Sounds Overview', link: '/sounds' },
          { text: 'Methods', link: '/sounds/methods' },
          { text: 'Attributes', link: '/sounds/attributes' }
        ]
      },
      {
        text: 'Civilizations',
        collapsed: false,
        items: [
          { text: 'Civilizations Overview', link: '/civilizations' },
          { text: 'Methods', link: '/civilizations/methods' },
          { text: 'Attributes', link: '/civilizations/attributes' }
        ]
      },
      {
        text: 'Advanced',
        collapsed: false,
        items: [
          { text: 'Technicalities', link: '/technicalities/' },
          { text: 'Error Handling', link: '/technicalities/error-handling' },
          { text: 'Validation', link: '/technicalities/validation' },
          { text: 'ID Preservation', link: '/technicalities/id-preservation' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/GoKuModder/aoe2-genie-tooling' },
      { icon: 'discord', link: '#' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: '© 2024 GOKUMODDER'
    },

    search: {
      provider: 'local'
    },

    outline: {
      level: [2, 3],
      label: 'On This Page'
    },

    editLink: {
      pattern: 'https://github.com/GoKuModder/aoe2-genie-tooling/edit/main/docs/:path',
      text: 'View on GitHub'
    },

    lastUpdated: {
      text: 'Revision',
      formatOptions: {
        dateStyle: 'short'
      }
    }
  }
})
