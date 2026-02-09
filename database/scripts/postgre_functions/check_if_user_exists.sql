create or replace function check_if_user_exists(p_user_id text, p_guild_id text)
returns jsonb
set search_path = public
as $$
begin
  PERFORM *
    FROM "user_guild"
    INNER JOIN "user" ON "user_guild".user_id = "user".id
    INNER JOIN "guild" ON "user_guild".guild_id = "guild".id
    WHERE "user".user_id = p_user_id
      AND "guild".guild_id = p_guild_id;

  if not found then
    return jsonb_build_object(
      'message', 'User not found',
      'result', false,
      'status', 'ok'
    );
  end if;

  return jsonb_build_object(
    'message', 'User found',
    'result', true,
    'status', 'ok'
  );
end;
$$ language plpgsql;
