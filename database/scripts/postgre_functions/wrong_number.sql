create or replace function wrong_number(p_id bigint)
returns jsonb
set search_path = public
as $$
declare
  res_guild_id bigint;
  res_last_counted_user_id text;
  res_last_counted_number bigint;
  res_user_id bigint;
begin
  update "counting_guild"
  set
    last_counted_number = "counting_guild".count_checkpoint,
    last_counted_user_id = none,
    count_checkpoint = 0
  where id = p_id;

  return jsonb_build_object(
    'message', 'Right user right number',
    'result', true,
    'status', 'ok'
  );
end;
$$ language plpgsql;