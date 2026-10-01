-- Suppression des demandes de test accumulees pendant la mise en place.
-- A executer dans Supabase > SQL Editor.

-- 1. Verifier AVANT de supprimer : cette requete liste ce qui sera efface.
select created_at, name, email
from contact_submissions
where email like '%@example.com'
order by created_at;

-- 2. Si la liste ne contient bien que des tests, executer la suppression.
--    Les vraies demandes de clients n'utilisent pas le domaine example.com,
--    qui est reserve a la documentation (RFC 2606) et ne peut pas recevoir
--    d'email : aucune demande legitime ne peut donc etre perdue ici.
delete from contact_submissions
where email like '%@example.com';

-- 3. Controler ce qu'il reste.
select count(*) as demandes_restantes from contact_submissions;
