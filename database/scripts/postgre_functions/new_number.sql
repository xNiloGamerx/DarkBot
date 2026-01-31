create or replace function new_number(p_data jsonb)
returns jsonb
as $$
declare
  res_guild_id bigint;
  res_last_counted_user_id text;
  res_last_counted_number bigint;
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

  -- get last user counted
  select "user".user_id
    from "counting_guild"
    into res_last_counted_user_id
    left join "user" on "user".id = "counting_guild".last_counted_user_id
    where "counting_guild".guild_id = p_data->>'guild_id';

  if not found then
    return jsonb_build_object(
      'message', 'Last counted user not in user table',
      'result', false,
      'status', 'ok'
    );
  end if;

  if res_last_counted_user_id <> p_data->>'last_counted_user_id' then
    return jsonb_build_object(
      'message', 'Last counted user equals currently counted user',
      'result', false,
      'status', 'ok'
    );
  end if;

  raise notice 'res_id: %', res_last_counted_user_id;

  -- get last counted number
  select last_counted_number
    from "counting_guild"
    into res_last_counted_number
    where "counting_guild".guild_id = res_guild_id;

  if (p_data->>'counted_number')::bigint <> res_last_counted_number + 1 then
    return jsonb_build_object(
      'message', 'Falsche Zahl',
      'result', false,
      'status', 'ok'
    );
  end if;

  update "counting_guild"
    set last_counted_user_id = res_last_counted_user_id
    where "counting_guild".guild_id = p_data->>'guild_id';
  
  update "counting_guild"
    set last_counted_number = last_counted_number + 1
    where "counting_guild".guild_id = p_data->>'guild_id';

  return jsonb_build_object(
    'message', 'Right user right number',
    'result', true,
    'status', 'ok'
  );
end;
$$ language plpgsql;