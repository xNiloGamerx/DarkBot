create or replace function delete_user(p_user_id text)
returns jsonb
set search_path = public
as $$
declare
  v_error_msg text;
  v_error_detail text;
begin
  delete
  from "user"
  where user_id = p_user_id;

  if not found then
    return jsonb_build_object(
      'message', 'User nicht gefunden',
      'result', false,
      'status', 'error'
    );
  end if;

  return jsonb_build_object(
    'message', 'User erfolgreich gelöscht',
    'result', true,
    'status', 'ok',
    'id', p_user_id
  );

  exception when others then
    -- Fängt alle Fehler ab (z.B. Foreign Key Constraints)
    get stacked diagnostics 
      v_error_msg = message_text,
      v_error_detail = pg_exception_detail;

    return jsonb_build_object(
      'message', 'Interner Datenbankfehler',
      'result', false,
      'status', 'error',
      'error_details', v_error_msg
    );
end;
$$ language plpgsql;