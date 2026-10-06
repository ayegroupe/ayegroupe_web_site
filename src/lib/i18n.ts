export type Lang = 'fr' | 'en';

export const translations = {
  fr: {
    nav: {
      home: 'Accueil',
      servicesIt: 'Services IT',
      creative: 'Studio Créatif',
      togo: 'Pôle Togo & Logistique',
      saas: 'Nos SaaS',
      about: 'À propos',
      contact: 'Contact',
      quote: 'Demander un devis',
    },
    footer: {
      baseline: 'Ingénierie logicielle depuis Surrey, Canada & hub commercial et logistique au Togo.',
      quickLinks: 'Navigation rapide',
      poles: 'Nos Pôles d\'activité',
      itPoleTitle: 'Pôle IT & Ingénierie',
      togoPoleTitle: 'Pôle Togo & Afrique',
      saasProducts: 'Produits SaaS en ligne',
      ayeprepDesc: 'Plateforme IA de préparation aux examens TCF / TEF Canada.',
      ayejobDesc: 'Portail intelligent de recrutement et carrières.',
      legal: 'Mentions Légales & Confidentialité',
      rights: 'Tous droits réservés. AYEGROUPE.',
      surreyAddress: 'Surrey, Colombie-Britannique, Canada',
      lomeAddress: 'Hub Régional : Lomé, Togo',
      emailAddress: 'ayegroupe@ayegroupe.com',
      whatsappPhone: '+1 778 809 1060',
      whatsappUrl: 'https://wa.me/17788091060',
      directContact: 'Contact Direct & WhatsApp',
    },
    common: {
      discoverMore: 'En savoir plus',
      contactUs: 'Nous contacter',
      liveProduct: 'En production',
      verified: 'Vérifié & Certifié',
      talkToExpert: 'Échanger avec un expert',
      viewAllActivities: 'Consulter les 38 activités déclarées',
    }
  },
  en: {
    nav: {
      home: 'Home',
      servicesIt: 'IT Services',
      creative: 'Creative Studio',
      togo: 'Togo Hub',
      saas: 'Our SaaS',
      about: 'About Us',
      contact: 'Contact',
      quote: 'Request a Quote',
    },
    footer: {
      baseline: 'Software engineering from Surrey, Canada & West Africa commercial and logistics hub.',
      quickLinks: 'Quick Navigation',
      poles: 'Business Divisions',
      itPoleTitle: 'IT & Software Engineering',
      togoPoleTitle: 'Togo & Africa Hub',
      saasProducts: 'Online SaaS Products',
      ayeprepDesc: 'AI-powered preparation platform for TCF / TEF Canada exams.',
      ayejobDesc: 'Smart recruitment and career matchmaking portal.',
      legal: 'Legal Notice & Privacy Policy',
      rights: 'All rights reserved. AYEGROUPE.',
      surreyAddress: 'Surrey, British Columbia, Canada',
      lomeAddress: 'Regional Hub: Lomé, Togo',
      emailAddress: 'ayegroupe@ayegroupe.com',
      whatsappPhone: '+1 778 809 1060',
      whatsappUrl: 'https://wa.me/17788091060',
      directContact: 'Direct Contact & WhatsApp',
    },
    common: {
      discoverMore: 'Learn more',
      contactUs: 'Contact Us',
      liveProduct: 'Live in Production',
      verified: 'Verified & Certified',
      talkToExpert: 'Speak with an Expert',
      viewAllActivities: 'View all 38 declared activities',
    }
  }
};

/** Pages dont le slug change selon la langue : une simple substitution de
 *  prefixe y fabrique une URL inexistante. */
const SLUG_PAIRS: ReadonlyArray<readonly [string, string]> = [
  ['/fr/services-creatifs', '/en/creative-services'],
];

/** Pages qui n'existent que dans une langue (outils internes). */
const SANS_EQUIVALENT = new Set(['/fr/tiktok-visuels']);

/**
 * Chemin equivalent dans l'autre langue, ou null si la page n'a pas de
 * traduction. Source unique pour le commutateur de langue et les hreflang :
 * les deux divergeaient, et le commutateur pointait vers des 404.
 */
export function altPath(currentPath: string, target: Lang): string | null {
  const p = currentPath.replace(/\/+$/, '') || `/${target}`;
  if (SANS_EQUIVALENT.has(p)) return null;

  for (const [fr, en] of SLUG_PAIRS) {
    if (p === fr || p === en) return target === 'fr' ? fr : en;
  }

  const swapped = p.replace(/^\/(fr|en)(\/|$)/, `/${target}$2`);
  return swapped.startsWith(`/${target}`) ? swapped : `/${target}`;
}
