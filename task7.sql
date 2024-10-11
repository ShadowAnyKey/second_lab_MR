CREATE OR REPLACE FUNCTION check_souvenirs_categories()
RETURNS TABLE (
    category_id BIGINT,
    issue TEXT
) AS $$
DECLARE
    rec RECORD;
    visited_ids BIGINT[];
    current_id BIGINT;
BEGIN
    -- Проверка обязательного поля Name
    FOR rec IN
        SELECT ID
        FROM SouvenirsCategories
        WHERE Name IS NULL OR TRIM(Name) = ''
    LOOP
        RETURN QUERY SELECT rec.ID, 'Отсутствует или пустое имя категории';
    END LOOP;

    -- Проверка существования родительской категории
    FOR rec IN
        SELECT sc.ID, sc.IdParent
        FROM SouvenirsCategories sc
        WHERE sc.IdParent IS NOT NULL
          AND NOT EXISTS (SELECT 1 FROM SouvenirsCategories WHERE ID = sc.IdParent)
    LOOP
        RETURN QUERY SELECT rec.ID, 'Некорректный IdParent: ' || rec.IdParent;
    END LOOP;

    -- Проверка на циклы в иерархии категорий
    FOR rec IN SELECT ID FROM SouvenirsCategories LOOP
        visited_ids := ARRAY[rec.ID];
        current_id := (SELECT IdParent FROM SouvenirsCategories WHERE ID = rec.ID);

        WHILE current_id IS NOT NULL LOOP
            IF current_id = rec.ID OR current_id = ANY(visited_ids) THEN
                RETURN QUERY SELECT rec.ID, 'Обнаружен цикл в иерархии категорий';
                EXIT;
            END IF;
            visited_ids := visited_ids || current_id;
            SELECT IdParent INTO current_id FROM SouvenirsCategories WHERE ID = current_id;
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;