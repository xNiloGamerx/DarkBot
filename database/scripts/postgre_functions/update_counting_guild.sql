create or replace function update_counting_guild(
  p_id bigint,
  p_updates jsonb
)
returns counting_guild
as $$
declare
  res_row counting_guild;
begin
  update "counting_guild"
  set
    last_counted_number = coalesce(
      (p_updates->>'last_counted_number')::bigint, 
      last_counted_number
    ),
    last_counted_user_id = coalesce(
      (p_updates->>'last_counted_user_id')::bigint, 
      last_counted_user_id
    ),
    count_checkpoint = coalesce(
      (p_updates->>'count_checkpoint')::bigint, 
      count_checkpoint
    ),
    count_points = coalesce(
      (p_updates->>'count_points')::bigint, 
      count_points
    ),
    last_counted_at = coalesce(
      (p_updates->>'last_counted_at')::timestamptz, 
      last_counted_at
    )
  where id = p_id
  returning * into res_row;

  return res_row;
end;
$$ language plpgsql;