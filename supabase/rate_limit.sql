-- Garde-fou anti-flood sur le formulaire de contact.
--
-- Le champ piege du formulaire arrete les robots qui lisent le HTML, mais la
-- cle "anon" etant publique, un robot peut ecrire directement dans l'API REST
-- en contournant le formulaire. Ce trigger plafonne les insertions quelle que
-- soit leur origine.
--
-- Principe : les limites sont TOUJOURS rapportees a un expediteur precis
-- (son email, son adresse IP). Aucun plafond global : un plafond commun a
-- tous les visiteurs permettrait a un spammeur d'empecher les vrais clients
-- d'ecrire, simplement en le saturant. Le connaitre ne lui sert donc a rien.
--
-- A executer dans Supabase > SQL Editor (remplace la version precedente).

create or replace function public.limit_contact_submissions()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  client_ip text;
  recent_same_email int;
  recent_same_ip int;
begin
  -- Limite par adresse email
  select count(*) into recent_same_email
  from contact_submissions
  where email = new.email
    and created_at > now() - interval '1 hour';

  if recent_same_email >= 4 then
    raise exception 'Trop de demandes envoyees avec cette adresse. Merci de reessayer plus tard.'
      using errcode = 'check_violation';
  end if;

  -- Limite par adresse IP : un spammeur ne penalise que lui-meme.
  -- L'en-tete peut contenir une liste "client, proxy1, proxy2" : on garde le
  -- premier element, qui identifie l'appelant.
  client_ip := nullif(
    split_part(
      coalesce(current_setting('request.headers', true)::json ->> 'x-forwarded-for', ''),
      ',', 1
    ),
    ''
  );

  if client_ip is not null then
    select count(*) into recent_same_ip
    from contact_submissions
    where client_ip_hash = md5(client_ip)
      and created_at > now() - interval '1 hour';

    if recent_same_ip >= 8 then
      raise exception 'Trop de demandes envoyees depuis ce poste. Merci de reessayer plus tard.'
        using errcode = 'check_violation';
    end if;

    -- Empreinte irreversible : permet de compter sans conserver l'IP en clair.
    new.client_ip_hash := md5(client_ip);
  end if;

  return new;
end;
$$;

-- Colonne technique utilisee par la limite par IP (empreinte, pas l'IP).
alter table public.contact_submissions
  add column if not exists client_ip_hash text;

create index if not exists contact_submissions_ip_recent
  on public.contact_submissions (client_ip_hash, created_at);

drop trigger if exists check_contact_submission_rate on public.contact_submissions;

create trigger check_contact_submission_rate
  before insert on public.contact_submissions
  for each row execute function public.limit_contact_submissions();
