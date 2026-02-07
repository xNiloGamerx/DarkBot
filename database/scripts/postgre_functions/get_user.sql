CREATE OR REPLACE FUNCTION get_user(p_user_id jsonb)
RETURNS SETOF "user"
SET search_path = public
AS $$
DECLARE
  res_user_guild_id bigint;
BEGIN
  return query
  select *
  from "user"
  where user_id = (p_user_id)::text;
END;
$$ LANGUAGE plpgsql;