# Plan d'exécution — Site web AYEGROUPE

> Document de spécification destiné à être exécuté par un agent (Antigravity). Il décrit l'architecture de l'information, le contenu, la stack technique, l'arborescence de fichiers et les phases de réalisation.

## 0. Résumé exécutif

AYEGROUPE est une entreprise individuelle avec deux pôles d'activité :

1. **Pôle IT / Ingénierie logicielle** (services déclarés à la création, portée internationale/remote) — conseil, développement sur mesure, intégration de systèmes.
2. **Pôle Togo** (présence physique/locale) — Import/Export, fourniture et maintenance de matériel IT/bureautique, logistique.

À cela s'ajoute une vitrine **Produits SaaS** présentant les deux SaaS déjà en production et monétisés : **AyePrep** (www.ayeprep.com) et **AyeJob** (www.ayejob.com), avec liens directs sortants.

Le site est un site **vitrine + génération de leads** (pas d'app web complexe), donc orienté contenu, rapide, SEO-friendly, bilingue FR/EN.

---

## 1. Objectifs du site

- Présenter AYEGROUPE comme une entreprise crédible sur deux marchés distincts (services IT internationaux vs. opérations physiques au Togo) sans les mélanger dans le message.
- Générer des contacts qualifiés (formulaire, WhatsApp, email, téléphone) pour chaque pôle d'activité.
- Mettre en avant les SaaS AyePrep et AyeJob comme preuve de compétence technique ("nous créons aussi nos propres produits") et rediriger le trafic vers eux.
- Être trouvable sur Google pour des requêtes locales togolaises (ex. "location de véhicule Lomé", "maintenance informatique Togo") ET des requêtes IT génériques (ex. "custom software development consultant").
- Rester simple à maintenir par une seule personne (pas de CMS lourd sauf besoin réel).

---

## 2. Identité de marque

À valider avec le client (toi) avant design, mais par défaut :

- **Nom** : AYEGROUPE
- **Baseline suggérée** : « Technologie, Commerce & Logistique — d'un seul groupe » (à ajuster)
- **Ton** : professionnel, direct, orienté PME/entreprises et administrations togolaises pour le pôle Togo ; ton plus "tech consulting" pour le pôle IT international.
- **Langues** : FR (langue principale, Togo) + EN (pôle IT international). Sélecteur de langue en haut de page.
- **Palette / logo** : si un logo existe déjà (à fournir), on en extrait la palette. Sinon palette par défaut proposée en section 7.

---

## 3. Architecture de l'information (sitemap)

```
/                          Accueil (groupe) — aiguille vers les 2 pôles + SaaS
/services-it/              Pôle IT & Ingénierie logicielle (international)
  /services-it/[categorie] Pages détail par catégorie de service (optionnel, phase 2)
/togo/                     Pôle Togo — Import/Export, IT & Bureautique, Logistique
  /togo/it-bureautique     Sous-section détaillée
  /togo/logistique         Sous-section détaillée
  /togo/import-export      Sous-section détaillée
/saas/                     Nos solutions SaaS (AyePrep, AyeJob) + CTA "on peut créer le vôtre"
/a-propos/                 À propos d'AYEGROUPE (entreprise individuelle, mission, valeurs)
/contact/                  Formulaire + coordonnées (par pôle)
/mentions-legales/         Mentions légales, RCCM/NIF si applicable, politique de confidentialité
/blog/ (optionnel, phase 2) Actualités / articles SEO
```

Navigation principale (header) : `Accueil · Services IT · Togo (Import-Export & Logistique) · Nos SaaS · À propos · Contact`
Footer : liens légaux, réseaux sociaux, coordonnées, liens directs vers ayeprep.com et ayejob.com.

---

## 4. Contenu détaillé par page

### 4.1 Accueil (`/`)
- Hero avec proposition de valeur globale du groupe + 2-3 CTA vers les pôles (Services IT / Togo / Nos SaaS).
- 3 blocs "pôles d'activité" (cartes) résumant chaque branche avec lien "En savoir plus".
- Bloc "Nos solutions SaaS" avec logos/captures AyePrep & AyeJob, lien direct externe vers chaque site.
- Bloc confiance : chiffres clés, secteurs servis, logos clients (si disponibles) — sinon différer.
- Bloc contact rapide.

### 4.2 Services IT (`/services-it/`)
Regrouper la longue liste officielle en **catégories lisibles** (le texte légal complet reste disponible, ex. en accordéon ou page "liste complète des activités déclarées" pour la conformité) :

1. **Développement logiciel sur mesure**
   custom application/software programming, custom computer programming services, custom software developers, software programming custom, systems analysis and design (software).
2. **Conseil & audit IT**
   IT consulting, computer consulting, computer hardware/software consulting, computer systems design consulting, requirements analysis (hardware).
3. **Conception & intégration de systèmes**
   computer systems design & analysis, management information systems design, office automation system design/integration, systems engineering / systems integration, computer systems integrators.
4. **Réseaux & infrastructure**
   local area network (LAN) design & integration, network systems integration.
5. **Solutions CAO/FAO/IAO (CAD/CAM/CAE)**
   CAD, CAM, CAE systems services.
6. **Exploitation, maintenance & continuité**
   computer system maintenance, computer facilities management, data processing facilities management, computer disaster recovery, facilities support services.
7. **Web & logiciels applicatifs**
   Internet/Web page design & development, software installation services, intégration de plusieurs logiciels dans le SI du client.
8. **Développement de SaaS monétisés** *(nouveau, à mettre en avant)*
   Conception, développement et exploitation de plateformes SaaS pour compte propre ou pour des clients (avec renvoi vers `/saas/` en preuve de réalisation : AyePrep, AyeJob).

Chaque catégorie : 2-3 phrases + liste à puces des prestations + CTA "Discuter de mon projet".

### 4.3 Togo — Import/Export, IT & Bureautique, Logistique (`/togo/`)
Page pôle avec 3 sous-blocs (chacun peut devenir une sous-page en phase 2) :

**A. General Trade — Import/Export**
- Import/export de marchandises générales, sourcing fournisseurs, dédouanement (si applicable).

**B. IT & Équipements de bureau**
- Fourniture, installation et maintenance d'équipements de bureau
- Fourniture, installation et maintenance de matériel informatique et consommables
- Fourniture de mobilier de bureau
- Câblage informatique et réseaux
- Analyse de données
- Migration Cloud
- IoT

**C. Logistique / Maintenance**
- Transport — acheminement de marchandises entre fournisseurs, entrepôts, clients
- Entreposage (warehousing)
- Gestion des stocks (suivi, contrôle, optimisation)
- Préparation de commandes et distribution (picking, packing, expédition)
- Location de véhicules
- Entretien et nettoyage de bureaux/bâtiments

CTA en fin de page : devis rapide / WhatsApp Business (très utilisé au Togo) / téléphone.

### 4.4 Nos solutions SaaS (`/saas/`)
- Intro : "AYEGROUPE conçoit aussi ses propres produits SaaS."
- Carte **AyePrep** : description courte, capture d'écran, bouton "Visiter www.ayeprep.com" (lien externe, `target="_blank"`, `rel="noopener noreferrer"`).
- Carte **AyeJob** : idem avec www.ayejob.com.
- Bloc CTA : "Vous voulez transformer votre idée en SaaS ?" → renvoi vers `/services-it/#saas` ou `/contact/`.

### 4.5 À propos (`/a-propos/`)
- Présentation d'AYEGROUPE (entreprise individuelle), mission, positionnement double (tech + commerce/logistique), pourquoi ce double pôle.
- Zone d'intervention (Togo pour le physique, international pour l'IT/remote).

### 4.6 Contact (`/contact/`)
- Formulaire simple (nom, email/téléphone, pôle concerné [IT / Togo / SaaS], message).
- Coordonnées directes : téléphone/WhatsApp, email, adresse (Togo).
- Carte (Google Maps embed) si adresse physique communicable.

### 4.7 Mentions légales (`/mentions-legales/`)
- Statut juridique (entreprise individuelle), RCCM/NIF si le client souhaite les afficher, politique de confidentialité, cookies.

---

## 5. Stack technique recommandée

Site principalement statique/contenu → privilégier **rapidité, SEO, faible coût d'hébergement, facilité de maintenance en solo**.

| Choix | Recommandation | Alternative |
|---|---|---|
| Framework | **Astro** (îlots interactifs légers, excellent SEO/perf) | Next.js si on veut prévoir une app/back-office plus tard |
| Styling | **Tailwind CSS** | CSS Modules |
| i18n | `astro-i18next` ou routing par dossier `/fr/`, `/en/` | next-intl (si Next.js) |
| Formulaire de contact | Formspree / Resend (email transactionnel) sans backend dédié | Fonction serverless (Vercel/Netlify) |
| Hébergement | **Vercel** ou **Netlify** (déploiement continu depuis GitHub) | GitHub Pages (si 100% statique, sans formulaire serverless) |
| CMS contenu (optionnel) | Fichiers Markdown/MDX versionnés dans le repo (pas de CMS pour démarrer) | Sanity/Payload si besoin d'édition non technique plus tard |
| Analytics | Plausible ou Google Analytics 4 | — |
| Nom de domaine | `ayegroupe.com` (ou `.tg`/`.com` selon disponibilité) | — |

> Ce choix est compatible avec exécution par un agent dans Antigravity : structure de fichiers simple, pas de base de données à provisionner au démarrage.

---

## 6. Arborescence de fichiers du projet

```
ayegroupe_web_site/
├── PLAN.md
├── README.md
├── astro.config.mjs
├── package.json
├── tailwind.config.cjs
├── public/
│   ├── favicon.svg
│   ├── logo/
│   └── images/
│       ├── services-it/
│       ├── togo/
│       └── saas/
└── src/
    ├── layouts/
    │   └── BaseLayout.astro
    ├── components/
    │   ├── Header.astro
    │   ├── Footer.astro
    │   ├── Hero.astro
    │   ├── ServiceCard.astro
    │   ├── SaasCard.astro
    │   ├── ContactForm.astro
    │   └── LanguageSwitcher.astro
    ├── content/
    │   ├── services-it/        (contenu structuré par catégorie, .md/.mdx)
    │   ├── togo/
    │   └── saas/
    ├── pages/
    │   ├── fr/
    │   │   ├── index.astro
    │   │   ├── services-it/index.astro
    │   │   ├── togo/
    │   │   │   ├── index.astro
    │   │   │   ├── it-bureautique.astro
    │   │   │   ├── logistique.astro
    │   │   │   └── import-export.astro
    │   │   ├── saas/index.astro
    │   │   ├── a-propos/index.astro
    │   │   ├── contact/index.astro
    │   │   └── mentions-legales/index.astro
    │   └── en/  (miroir de la structure fr/ pour le pôle IT international)
    └── styles/
        └── global.css
```

---

## 7. Design system (base de départ)

- **Couleurs** : bleu profond (confiance/tech) + accent orange ou vert (énergie/Afrique/commerce) — palette exacte à valider avec logo existant.
- **Typographie** : une sans-serif moderne (ex. Inter / Sora) pour titres, une sans-serif lisible pour le corps de texte.
- **Composants clés** : cartes de service, bandeaux CTA, badges "SaaS en ligne", accordéon pour la liste légale complète des activités déclarées.
- **Responsive** : mobile-first impératif (beaucoup de trafic togolais en mobile).

---

## 8. SEO, multilingue, performance

- Balises `title`/`meta description` uniques par page, en FR et EN.
- `hreflang` entre pages FR/EN équivalentes.
- Sitemap.xml + robots.txt générés automatiquement par Astro.
- Schéma structuré `LocalBusiness` (pôle Togo) et `ProfessionalService`/`Organization` (pôle IT) en JSON-LD.
- Core Web Vitals : images optimisées (`astro:assets`), lazy-loading, pas de JS lourd inutile.
- Mots-clés Togo à cibler : "maintenance informatique Lomé/Togo", "location de véhicule entreprise Togo", "import export Togo", "logistique Togo", "fourniture matériel bureau Togo".
- Mots-clés IT internationaux : "custom software development", "IT consulting services", "systems integration consultant".

---

## 9. Liens externes SaaS — règles d'implémentation

- Lien vers `https://www.ayeprep.com` et `https://www.ayejob.com` : `<a href="..." target="_blank" rel="noopener noreferrer">`.
- Ne jamais les intégrer en `<iframe>` (risque de blocage X-Frame-Options + mauvaise UX) — toujours redirection en nouvel onglet avec capture d'écran statique côté AYEGROUPE.

---

## 10. Phases d'exécution (à donner à l'agent Antigravity dans l'ordre)

**Phase 0 — Setup projet**
1. Initialiser projet Astro + Tailwind dans le repo existant.
2. Mettre en place `BaseLayout`, `Header`, `Footer`, `LanguageSwitcher`.
3. Configurer routing `/fr/` (défaut) et `/en/`.

**Phase 1 — Contenu statique des pages principales**
4. Page Accueil avec les 3 blocs pôles + bloc SaaS.
5. Page Services IT avec les 8 catégories (section 4.2).
6. Page Togo avec les 3 sous-blocs (section 4.3).
7. Page Nos SaaS (AyePrep + AyeJob) avec liens externes sécurisés.
8. Page À propos.

**Phase 2 — Contact & conformité**
9. Formulaire de contact (Formspree ou équivalent) + coordonnées + WhatsApp.
10. Page Mentions légales.
11. JSON-LD + meta SEO sur toutes les pages.

**Phase 3 — Finitions**
12. Responsive/QA sur mobile (prioritaire, marché togolais).
13. Sitemap.xml, robots.txt, favicon, OpenGraph images.
14. Analytics (Plausible/GA4).

**Phase 4 — Déploiement**
15. Déploiement Vercel/Netlify connecté au repo GitHub `ayegroupe_web_site`.
16. Connexion du nom de domaine `ayegroupe.*`.
17. Vérification Google Search Console + soumission sitemap.

**Phase 5 (optionnelle, ultérieure)**
18. Sous-pages détaillées par catégorie de service.
19. Blog/actualités pour le SEO.
20. Espace "études de cas" mettant en avant AyePrep/AyeJob comme réalisations.

---

## 11. Décisions en attente de validation par le client

- Logo et charte graphique existants ou à créer ?
- Nom de domaine définitif (`.com`, `.tg`, autre) ?
- Coordonnées exactes à publier (téléphone, WhatsApp, adresse Togo, RCCM/NIF) ?
- Faut-il afficher des références clients / réalisations concrètes dès le lancement ?
- Astro vs Next.js si une évolution vers un espace client (back-office, devis en ligne) est prévue à moyen terme ?
