-- A executer dans Supabase > SQL Editor (une seule fois, sur le projet de production)

create table if not exists contact_submissions (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name text not null,
  email text not null,
  phone text,
  pole text not null,
  message text not null,
  lang text not null default 'fr'
);

alter table contact_submissions enable row level security;

-- Le site public (cle "anon") peut uniquement INSERER des lignes,
-- jamais les lire, les modifier ou les supprimer.
create policy "public_insert_contact_submissions"
  on contact_submissions
  for insert
  to anon
  with check (true);

-- Optionnel : recevoir un email a chaque nouveau message.
-- Supabase > Database > Webhooks > "Create a new hook"
--   Table: contact_submissions, Event: INSERT
--   Type: HTTP Request vers une Edge Function ou un service comme
--   Resend / Zapier / Make qui enverra l'email de notification.
