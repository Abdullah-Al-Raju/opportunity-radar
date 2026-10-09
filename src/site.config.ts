import { defineSolitudeConfig } from './lib/config';

export default defineSolitudeConfig({
  site: 'https://opportunity-radar-c60.pages.dev',
  title: 'Opportunity Radar',
  description:
    'Real-time radar for fully funded international scholarships, global fellowships, grants, and high-value developer tools.',
  locale: 'en',
  timeZone: 'UTC',
  author: { name: 'Opportunity Radar Editorial Team' },
  menus: [
    {
      name: 'Opportunities',
      children: [
        { name: 'All Guides', url: '/archives/', icon: 'fas fa-graduation-cap' },
        { name: 'Categories', url: '/categories/', icon: 'fas fa-clone' },
        { name: 'Tags', url: '/tags/', icon: 'fas fa-tags' },
      ],
    },
    {
      name: 'Scholarships',
      url: '/categories/scholarships/',
      icon: 'fas fa-award',
    },
    {
      name: 'Dev & AI Tools',
      url: '/categories/developer-tools/',
      icon: 'fas fa-code',
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
        'Opportunity Radar': [
          {
            name: 'Opportunity Radar',
            url: 'https://opportunity-radar-c60.pages.dev',
            icon: '/img/logo.png',
          },
        ],
      },
    },
    hometop: {
      banner: {
        title: 'Global Opportunity & Tech Radar',
        desc: 'Fully funded scholarships, international fellowships, and premium developer tools for free.',
      },
    },
    aside: {
      home: { noSticky: 'about', Sticky: 'allInfo' },
      post: { noSticky: 'about', Sticky: 'newestPost,allInfo' },
      page: { noSticky: 'about', Sticky: 'newestPost,allInfo' },
      my_card: {
        description: 'Autonomous research radar tracking global education & tech grants.',
        content: 'Funding your future with zero student debt.',
        witty_words: ['Fully Funded 2026/2027', 'Global Fellowships', 'Free Developer Tools'],
        information: [
          {
            name: 'RSS Feed',
            url: '/index.xml',
            icon: 'fas fa-rss',
          },
          {
            name: 'All Scholarships',
            url: '/categories/scholarships/',
            icon: 'fas fa-graduation-cap',
          },
        ],
      },
    },
    footer: {
      information: {
        left: [
          {
            name: 'Opportunity Radar',
            url: 'https://opportunity-radar-c60.pages.dev',
            icon: 'fas fa-globe',
          },
        ],
        right: [{ name: 'RSS', url: '/index.xml', icon: 'fas fa-rss' }],
      },
      group: {
        Explore: [
          { name: 'All Guides', url: '/archives/' },
          { name: 'Scholarships', url: '/categories/scholarships/' },
          { name: 'Developer Tools', url: '/categories/developer-tools/' },
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
    search: { tags: ['Scholarships', 'Grants', 'Developer Tools', 'AI'], local: { preload: true } },
    pwa: { enable: true },
    extends: {
      head: [
        // Meta tags for SEO and IndexNow verification if needed
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />',
      ],
      body: [],
    },
  },
});
