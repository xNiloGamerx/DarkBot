CREATE OR REPLACE FUNCTION get_user_by_id(p_id text)
RETURNS SETOF "user"
SET search_path = public
AS $$
BEGIN
  return query
  select *
  from "user"
  where id = (p_id)::bigint;
END;
$$ LANGUAGE plpgsql;