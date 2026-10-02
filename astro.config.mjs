import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://ayegroupe.com',
  i18n: {
    defaultLocale: 'fr',
    locales: ['fr', 'en'],
    routing: {
      prefixDefaultLocale: true,
      redirectToDefaultLocale: false,
    }
  },
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
    sitemap({
      // Outil de production interne : ne doit pas etre soumis a Google.
      filter: (page) => !page.includes('/tiktok-visuels'),
    }),
  ],
});
