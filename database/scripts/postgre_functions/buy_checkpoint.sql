create or replace function buy_checkpoint(p_data jsonb)
returns jsonb
set search_path = public
as $$
declare
  res_count_points bigint;
  res_last_counted_number bigint;
  res_count_checkpoint bigint;
begin
  select count_points, last_counted_number, count_checkpoint
  into res_count_points, res_last_counted_number, res_count_checkpoint
  from "counting_guild";

  if res_last_counted_number - res_count_checkpoint <= 5 then
    return jsonb_build_object(
      'message', 'Der Checkpoint kann erst nach mehr 5 counts wieder gekauft werden!',
      'result', false,
      'status', 'ok'
    );
  end if;

  if (p_data->>'price')::bigint > res_count_points then
    return jsonb_build_object(
      'message', 'Nicht genug Punkte!',
      'result', false,
      'status', 'ok'
    );
  end if;

  update "counting_guild"
    set
      "count_checkpoint" = "last_counted_number",
      "count_points" = "count_points" - (p_data->>'price')::bigint
    where id = (p_data->>'id')::bigint;

  return jsonb_build_object(
    'message', 'Updated data for buying checkpoint',
    'result', true,
    'status', 'ok'
  );
end;
$$ language plpgsql;