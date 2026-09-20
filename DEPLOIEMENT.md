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
- Expéditeur actuel : `onboarding@resend.dev` — tant que le domaine n'est pas vérifié chez Resend, les emails **ne peuvent partir que vers `ayegroupe@ayegroupe.com`** (l'adresse propriétaire du compte Resend), et risquent d'arriver en indésirables.
- Pour envoyer depuis `contact@ayegroupe.com` vers n'importe quelle adresse : vérifier le domaine sur resend.com → Domains → Add Domain, puis ajouter les 3 enregistrements DNS fournis dans Cloudflare.
- Diagnostic en cas de non-réception : `select id, status_code, content, created from net._http_response order by created desc limit 10;` (200 = accepté par Resend).

## 4. DNS (Cloudflare)

Le domaine `ayegroupe.com` est géré via Cloudflare (nameservers `laila.ns.cloudflare.com` / `elliott.ns.cloudflare.com`).

| Enregistrement | Type | Nom | Valeur | Proxy |
|---|---|---|---|---|
| Apex | A / CNAME (flattening) | `@` | géré automatiquement par Vercel Domain Connect | DNS only |
| www | CNAME | `www` | `9dc371825286020a.vercel-dns-017.com` | **DNS only** (nuage gris, pas orange) |

⚠️ Si tu ajoutes un jour un autre enregistrement lié à Vercel, garde toujours le proxy Cloudflare désactivé ("DNS only"), sinon le certificat SSL de Vercel ne peut pas se générer.

## 5. Fichiers de config locaux importants

- `.env` (jamais commité) : contient `PUBLIC_SUPABASE_URL` et `PUBLIC_SUPABASE_ANON_KEY` pour le développement local (`npm run dev`).
- `.env.example` : modèle sans les vraies valeurs, commité pour référence.
- `astro.config.mjs` : `site: 'https://ayegroupe.com'` — à mettre à jour si le domaine principal change un jour.

## 6. Pièges déjà rencontrés (pour ne pas les refaire)

1. **Variables `PUBLIC_` en mode "Sensitive" sur Vercel** → build silencieusement cassé (valeurs vides). Toujours utiliser "Non-sensitive/Config" pour ces variables.
2. **`<script define:vars={...}>` dans un composant Astro** → désactive le bundling Vite, un `import()` relatif à l'intérieur ne fonctionne plus dans le navigateur. Passer les valeurs par attribut `data-*` à la place.
3. **`Astro.redirect()` en build statique** → génère une redirection vers l'URL **absolue** définie dans `site`, pas une URL relative. Problématique si testé sur un domaine temporaire (ex. `*.vercel.app`) avant que le domaine final soit branché.
4. **Reconnecter un repo Git à un projet Vercel existant ne redéploie pas automatiquement** ce qui a déjà été poussé avant la connexion — il faut un nouveau push (ou passer par le CLI directement) après coup.
5. **Ne pas ajouter `@astrojs/vercel` v7 pour créer une route serveur** tant qu'on est sur Astro 4 : cet adaptateur ne connaît que Node 18/20 et génère une fonction en `nodejs18.x`, un runtime retiré chez Vercel. Il faudrait d'abord migrer vers Astro 5 + adaptateur v8. C'est la raison pour laquelle la notification email passe par un trigger Postgres plutôt que par une route API du site.
