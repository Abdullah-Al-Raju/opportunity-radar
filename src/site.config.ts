import { defineSolitudeConfig } from './lib/config';

export default defineSolitudeConfig({
  site: 'https://opportunity-radar-c60.pages.dev',
  title: 'Tech & AI Radar',
  description:
    'Autonomous radar tracking breakthrough AI models, open-source LLMs, developer tools, free cloud credits, and agentic workflows.',
  locale: 'en',
  timeZone: 'UTC',
  author: { name: 'Tech & AI Radar Editorial Team' },
  menus: [
    {
      name: 'Explore Tech',
      children: [
        { name: 'All Guides', url: '/archives/', icon: 'fas fa-layer-group' },
        { name: 'Categories', url: '/categories/', icon: 'fas fa-clone' },
        { name: 'Tags', url: '/tags/', icon: 'fas fa-tags' },
      ],
    },
    {
      name: 'AI Tools & LLMs',
      url: '/categories/ai-tools/',
      icon: 'fas fa-brain',
    },
    {
      name: 'Developer Tools',
      url: '/categories/developer-tools/',
      icon: 'fas fa-code',
    },
    {
      name: 'Autonomous Agents',
      url: '/categories/autonomous-agents/',
      icon: 'fas fa-robot',
    },
    {
      name: 'Cloud & Free Perks',
      url: '/categories/cloud-perks/',
      icon: 'fas fa-cloud',
    },
    {
      name: 'Trust & Legal',
      children: [
        { name: 'About Editorial', url: '/about/', icon: 'fas fa-user-shield' },
        { name: 'Contact Us', url: '/contact/', icon: 'fas fa-envelope' },
        { name: 'Privacy Policy', url: '/privacy/', icon: 'fas fa-shield-halved' },
        { name: 'Terms of Service', url: '/terms/', icon: 'fas fa-file-contract' },
        { name: 'Affiliate Disclaimer', url: '/disclaimer/', icon: 'fas fa-scale-balanced' },
      ],
    },
  ],
  theme: {
    lightbox: 'fancybox',
    nav: {
      group: {
        'Tech & AI Radar': [
          {
            name: 'Tech & AI Radar',
            url: 'https://opportunity-radar-c60.pages.dev',
            icon: '/img/logo.png',
          },
        ],
      },
    },
    hometop: {
      banner: {
        title: 'Autonomous AI & Developer Tech Radar',
        desc: 'Curated intelligence for breakthrough AI models, open-source LLMs, developer tools, and free cloud credits.',
      },
    },
    aside: {
      home: { noSticky: 'about', Sticky: 'allInfo' },
      post: { noSticky: 'about', Sticky: 'newestPost,allInfo' },
      page: { noSticky: 'about', Sticky: 'newestPost,allInfo' },
      my_card: {
        description: 'Autonomous intelligence engine tracking next-generation AI and developer technology.',
        content: 'Supercharge your engineering workflow with free AI tools.',
        witty_words: ['Breakthrough AI', 'Autonomous Agents', 'Free Cloud Credits', 'Developer Tools'],
        information: [
          {
            name: 'RSS Feed',
            url: '/index.xml',
            icon: 'fas fa-rss',
          },
          {
            name: 'AI Tools',
            url: '/categories/ai-tools/',
            icon: 'fas fa-brain',
          },
        ],
      },
    },
    footer: {
      information: {
        left: [
          {
            name: 'Tech & AI Radar',
            url: 'https://opportunity-radar-c60.pages.dev',
            icon: 'fas fa-microchip',
          },
        ],
        right: [{ name: 'RSS', url: '/index.xml', icon: 'fas fa-rss' }],
      },
      group: {
        Explore: [
          { name: 'All Guides', url: '/archives/' },
          { name: 'AI Tools', url: '/categories/ai-tools/' },
          { name: 'Developer Tools', url: '/categories/developer-tools/' },
          { name: 'Cloud & Perks', url: '/categories/cloud-perks/' },
        ],
        Legal: [
          { name: 'Privacy Policy', url: '/privacy/' },
          { name: 'Terms of Service', url: '/terms/' },
          { name: 'Affiliate Disclaimer', url: '/disclaimer/' },
          { name: 'Contact Editorial', url: '/contact/' },
        ],
      },
    },
    capsule: { enable: false, id: '', type: 'playlist', server: 'qishui' },
    post: {
      meta: { locate: false },
      covercolor: { enable: true, mode: 'local' },
    },
    brevity: { enable: false },
    keyboard: {
      enable: true,
      list: [
        { modifier: 'shift', key: 'D', action: 'toggleTheme' },
        { modifier: 'mod', key: 'F', action: 'openSearch' },
        { modifier: 'shift', key: 'K', action: 'toggleKeyboard' },
      ],
    },
    search: {
      tags: ['AI Tools', 'DeepSeek', 'Claude', 'Gemini', 'Ollama', 'Developer Tools', 'Cloud', 'Agents'],
      local: { preload: true },
    },
    pwa: { enable: true },
    extends: {
      head: [
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />',
      ],
      body: [],
    },
  },
});
