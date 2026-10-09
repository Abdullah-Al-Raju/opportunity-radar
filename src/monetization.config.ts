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
    wiseUrl: string;
    revolutUrl: string;
    grammarlyUrl: string;
    studentBeansUrl: string;
  };
  sponsor: {
    buyMeACoffee?: string;
    kofi?: string;
    paypal?: string;
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
    headerBannerHtml: `<div class="my-4 p-3.5 bg-gradient-to-r from-blue-600/10 via-indigo-600/10 to-purple-600/10 border border-blue-500/20 rounded-xl flex flex-wrap items-center justify-between gap-2 text-sm shadow-sm">
      <div class="flex items-center gap-2">
        <span class="text-base">🎓</span>
        <span class="font-medium text-slate-800 dark:text-slate-200">2026/2027 Fully-Funded International Scholarship Applications are Now Open</span>
      </div>
      <a href="/categories/scholarships/" class="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold text-xs tracking-wide transition-colors">Browse Deadlines &rarr;</a>
    </div>`,
    inArticleHtml: `<div class="my-6 p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl text-center">
      <p class="text-[11px] font-bold text-amber-700 dark:text-amber-400 uppercase tracking-widest mb-1">Recommended Student Tool</p>
      <p class="text-sm font-semibold text-slate-800 dark:text-slate-100 mb-1">Transfer international tuition and living funds with zero hidden markups</p>
      <p class="text-xs text-slate-600 dark:text-slate-300 mb-3">Save up to 8x compared to legacy banks when receiving scholarship payments.</p>
      <a href="https://wise.com" target="_blank" rel="nofollow noopener sponsored" class="inline-flex items-center gap-1.5 px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-bold text-xs shadow-sm transition-colors">Open Free Wise Account &rarr;</a>
    </div>`,
    sidebarHtml: `<div class="p-4 bg-slate-100 dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 text-center">
      <span class="text-[11px] uppercase font-bold text-blue-600 dark:text-blue-400 tracking-wider">Student Perk</span>
      <h4 class="font-bold text-sm mt-1 mb-1 text-slate-900 dark:text-white">GitHub Student Developer Pack</h4>
      <p class="text-xs text-slate-600 dark:text-slate-400 mb-3">$200,000+ worth of free cloud hosting, domains & developer tools.</p>
      <a href="/p/github-student-developer-pack-guide/" class="block w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition-colors">Claim Free Benefits &rarr;</a>
    </div>`,
  },
  affiliateDisclosures: {
    enabled: true,
    noticeText: 'Disclosure: Opportunity Radar provides independently researched guides. Some links are affiliate or referral links; if you register or apply through them, we may earn a commission at no extra cost to you.',
  },
  affiliates: {
    wiseUrl: 'https://wise.com',
    revolutUrl: 'https://revolut.com',
    grammarlyUrl: 'https://grammarly.com',
    studentBeansUrl: 'https://studentbeans.com',
  },
  sponsor: {
    buyMeACoffee: 'https://buymeacoffee.com',
    kofi: 'https://ko-fi.com',
  },
};
