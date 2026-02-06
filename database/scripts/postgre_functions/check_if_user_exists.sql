create or replace function check_if_user_exists(p_user_id text)
returns jsonb
set search_path = public
as $$
begin
  perform id
  from "user"
  where user_id = p_user_id;

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
