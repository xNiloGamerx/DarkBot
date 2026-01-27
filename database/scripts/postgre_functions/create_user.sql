create or replace function create_user(p_data jsonb)
returns jsonb
as $$
declare
  guild_id bigint;
  res_id bigint;
begin
  -- select guild id from given guild_id
  select id
  into guild_id
  from "guild"
  where guild_id = p_data->>'guild_id';

  if not found then
    return jsonb_build_object(
      'message', 'Guild was not found',
      'status', 'not found'
    );
  end if;

  insert into "user" (user_id, username, display_name, created_at)
  values (
    p_data->>'user_id', 
    p_data->>'username', 
    p_data->>'display_name', 
    (p_data->>'created_at')::timestamptz
  )
  on conflict (user_id) do nothing
  returning id into res_id;

  if res_id is null then
    select id
    into res_id
    from "user"
    where user_id = p_data->>'user_id';
  end if;

  insert into "user_guild" (user_id, guild_id, joined_at)
  values (res_id, guild_id, (p_data->>'joined_at')::timestamptz)
  on conflict (user_id, guild_id) do nothing;

  return jsonb_build_object(
    'id', res_id,
    'status', 'ok'
  );
end;
$$ language plpgsql;