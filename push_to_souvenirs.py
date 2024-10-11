import psycopg2
import pandas as pd
import numpy as np

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

# Функция для импорта данных из data.xlsx
def import_data(file_path, conn):
    try:
        cursor = conn.cursor()

        # Читаем Excel-файл
        df = pd.read_excel(file_path)

        # Заполняем отсутствующие значения None
        df = df.replace({np.nan: None})

        # 1. Обработка справочников
        ## a. Colors
        unique_colors = df['color'].dropna().unique()
        color_id_map = {}
        for color in unique_colors:
            # Проверяем, существует ли уже такой цвет в таблице
            cursor.execute("SELECT ID FROM colors WHERE name = %s;", (color,))
            result = cursor.fetchone()
            if result:
                color_id = result[0]
            else:
                # Вставляем новый цвет
                cursor.execute("INSERT INTO colors (name) VALUES (%s) RETURNING ID;", (color,))
                color_id = cursor.fetchone()[0]
            color_id_map[color] = color_id

        ## b. SouvenirMaterials
        unique_materials = df['material'].dropna().unique()
        material_id_map = {}
        for material in unique_materials:
            cursor.execute("SELECT ID FROM souvenirmaterials WHERE name = %s;", (material,))
            result = cursor.fetchone()
            if result:
                material_id = result[0]
            else:
                cursor.execute("INSERT INTO souvenirmaterials (name) VALUES (%s) RETURNING ID;", (material,))
                material_id = cursor.fetchone()[0]
            material_id_map[material] = material_id

        ## c. ApplicationMethods
        unique_methods = df['applicMetod'].dropna().unique()
        method_id_map = {}
        for method in unique_methods:
            cursor.execute("SELECT ID FROM applicationmethods WHERE name = %s;", (method,))
            result = cursor.fetchone()
            if result:
                method_id = result[0]
            else:
                cursor.execute("INSERT INTO applicationmethods (name) VALUES (%s) RETURNING ID;", (method,))
                method_id = cursor.fetchone()[0]
            method_id_map[method] = method_id

        # Фиксируем вставку в справочники
        conn.commit()

        # Список обязательных полей
        required_fields = ['url', 'shortname', 'name', 'description', 'rating', 'categoryid',
                           'color', 'prodsize', 'material', 'applicMetod', 'fullCategories', 'dealerPrice', 'price']

        # 2. Обработка основной таблицы Souvenirs
        skipped_records = 0
        for index, row in df.iterrows():
            # Проверка обязательных полей
            missing_fields = [field for field in required_fields if row[field] is None]
            if missing_fields:
                print(f"Запись на строке {index + 2} пропущена из-за отсутствия обязательных полей: {', '.join(missing_fields)}")
                skipped_records += 1
                continue

            # Получаем значения для внешних ключей
            color = row['color']
            material = row['material']
            applic_method = row['applicMetod']
            category_id = row['categoryid']

            # Проверяем, существует ли категория с таким ID
            cursor.execute("SELECT ID FROM souvenirscategories WHERE ID = %s;", (category_id,))
            if not cursor.fetchone():
                print(f"Категория с ID {category_id} не найдена. Создаем новую запись.")
                cursor.execute("INSERT INTO souvenirscategories (ID, IdParent, Name) VALUES (%s, NULL, 'Неизвестная категория');", (category_id,))

            # Получаем идентификаторы из справочников
            id_color = color_id_map.get(color)
            id_material = material_id_map.get(material)
            id_applic_method = method_id_map.get(applic_method)

            # Проверка отсутствия None в идентификаторах внешних ключей
            if None in [id_color, id_material, id_applic_method]:
                print(f"Запись на строке {index + 2} пропущена из-за отсутствия данных в справочниках.")
                skipped_records += 1
                continue

            # Подготовка данных для вставки
            insert_data = (
                row['url'],
                row['shortname'],
                row['name'],
                row['description'],
                int(row['rating']) if row['rating'] is not None else 0,
                category_id,
                id_color,
                row['prodsize'],
                id_material,
                row['weight'],
                row['qtypics'],
                row['picssize'],
                id_applic_method,
                row['fullCategories'],
                row['dealerPrice'],
                row['price'],
                None  # Comments
            )

            # Вставка данных в таблицу Souvenirs
            insert_query = """
            INSERT INTO souvenirs (
                URL, ShortName, Name, Description, Rating, IdCategory, IdColor, Size, 
                IdMaterial, Weight, QTypics, PicsSize, IdApplicMetod, AllCategories, 
                DealerPrice, Price, Comments
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING ID;
            """
            cursor.execute(insert_query, insert_data)
            souvenir_id = cursor.fetchone()[0]
            print(f"Сувенир '{row['name']}' (ID: {souvenir_id}) успешно добавлен.")

        # Фиксируем вставку сувениров
        conn.commit()
        cursor.close()
        print("Импорт данных завершен.")
        print(f"Всего пропущено записей: {skipped_records}")

        # Обновляем последовательности
        update_sequences = [
            "SELECT setval('colors_id_seq', (SELECT MAX(ID) FROM colors));",
            "SELECT setval('souvenirmaterials_id_seq', (SELECT MAX(ID) FROM souvenirmaterials));",
            "SELECT setval('applicationmethods_id_seq', (SELECT MAX(ID) FROM applicationmethods));",
            "SELECT setval('souvenirs_id_seq', (SELECT MAX(ID) FROM souvenirs));",
            "SELECT setval('souvenirscategories_id_seq', (SELECT MAX(ID) FROM souvenirscategories));"
        ]
        cursor = conn.cursor()
        for query in update_sequences:
            cursor.execute(query)
        conn.commit()
        cursor.close()
        print("Последовательности обновлены.")

    except Exception as e:
        print(f"Ошибка при импорте данных: {e}")
        conn.rollback()

# Основная функция
def main():
    conn = connect_db(db_config)
    if conn is not None:
        import_data('data.xlsx', conn)
        conn.close()
        print("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    main()