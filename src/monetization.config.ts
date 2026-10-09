export interface MonetizationConfig {
  mode: 'instant' | 'adsense' | 'dual' | 'off';
  adsense: {
    enabled: boolean;
    clientId: string;
    slots: {
      headerBanner?: string;
      inArticle?: string;
      sidebar?: string;
      footer?: string;
    };
  };
  instantAds: {
    enabled: boolean;
    provider: 'monetag' | 'adsterra' | 'custom';
    headerBannerHtml: string;
    inArticleHtml: string;
    sidebarHtml: string;
  };
  affiliateDisclosures: {
    enabled: boolean;
    noticeText: string;
  };
  affiliates: {
    digitalOceanUrl: string;
    cloudGpuUrl: string;
    grammarlyUrl: string;
    githubStudentPackUrl: string;
  };
  sponsor: {
    buyMeACoffee?: string;
    kofi?: string;
    githubSponsors?: string;
  };
}

export const monetizationConfig: MonetizationConfig = {
  mode: 'instant', // 'instant' enables day-1 zero-barrier revenue units; switch to 'adsense' or 'dual' when Google approves
  adsense: {
    enabled: false,
    clientId: 'ca-pub-XXXXXXXXXXXXXXXX',
    slots: {
      headerBanner: '1234567890',
      inArticle: '2345678901',
      sidebar: '3456789012',
      footer: '4567890123',
    },
  },
  instantAds: {
    enabled: true,
    provider: 'custom',
    headerBannerHtml: `<div class="my-4 p-3.5 bg-gradient-to-r from-cyan-600/10 via-blue-600/10 to-indigo-600/10 border border-cyan-500/20 rounded-xl flex flex-wrap items-center justify-between gap-2 text-sm shadow-sm">
      <div class="flex items-center gap-2">
        <span class="text-base">⚡</span>
        <span class="font-medium text-slate-800 dark:text-slate-200">Unlock $1,000+ in Free Cloud Credits for AI & App Deployment (AWS, GCP, Azure)</span>
      </div>
      <a href="/p/free-cloud-credits-aws-azure-gcp-guide/" class="px-3.5 py-1.5 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg font-semibold text-xs tracking-wide transition-colors">Claim Credits &rarr;</a>
    </div>`,
    inArticleHtml: `<div class="my-6 p-4 bg-indigo-500/10 border border-indigo-500/30 rounded-xl text-center">
      <p class="text-[11px] font-bold text-indigo-700 dark:text-indigo-400 uppercase tracking-widest mb-1">Developer Recommended</p>
      <p class="text-sm font-semibold text-slate-800 dark:text-slate-100 mb-1">Deploy Full-Stack AI Models & Microservices with Free Tier Credits</p>
      <p class="text-xs text-slate-600 dark:text-slate-300 mb-3">High-speed NVMe cloud droplets, managed PostgreSQL, and free SSL certificates.</p>
      <a href="https://www.digitalocean.com" target="_blank" rel="nofollow noopener sponsored" class="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-bold text-xs shadow-sm transition-colors">Activate $200 Free Cloud Credits &rarr;</a>
    </div>`,
    sidebarHtml: `<div class="p-4 bg-slate-100 dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 text-center">
      <span class="text-[11px] uppercase font-bold text-cyan-600 dark:text-cyan-400 tracking-wider">Free Dev Suite</span>
      <h4 class="font-bold text-sm mt-1 mb-1 text-slate-900 dark:text-white">GitHub Student Developer Pack</h4>
      <p class="text-xs text-slate-600 dark:text-slate-400 mb-3">$200,000+ worth of free cloud hosting, domains & developer tools.</p>
      <a href="/p/github-student-developer-pack-guide/" class="block w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition-colors">Get Setup Guide &rarr;</a>
    </div>`,
  },
  affiliateDisclosures: {
    enabled: true,
    noticeText: 'Disclosure: Tech & AI Radar independently reviews software and developer infrastructure. Some links may earn us a referral commission at zero additional cost to you.',
  },
  affiliates: {
    digitalOceanUrl: 'https://m.do.co/c/free-credit',
    cloudGpuUrl: 'https://runpod.io',
    grammarlyUrl: 'https://grammarly.com',
    githubStudentPackUrl: 'https://education.github.com/pack',
  },
  sponsor: {
    buyMeACoffee: 'https://buymeacoffee.com',
    kofi: 'https://ko-fi.com',
    githubSponsors: 'https://github.com/sponsors',
  },
};
