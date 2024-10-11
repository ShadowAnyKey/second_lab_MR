--Первым делом, создаём таблицу, в которую мы запишем уведомления
CREATE TABLE user_notifications (
    ID SERIAL PRIMARY KEY,
    NotificationDate TIMESTAMP DEFAULT NOW(),
    Message TEXT NOT NULL,
    IsRead BOOLEAN DEFAULT FALSE
);

--Создаём функцию триггер
CREATE OR REPLACE FUNCTION fn_trigger_low_stock()
RETURNS TRIGGER AS $$
DECLARE
    current_stock INTEGER;
    has_procurements BOOLEAN;
    souvenir_name VARCHAR;
BEGIN
    -- Получаем общее количество товара на складе
    SELECT SUM(Amount) INTO current_stock
    FROM souvenirstores
    WHERE IdSouvenir = NEW.IdSouvenir;

    -- Если количество NULL, то устанавливаем в 0
    current_stock := COALESCE(current_stock, 0);

    -- Проверяем, есть ли запланированные поставки для этого товара
    SELECT EXISTS (
        SELECT 1
        FROM procurementsouvenirs psu
        JOIN souvenirprocurements sp ON psu.IdProcurement = sp.ID
        JOIN procurementstatuses pst ON sp.IdStatus = pst.ID
        WHERE psu.IdSouvenir = NEW.IdSouvenir
          AND pst.Name IN ('Новый', 'В обработке')
    ) INTO has_procurements;

    -- Получаем название сувенира
    SELECT Name INTO souvenir_name
    FROM souvenirs
    WHERE ID = NEW.IdSouvenir;

    -- Если количество меньше 50 и нет запланированных поставок
    IF current_stock < 50 AND NOT has_procurements THEN
        INSERT INTO user_notifications (Message)
        VALUES (
            FORMAT(
                'Сувенир "%s" (ID: %s) имеет низкий остаток (%s шт.) и нет запланированных поставок.',
                souvenir_name,
                NEW.IdSouvenir,
                current_stock
            )
        );
    END IF;

    RETURN NULL; -- Для триггеров AFTER можно возвращать NULL
END;
$$ LANGUAGE plpgsql;

--Создаём триггер, который мы прикрепляем к триггер функции
CREATE TRIGGER trg_low_stock
AFTER INSERT OR UPDATE ON souvenirstores
FOR EACH ROW
EXECUTE FUNCTION fn_trigger_low_stock();

--Проверка для нашего триггера
UPDATE souvenirstores
SET Amount = 45
WHERE IdSouvenir = 1;