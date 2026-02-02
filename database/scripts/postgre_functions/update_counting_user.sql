create or replace function update_counting_user(
  p_id bigint,
  p_updates jsonb
)
returns counting_user
as $$
declare
  res_row counting_user;
begin
  update "counting_user"
  set
    count_total = coalesce(
      (p_updates->>'count_total')::bigint, 
      count_total
    ),
    count_errors = coalesce(
      (p_updates->>'count_errors')::bigint, 
      count_errors
    ),
    avg_count_reaction_time = coalesce(
      (p_updates->>'avg_count_reaction_time')::bigint, 
      avg_count_reaction_time
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