CREATE OR REPLACE FUNCTION get_category_tree(selected_category_id BIGINT)
RETURNS TABLE (
    id BIGINT,
    idparent BIGINT,
    name VARCHAR,
    level INTEGER
) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE CategoryTree AS (
        -- Начальный запрос
        SELECT
            sc.ID,
            sc.IdParent,
            sc.Name,
            0 AS Level
        FROM
            souvenirscategories sc
        WHERE
            sc.ID = selected_category_id

        UNION ALL

        -- Рекурсивный запрос
        SELECT
            sc.ID,
            sc.IdParent,
            sc.Name,
            ct.Level + 1 AS Level
        FROM
            souvenirscategories sc
            INNER JOIN CategoryTree ct ON sc.IdParent = ct.ID
    )
    SELECT
        ct.ID,
        ct.IdParent,
        ct.Name,
        ct.Level
    FROM
        CategoryTree ct
    ORDER BY
        ct.Level, ct.Name;
END; $$
LANGUAGE plpgsql;