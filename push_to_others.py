import psycopg2
import random
import datetime

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

# Функция для заполнения таблицы providers
def populate_providers(conn):
    try:
        cursor = conn.cursor()
        providers = []
        for i in range(1, 11):
            name = f'Поставщик #{i}'
            email = f'provider{i}@example.com'
            contact_person = f'Контактное лицо {i}'
            comments = f'Комментарий для поставщика {i}'
            providers.append((name, email, contact_person, comments))
        
        insert_query = """
        INSERT INTO providers (Name, Email, ContactPerson, Comments)
        VALUES (%s, %s, %s, %s) RETURNING ID;
        """
        provider_ids = []
        for provider in providers:
            cursor.execute(insert_query, provider)
            provider_id = cursor.fetchone()[0]
            provider_ids.append(provider_id)
            print(f"Поставщик '{provider[0]}' добавлен с ID {provider_id}.")
        conn.commit()
        cursor.close()
        return provider_ids
    except Exception as e:
        print(f"Ошибка при заполнении таблицы providers: {e}")
        conn.rollback()

# Функция для заполнения таблицы procurementstatuses
def populate_procurementstatuses(conn):
    try:
        cursor = conn.cursor()
        statuses = [
            'Новый',
            'В обработке',
            'Отгружен',
            'Доставлен',
            'Отменен',
            'Ожидает оплаты',
            'Оплачен',
            'Завершен',
            'Возврат',
            'Закрыт'
        ]
        insert_query = """
        INSERT INTO procurementstatuses (Name)
        VALUES (%s) RETURNING ID;
        """
        status_ids = []
        for status in statuses:
            cursor.execute(insert_query, (status,))
            status_id = cursor.fetchone()[0]
            status_ids.append(status_id)
            print(f"Статус закупки '{status}' добавлен с ID {status_id}.")
        conn.commit()
        cursor.close()
        return status_ids
    except Exception as e:
        print(f"Ошибка при заполнении таблицы procurementstatuses: {e}")
        conn.rollback()

# Функция для заполнения таблицы souvenirprocurements
def populate_souvenirprocurements(conn, provider_ids, status_ids):
    try:
        cursor = conn.cursor()
        procurements = []
        for i in range(1, 11):
            id_provider = random.choice(provider_ids)
            date = datetime.date(2023, random.randint(1, 12), random.randint(1, 28))
            id_status = random.choice(status_ids)
            procurements.append((id_provider, date, id_status))
        
        insert_query = """
        INSERT INTO souvenirprocurements (IdProvider, Date, IdStatus)
        VALUES (%s, %s, %s) RETURNING ID;
        """
        procurement_ids = []
        for procurement in procurements:
            cursor.execute(insert_query, procurement)
            procurement_id = cursor.fetchone()[0]
            procurement_ids.append(procurement_id)
            print(f"Закупка добавлена с ID {procurement_id}.")
        conn.commit()
        cursor.close()
        return procurement_ids
    except Exception as e:
        print(f"Ошибка при заполнении таблицы souvenirprocurements: {e}")
        conn.rollback()

# Функция для заполнения таблицы procurementsouvenirs
def populate_procurementsouvenirs(conn, procurement_ids, souvenir_ids):
    try:
        cursor = conn.cursor()
        procurement_souvenirs = []
        for procurement_id in procurement_ids:
            num_items = random.randint(1, 5)
            for _ in range(num_items):
                id_souvenir = random.choice(souvenir_ids)
                amount = random.randint(10, 100)
                price = round(random.uniform(50, 500), 2)
                procurement_souvenirs.append((id_souvenir, procurement_id, amount, price))
        
        insert_query = """
        INSERT INTO procurementsouvenirs (IdSouvenir, IdProcurement, Amount, Price)
        VALUES (%s, %s, %s, %s) RETURNING ID;
        """
        for ps in procurement_souvenirs:
            cursor.execute(insert_query, ps)
            ps_id = cursor.fetchone()[0]
            print(f"Закупленный сувенир добавлен с ID {ps_id}.")
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Ошибка при заполнении таблицы procurementsouvenirs: {e}")
        conn.rollback()

# Функция для заполнения таблицы souvenirstores
def populate_souvenirstores(conn, souvenir_ids, procurement_ids):
    try:
        cursor = conn.cursor()
        store_entries = []
        for id_souvenir in souvenir_ids:
            id_procurement = random.choice(procurement_ids)
            amount = random.randint(10, 100)
            comments = f"Партия товара {id_souvenir}"
            store_entries.append((id_souvenir, id_procurement, amount, comments))
        
        insert_query = """
        INSERT INTO souvenirstores (IdSouvenir, IdProcurement, Amount, Comments)
        VALUES (%s, %s, %s, %s) RETURNING ID;
        """
        for entry in store_entries:
            cursor.execute(insert_query, entry)
            store_id = cursor.fetchone()[0]
            print(f"Запись на складе добавлена с ID {store_id}.")
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Ошибка при заполнении таблицы souvenirstores: {e}")
        conn.rollback()

# Основная функция
def main():
    conn = connect_db(db_config)
    if conn is not None:
        # Предполагается, что таблица souvenirs уже заполнена
        # Получаем список ID существующих сувениров
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM souvenirs;")
        result = cursor.fetchall()
        souvenir_ids = [row[0] for row in result]
        cursor.close()
        
        if not souvenir_ids:
            print("Таблица souvenirs пуста. Пожалуйста, сначала заполните ее.")
            conn.close()
            return

        provider_ids = populate_providers(conn)
        status_ids = populate_procurementstatuses(conn)
        procurement_ids = populate_souvenirprocurements(conn, provider_ids, status_ids)
        populate_procurementsouvenirs(conn, procurement_ids, souvenir_ids)
        populate_souvenirstores(conn, souvenir_ids, procurement_ids)

        conn.close()
        print("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    main()