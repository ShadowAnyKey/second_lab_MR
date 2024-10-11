import psycopg2

# Параметры подключения к базе данных
db_config = {
    'host': 'localhost',
    'port': '5433',
    'database': 'LR2DataBase',
    'user': 'postgres',
    'password': 'admin'
}

# Функция для подключения к базе данных
def connect_db(config):
    try:
        conn = psycopg2.connect(**config)
        print("Соединение с базой данных установлено")
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None
conn = connect_db(db_config)

# Функция для чтения файла categories.txt и вставки данных в базу
def import_categories(file_path, conn):
    try:
        cursor = conn.cursor()

        with open(file_path, 'r', encoding='utf-8') as file:
            next(file)  # Пропускаем заголовок
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Пропускаем пустые строки

                parts = line.split(',')
                if len(parts) < 3:
                    print(f"Неверный формат строки: {line}")
                    continue

                category_id = int(parts[0])
                parent_id = parts[1] if parts[1] else None
                if parent_id is not None:
                    parent_id = int(parent_id)
                name = parts[2]

                # Вставка данных в таблицу souvenirscategories
                insert_query = """
                INSERT INTO souvenirscategories (ID, IdParent, Name)
                VALUES (%s, %s, %s)
                ON CONFLICT (ID) DO NOTHING;
                """

                cursor.execute(insert_query, (category_id, parent_id, name))
                print(f"Категория '{name}' (ID: {category_id}) успешно добавлена.")

        # Фиксируем транзакцию
        conn.commit()
        cursor.close()
        print("Импорт категорий завершен.")

        # Обновляем последовательность ID
        update_sequence_query = """
        SELECT setval('souvenirscategories_id_seq', (SELECT MAX(ID) FROM souvenirscategories));
        """
        cursor = conn.cursor()
        cursor.execute(update_sequence_query)
        conn.commit()
        cursor.close()
        print("Последовательность ID обновлена.")

    except Exception as e:
        print(f"Ошибка при импорте категорий: {e}")
        conn.rollback()

# Основная функция
def main():
    conn = connect_db(db_config)
    if conn is not None:
        import_categories('categories.txt', conn)
        conn.close()
        print("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    main()