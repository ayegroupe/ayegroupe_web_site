-- Garde-fou anti-flood sur le formulaire de contact.
--
-- Le champ piege du formulaire arrete les robots qui lisent le HTML, mais la
-- cle "anon" etant publique, un robot peut ecrire directement dans l'API REST
-- en contournant le formulaire. Ce trigger plafonne les insertions quelle que
-- soit leur origine.
--
-- A executer une seule fois dans Supabase > SQL Editor.

create or replace function public.limit_contact_submissions()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  recent_same_email int;
  recent_total int;
begin
  select count(*) into recent_same_email
  from contact_submissions
  where email = new.email
    and created_at > now() - interval '1 hour';

  if recent_same_email >= 5 then
    raise exception 'Trop de demandes envoyees avec cette adresse. Merci de reessayer plus tard.'
      using errcode = 'check_violation';
  end if;

  select count(*) into recent_total
  from contact_submissions
  where created_at > now() - interval '1 hour';

  -- Plafond global genereux : il ne vise qu'a contenir un flood massif, pas
  -- a gener une activite commerciale normale.
  if recent_total >= 40 then
    raise exception 'Volume de demandes anormalement eleve. Merci de reessayer plus tard.'
      using errcode = 'check_violation';
  end if;

  return new;
end;
$$;

drop trigger if exists check_contact_submission_rate on public.contact_submissions;

create trigger check_contact_submission_rate
  before insert on public.contact_submissions
  for each row execute function public.limit_contact_submissions();

-- Verifier le nombre de demandes recues sur la derniere heure :
--   select count(*) from contact_submissions
--   where created_at > now() - interval '1 hour';
