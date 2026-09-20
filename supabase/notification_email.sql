-- Notification email a chaque nouveau message du formulaire de contact.
--
-- Principe : un trigger Postgres appelle l'API Resend via pg_net a chaque
-- insertion dans contact_submissions. Aucune modification du site n'est
-- necessaire : le formulaire continue d'ecrire directement dans Supabase.
--
-- A executer une seule fois dans Supabase > SQL Editor.
-- Remplacer au prealable les deux valeurs marquees CHANGER.

-- 1. Extension pour les appels HTTP sortants depuis la base
create extension if not exists pg_net with schema extensions;

-- 2. Stocker la cle API Resend dans le Vault (chiffree, jamais en clair
--    dans la definition de la fonction)
select vault.create_secret('re_CHANGER_CLE_RESEND', 'resend_api_key');

-- 3. Fonction declenchee a chaque nouveau message
create or replace function public.notify_contact_submission()
returns trigger
language plpgsql
security definer
set search_path = public, extensions, vault
as $$
declare
  api_key text;
begin
  select decrypted_secret into api_key
  from vault.decrypted_secrets
  where name = 'resend_api_key';

  perform net.http_post(
    url := 'https://api.resend.com/emails',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer ' || api_key
    ),
    body := jsonb_build_object(
      -- Necessite que le domaine soit ajoute chez Resend. Sinon, repli sur
      -- 'AYEGROUPE <onboarding@resend.dev>' (envoi limite a l'adresse
      -- proprietaire du compte Resend).
      'from', 'AYEGROUPE <contact@ayegroupe.com>',
      'to', jsonb_build_array('CHANGER@exemple.com'),
      'reply_to', new.email,
      'subject', 'Nouvelle demande AYEGROUPE - ' || new.name,
      'text', concat_ws(E'\n',
        'Nom / Societe : ' || new.name,
        'Email : ' || new.email,
        'Telephone : ' || coalesce(new.phone, '-'),
        'Pole : ' || new.pole,
        'Langue : ' || new.lang,
        'Recu le : ' || to_char(new.created_at, 'DD/MM/YYYY HH24:MI'),
        '',
        'Message :',
        new.message
      )
    )
  );

  return new;
end;
$$;

-- 4. Brancher la fonction sur la table
drop trigger if exists on_contact_submission on public.contact_submissions;

create trigger on_contact_submission
  after insert on public.contact_submissions
  for each row execute function public.notify_contact_submission();

-- ---------------------------------------------------------------------------
-- Diagnostic : pg_net envoie les requetes en arriere-plan. Pour verifier ce
-- que Resend a repondu aux derniers envois :
--
--   select id, status_code, content, created
--   from net._http_response
--   order by created desc
--   limit 10;
--
-- status_code 200 = email accepte par Resend.
-- 403 = domaine expediteur non verifie, ou destinataire non autorise tant
-- que le domaine n'est pas verifie chez Resend.
-- ---------------------------------------------------------------------------
