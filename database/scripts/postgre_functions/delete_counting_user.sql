create or replace function delete_counting_user(p_user_id text, p_guild_id text)
returns jsonb
set search_path = public
as $$
declare
  v_error_msg text;
  v_error_detail text;
begin
  DELETE FROM "counting_user" cu
  USING "user_guild" ug, "user" u, "guild" g
  WHERE cu.user_guild_id = ug.id
    AND ug.user_id = u.id
    AND ug.guild_id = g.id
    AND g.guild_id = '819152506294763520'
    AND u.user_id = '752950649834176622';

  if not found then
    return jsonb_build_object(
      'message', 'Counting User nicht gefunden',
      'result', false,
      'status', 'error'
    );
  end if;

  return jsonb_build_object(
    'message', 'Counting User erfolgreich gelöscht',
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