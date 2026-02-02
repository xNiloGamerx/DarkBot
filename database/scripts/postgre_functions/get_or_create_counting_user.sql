CREATE OR REPLACE FUNCTION get_or_create_counting_user(p_data jsonb)
RETURNS TABLE(
    out_id bigint,
    out_count_total bigint,
    out_count_errors bigint,
    out_avg_count_reaction_time bigint,
    out_count_points bigint,
    out_last_counted_at timestamptz,
    out_created_at timestamptz,
    out_user_guild_id bigint
)
SET search_path = public
AS $$
DECLARE
    res_user_guild_id bigint;
BEGIN
    -- 1. Bestimme die user_guild_id
    SELECT ug.id
    INTO res_user_guild_id
    FROM "user_guild" ug
    INNER JOIN "user" u ON u.id = ug.user_id
    INNER JOIN "guild" g ON g.id = ug.guild_id
    WHERE u.user_id = p_data->>'user_id'
      AND g.guild_id = p_data->>'guild_id';

    -- 2. Versuche, den counting_user einzufügen
    RETURN QUERY
    INSERT INTO counting_user(user_guild_id)
    VALUES (res_user_guild_id)
    ON CONFLICT (user_guild_id) DO NOTHING
    RETURNING 
        id, 
        count_total, 
        count_errors, 
        avg_count_reaction_time, 
        count_points, 
        last_counted_at, 
        created_at, 
        counting_user.user_guild_id;

    -- 3. Wenn kein Insert passiert ist (FOUND ist false), existiert er schon
    IF NOT FOUND THEN
        RETURN QUERY
        SELECT 
            id, 
            count_total, 
            count_errors, 
            avg_count_reaction_time, 
            count_points, 
            last_counted_at, 
            created_at, 
            user_guild_id
        FROM counting_user
        WHERE user_guild_id = res_user_guild_id;
    END IF;
END;
$$ LANGUAGE plpgsql;