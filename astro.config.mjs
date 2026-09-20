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
      // La racine est une page de redirection en noindex : l'inclure ferait
      // remonter une erreur "URL soumise marquée noindex" dans Search Console.
      filter: (page) => page !== 'https://ayegroupe.com/',
    }),
  ],
});
