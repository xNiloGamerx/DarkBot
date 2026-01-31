create or replace function create_counting_guild(p_data jsonb)
returns jsonb
as $$
declare
  res_guild_id bigint;
  res_channel_id bigint;
  res_id bigint;
begin
  -- select guild id from given guild_id
  select id
  into res_guild_id
  from "guild"
  where guild_id = p_data->>'guild_id';

  if not found then
    return jsonb_build_object(
      'message', 'Guild was not found',
      'status', 'not found'
    );
  end if;

  -- select guild id from given guild_id
  select id
  into res_channel_id
  from "channel"
  where channel_id = p_data->>'channel_id';

  if not found then
    return jsonb_build_object(
      'message', 'Channel was not found',
      'status', 'not found'
    );
  end if;

  insert into "counting_guild" (guild_id, channel_id)
  values (res_guild_id, res_channel_id)
  on conflict (guild_id) do update
  set guild_id = excluded.guild_id
  returning id into res_id;

  return jsonb_build_object(
    'id', res_id,
    'status', 'ok'
  );
end;
$$ language plpgsql;