# Configuration de déploiement — AYEGROUPE

Référence des paramètres mis en place. À garder à jour si un élément change (renommage de projet, nouveau domaine, etc.).

## 1. GitHub

| Paramètre | Valeur |
|---|---|
| Repo actif (à utiliser) | `github.com/ayegroupe/ayegroupe_web_site` (public) |
| Branche | `main` |
| Remote local | `origin` → `github-ayegroupe:ayegroupe/ayegroupe_web_site.git` (SSH) |
| Ancien repo (abandonné) | `github.com/noevansarl/ayegroupe_web_site` — ne plus l'utiliser, il n'est relié à aucun déploiement |

**Authentification push** : via une clé SSH dédiée, pas un token.
- Clé privée : `~/.ssh/ayegroupe_deploy`
- Config SSH : bloc `Host github-ayegroupe` dans `~/.ssh/config`
- Côté GitHub : Deploy Key ajoutée sur le repo (Settings → Deploy keys), avec accès en écriture.
- Un `git push origin main` fonctionne directement, sans mot de passe ni token.

## 2. Vercel

| Paramètre | Valeur |
|---|---|
| Compte / Team | `ayegroupe` (team slug interne : `ayegroupes-projects`) |
| Projet actif (à utiliser) | `ayegroupe_web_site` |
| Anciens projets (à ignorer) | `ayegroupe-web-site` (doublon créé par erreur), et tout projet sous l'équipe `ayegroupe_studio` (Pro) — jamais correctement relié |
| URL de déploiement Vercel | `https://ayegroupe-web-site.vercel.app` |
| Domaines personnalisés | `https://ayegroupe.com` et `https://www.ayegroupe.com` |
| Connexion Git | Repo `ayegroupe/ayegroupe_web_site`, branche `main` → chaque push déclenche un build + déploiement Production automatique |
| Variables d'environnement | `PUBLIC_SUPABASE_URL`, `PUBLIC_SUPABASE_ANON_KEY` — définies pour Production **et** Preview, en mode **Non-sensitive / Config** (⚠️ ne jamais les remettre en "Sensitive", ça les vide silencieusement au build pour les variables à préfixe `PUBLIC_`) |

**Si tu dois régénérer un accès CLI** : `vercel login` dans un terminal (pas besoin de token si tu es déjà connecté), puis dans le dossier du projet, la liaison est déjà enregistrée dans `.vercel/project.json`.

## 3. Supabase

| Paramètre | Valeur |
|---|---|
| Projet | `qgsjxnkaqgwmtlcmfldc` |
| URL | `https://qgsjxnkaqgwmtlcmfldc.supabase.co` |
| Table | `contact_submissions` (schéma dans [supabase/schema.sql](supabase/schema.sql)) |
| Sécurité | RLS activé — le rôle `anon` peut uniquement **insérer** (aucune lecture publique possible) |
| Où lire les messages reçus | Supabase Dashboard → Table Editor → `contact_submissions` (connecté en tant que propriétaire du projet) |
| Notification email | Trigger `on_contact_submission` → appelle l'API Resend via `pg_net` (script : [supabase/notification_email.sql](supabase/notification_email.sql)) |

**Notifications email (Resend)**
- Clé API stockée chiffrée dans le Vault Supabase sous le nom `resend_api_key` (jamais dans le code).
- Expéditeur : `contact@ayegroupe.com`, destinataire : `ayegroupe@ayegroupe.com`, `reply_to` = l'email du prospect (répondre à l'email répond directement au client).
- Domaine `ayegroupe.com` déclaré chez Resend. Enregistrements DNS en place dans Cloudflare : DKIM (`resend._domainkey`), MX + SPF (`send`, en CNAME vers l'infra Resend), DMARC (`_dmarc`, politique `p=none`).
- Diagnostic en cas de non-réception : `select id, status_code, content, created from net._http_response order by created desc limit 10;` (200 = accepté par Resend).

## 4. DNS (Cloudflare)

Le domaine `ayegroupe.com` est géré via Cloudflare (nameservers `laila.ns.cloudflare.com` / `elliott.ns.cloudflare.com`).

| Enregistrement | Type | Nom | Valeur | Proxy |
|---|---|---|---|---|
| Apex | A / CNAME (flattening) | `@` | géré automatiquement par Vercel Domain Connect | DNS only |
| www | CNAME | `www` | `9dc371825286020a.vercel-dns-017.com` | **DNS only** (nuage gris, pas orange) |

⚠️ Si tu ajoutes un jour un autre enregistrement lié à Vercel, garde toujours le proxy Cloudflare désactivé ("DNS only"), sinon le certificat SSL de Vercel ne peut pas se générer.

## 5. Référencement (Google Search Console)

| Paramètre | Valeur |
|---|---|
| Propriété | `ayegroupe.com`, type **Domaine** (couvre www/non-www, http/https), vérifiée par TXT DNS |
| Sitemap soumis | `https://ayegroupe.com/sitemap-index.xml` |
| robots.txt | [public/robots.txt](public/robots.txt) — une seule directive `Sitemap:`, vers le sitemap-index |

- Sur une propriété de type **Domaine**, Search Console exige l'**URL complète** du sitemap (`https://ayegroupe.com/sitemap-index.xml`) ; saisir seulement `sitemap-index.xml` renvoie « adresse de sitemap incorrecte ».
- La racine `/` est une **redirection HTTP 308 vers `/fr`**, déclarée dans [vercel.json](vercel.json) — il n'existe aucune page à cette adresse. Ne jamais demander son indexation : inspecter `/fr/` à la place.
- Les titres de page ne doivent **pas** contenir `| AYEGROUPE` : le `BaseLayout` ajoute déjà ce suffixe.

## 6. Mesure d'audience

| Outil | Configuration |
|---|---|
| Vercel Web Analytics | Composant `@vercel/analytics/astro` dans le `BaseLayout`. Sans cookie → chargé sans consentement. **Doit être activé** dans Vercel → projet → onglet Analytics, sinon rien n'est collecté. |
| Google Analytics 4 | Propriété `AYEGROUPE`, ID de mesure `G-X79Z15EJBW`, fourni via la variable `PUBLIC_GA_MEASUREMENT_ID` (Production + Preview). |
| Consentement | [src/components/CookieConsent.astro](src/components/CookieConsent.astro) — bannière FR/EN, choix mémorisé dans `localStorage` sous `ayegroupe-cookie-consent`. GA4 n'est injecté qu'après acceptation. |

- Si `PUBLIC_GA_MEASUREMENT_ID` est absent, GA4 n'est pas chargé **et** la bannière ne s'affiche pas (aucun cookie déposé, donc rien à consentir).
- ⚠️ Le détecteur de balise de Google affichera **toujours** « balise non détectée » : son robot ne clique pas sur « Accepter ». Ce n'est pas une erreur. Pour vérifier réellement GA4 : naviguer sur le site en privé, accepter la bannière, et se regarder apparaître dans GA4 → Rapports → Temps réel.
- Une variable d'environnement ajoutée sur Vercel ne déclenche pas de rebuild : il faut pousser un commit (au besoin `git commit --allow-empty`) pour qu'elle soit prise en compte.

## 7. Socle technique

- **Astro 5** (build statique, sans adaptateur), **Tailwind 3** via `@astrojs/tailwind` v6, `@astrojs/sitemap`.
- Ne pas monter au-delà d'Astro 5 sans traiter Tailwind : `@astrojs/tailwind` ne supporte pas Astro 6+, la suite impose une migration vers Tailwind 4 (configuration entièrement différente, risque de régressions visuelles).
- `npm audit` signale des alertes sur Astro, y compris une « critique ». Elles visent des fonctionnalités **non utilisées ici** : `astro:assets` (l'alerte critique, liée à l'optimisation AVIF), le rendu serveur, les middlewares, `define:vars`, les *spread props*, les *view transitions* et les *server islands*. Le site étant 100 % statique et n'employant aucun de ces mécanismes, ces alertes ne constituent pas une exposition réelle — le vérifier avant de déclencher une migration en urgence.

## 8. Fichiers de config locaux importants

- `.env` (jamais commité) : contient `PUBLIC_SUPABASE_URL` et `PUBLIC_SUPABASE_ANON_KEY` pour le développement local (`npm run dev`).
- `.env.example` : modèle sans les vraies valeurs, commité pour référence.
- `astro.config.mjs` : `site: 'https://ayegroupe.com'` — à mettre à jour si le domaine principal change un jour.

## 8. Pièges déjà rencontrés (pour ne pas les refaire)

1. **Variables `PUBLIC_` en mode "Sensitive" sur Vercel** → build silencieusement cassé (valeurs vides). Toujours utiliser "Non-sensitive/Config" pour ces variables.
2. **`<script define:vars={...}>` dans un composant Astro** → désactive le bundling Vite, un `import()` relatif à l'intérieur ne fonctionne plus dans le navigateur. Passer les valeurs par attribut `data-*` à la place.
3. **`Astro.redirect()` en build statique** → génère une redirection vers l'URL **absolue** définie dans `site`, pas une URL relative. Problématique si testé sur un domaine temporaire (ex. `*.vercel.app`) avant que le domaine final soit branché.
4. **Reconnecter un repo Git à un projet Vercel existant ne redéploie pas automatiquement** ce qui a déjà été poussé avant la connexion — il faut un nouveau push (ou passer par le CLI directement) après coup.
5. **Pour ajouter une route serveur (API), utiliser `@astrojs/vercel` v8** — la v7 ne connaît que Node 18/20 et génère une fonction en `nodejs18.x`, un runtime retiré chez Vercel. C'est ce blocage, du temps d'Astro 4, qui a conduit à faire passer la notification email par un trigger Postgres plutôt que par une route API du site. Le site étant désormais sur Astro 5, une route serveur redevient envisageable.
