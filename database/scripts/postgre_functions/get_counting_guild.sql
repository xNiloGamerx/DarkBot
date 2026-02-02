CREATE OR REPLACE FUNCTION get_counting_guild(p_data jsonb)
RETURNS TABLE(
    out_id bigint,
    out_guild_id bigint,
    out_last_counted_number bigint,
    out_last_counted_user_id bigint,
    out_count_checkpoint bigint,
    out_count_points bigint,
    out_created_at timestamptz,
    out_channel_id bigint,
    out_last_counted_at timestamptz
)
SET search_path = public
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        "counting_guild".id, 
        "counting_guild".guild_id, 
        "counting_guild".last_counted_number, 
        "counting_guild".last_counted_user_id, 
        "counting_guild".count_checkpoint, 
        "counting_guild".count_points, 
        "counting_guild".created_at, 
        "counting_guild".channel_id, 
        "counting_guild".last_counted_at 
    FROM "counting_guild"
    INNER JOIN "guild" ON "guild".id = "counting_guild".guild_id
    WHERE "guild".guild_id = p_data->>'guild_id';
END;
$$ LANGUAGE plpgsql;