import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://ayegroupe.com',
  // Astro calcule l'empreinte de chaque script et style en ligne et les
  // inscrit dans un <meta> CSP par page. Les deux politiques — ce meta et
  // l'en-tete envoye par Vercel — s'appliquent en meme temps : une ressource
  // doit etre autorisee par les deux. C'est le meta qui impose les empreintes
  // et rend 'unsafe-inline' sans effet.
  // Les sources externes doivent y etre redeclarees, sinon le meta les bloque
  // alors que l'en-tete les autorise.
  experimental: {
    csp: {
      scriptDirective: {
        resources: [
          "'self'",
          'https://va.vercel-scripts.com',      // Vercel Web Analytics
          'https://www.googletagmanager.com',   // GA4, charge apres consentement
        ],
      },
      styleDirective: {
        resources: [
          "'self'",
          'https://fonts.googleapis.com',
        ],
      },
    },
  },
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
