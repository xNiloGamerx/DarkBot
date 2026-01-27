create or replace function create_guild(p_data jsonb)
returns jsonb
as $$
declare
  res_id bigint;
begin
  insert into guild (guild_id, name, created_at)
  values (p_data->>'guild_id', p_data->>'name', (p_data->>'created_at')::timestamptz)
  on conflict do nothing
  returning id into res_id;

  return jsonb_build_object(
    'id', res_id,
    'status', 'ok'
  );
end;
$$ language plpgsql;