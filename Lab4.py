import sqlite3
from tabulate import tabulate
from datetime import datetime

DB_PATH = r"C:\Users\user\Desktop\DB"

def connect_db():
    return sqlite3.connect(DB_PATH)

def get_table_relations():
    """Получаем информацию о всех связях между таблицами"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Получаем список всех таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    
    relations = {}
    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        fks = cursor.fetchall()
        relations[table] = []
        for fk in fks:
            relations[table].append({
                'from_column': fk[3],
                'to_table': fk[2],
                'to_column': fk[4]
            })
    
    conn.close()
    return relations

def build_join_query(table_name, limit=5):
    """Строим JOIN-запрос динамически на основе связей"""
    relations = get_table_relations()
    
    # Получаем все столбцы основной таблицы
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    main_columns = [col[1] for col in cursor.fetchall()]
    conn.close()
    
    # Определяем столбцы для SELECT
    select_parts = []
    hidden_columns = set()
    
    # Добавляем столбцы основной таблицы (кроме ID для JOIN)
    for col in main_columns:
        is_fk_column = any(fk['from_column'] == col for fk in relations.get(table_name, []))
        if not is_fk_column:
            select_parts.append(f"{table_name}.{col}")
        else:
            hidden_columns.add(f"{table_name}.{col}")
    
    # Добавляем данные из связанных таблиц
    for fk in relations.get(table_name, []):
        to_table = fk['to_table']
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({to_table});")
        to_columns = [col[1] for col in cursor.fetchall() if col[1] != fk['to_column']]
        conn.close()
        
        for col in to_columns:
            select_parts.append(f"{to_table}.{col} AS '{to_table}_{col}'")
    
    # Собираем JOIN-части
    from_part = f"FROM {table_name}"
    join_parts = []
    for fk in relations.get(table_name, []):
        join_parts.append(
            f"LEFT JOIN {fk['to_table']} ON {table_name}.{fk['from_column']} = {fk['to_table']}.{fk['to_column']}"
        )
    
    query = f"""
        SELECT {', '.join(select_parts)}
        {from_part}
        {' '.join(join_parts)}
        LIMIT ?
    """
    
    return query, hidden_columns

def get_table_data(table_name, limit=5):
    """Получаем данные таблицы с JOIN, скрывая технические ID"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        query, hidden_columns = build_join_query(table_name)
        cursor.execute(query, (limit,))
        
        data = cursor.fetchall()
        headers = []
        
        # Форматируем заголовки, исключая скрытые столбцы
        for description in cursor.description:
            col_name = description[0]
            table_col = f"{description[1]}.{col_name}" if description[1] else col_name
            
            if table_col not in hidden_columns:
                if '_' in col_name and not col_name.endswith('_id'):
                    parts = col_name.split('_')
                    headers.append(f"{parts[0]}:{parts[1]}")
                else:
                    headers.append(col_name)
        
        return headers, data
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return [], []
    finally:
        conn.close()

def show_table_menu(table_name):
    while True:
        headers, data = get_table_data(table_name)
        
        print(f"\nСодержимое таблицы {table_name}:")
        print(tabulate(data, headers=headers, tablefmt="grid"))
        
        print("\nДоступные операции:")
        print("1. Просмотр данных")
        print("2. Добавление данных")
        print("3. Обновление данных")
        print("4. Удаление данных")
        print("5. Вернуться к выбору таблицы")
        
        operation = input("Выберите операцию (1-5): ")
        
        if operation == "1":
            limit = input("Сколько записей показать (по умолчанию 5)? ").strip()
            try:
                headers, data = get_table_data(table_name, int(limit) if limit else 5)
                print(f"\nПоследние {len(data)} записей:")
                print(tabulate(data, headers=headers, tablefmt="grid"))
            except ValueError:
                print("Ошибка: введите целое число!")
        elif operation == "2":
            orig_headers = get_table_columns(table_name)
            print(f"\nДобавление записи в таблицу {table_name}")
            print("Доступные колонки:", ", ".join(orig_headers))
            columns = input("Введите названия колонок через запятую: ").split(',')
            values = input("Введите значения через точку с запятой: ").split(';')
            insert_data(table_name, [col.strip() for col in columns], [val.strip() for val in values])
        elif operation == "3":
            update_data(table_name)
        elif operation == "4":
            delete_data(table_name)
        elif operation == "5":
            return
        else:
            print("\nНеверный выбор операции!")

def get_table_columns(table_name):
    """Получаем список колонок таблицы"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [column[1] for column in cursor.fetchall()]
    conn.close()
    return columns

def insert_data(table_name, columns, values):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        placeholders = ', '.join(['?'] * len(values))
        columns_str = ', '.join(columns)
        cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});", values)
        conn.commit()
        print("\nДанные успешно добавлены!")
    except sqlite3.Error as e:
        print(f"\nОшибка при добавлении данных: {e}")
    finally:
        conn.close()

def update_data(table_name):
    """Обновление данных с поддержкой сложных условий"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Показываем доступные колонки
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [column[1] for column in cursor.fetchall()]
        print("\nДоступные колонки:", ", ".join(columns))
        
        # Запрашиваем колонки для обновления
        update_cols = input("Введите названия колонок для обновления (через запятую): ").split(',')
        new_values = input("Введите новые значения (через точку с запятой): ").split(';')
        
        if len(update_cols) != len(new_values):
            print("Количество колонок и значений не совпадает!")
            return
        
        # Запрашиваем условия WHERE
        print("\nСоздание условий WHERE (оставьте пусто для завершения):")
        conditions = []
        params = []
        
        while True:
            col = input("Колонка для условия: ").strip()
            if not col:
                break
            if col not in columns:
                print(f"Колонка {col} не существует!")
                continue
                
            operator = input("Оператор (=, !=, >, <, LIKE и т.д.): ").strip()
            value = input("Значение: ").strip()
            
            conditions.append(f"{col} {operator} ?")
            params.append(value)
        
        if not conditions:
            print("Необходимо указать хотя бы одно условие!")
            return
        
        # Строим SQL запрос
        set_clause = ", ".join([f"{col.strip()} = ?" for col in update_cols])
        where_clause = " AND ".join(conditions)
        params = [val.strip() for val in new_values] + params
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        
        # Выполняем запрос
        cursor.execute(query, params)
        conn.commit()
        
        print(f"\nОбновлено {cursor.rowcount} записей")
        
    except Exception as e:
        print(f"\nОшибка при обновлении данных: {e}")
    finally:
        conn.close()

def delete_data(table_name):
    """Удаление данных с поддержкой сложных условий"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Показываем доступные колонки
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [column[1] for column in cursor.fetchall()]
        print("\nДоступные колонки:", ", ".join(columns))
        
        # Запрашиваем условия WHERE
        print("\nСоздание условий WHERE (оставьте пусто для завершения):")
        conditions = []
        params = []
        
        while True:
            col = input("Колонка для условия: ").strip()
            if not col:
                break
            if col not in columns:
                print(f"Колонка {col} не существует!")
                continue
                
            operator = input("Оператор (=, !=, >, <, LIKE и т.д.): ").strip()
            value = input("Значение: ").strip()
            
            conditions.append(f"{col} {operator} ?")
            params.append(value)
        
        if not conditions:
            print("Необходимо указать хотя бы одно условие!")
            return
        
        # Строим SQL запрос
        where_clause = " AND ".join(conditions)
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        
        # Показываем какие записи будут удалены
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {where_clause}", params)
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Нет записей, соответствующих условиям")
            return
        
        cursor.execute(f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT 5", params)
        preview = cursor.fetchall()
        
        print(f"\nБудет удалено {count} записей. Примеры:")
        headers = [desc[0] for desc in cursor.description]
        print(tabulate(preview, headers=headers, tablefmt="grid"))
        
        confirm = input("\nВы уверены? (y/n): ").lower()
        if confirm != 'y':
            print("Отменено")
            return
        
        # Выполняем удаление
        cursor.execute(query, params)
        conn.commit()
        
        print(f"\nУдалено {cursor.rowcount} записей")
        
    except Exception as e:
        print(f"\nОшибка при удалении данных: {e}")
    finally:
        conn.close()
def show_analytics_menu():
    """Меню аналитических функций"""
    while True:
        print("\nАналитические функции:")
        print("1. Анализ транзакций за период")
        print("2. Статистика по клиентским сегментам")
        print("3. Анализ активности клиентов")  # Новая функция
        print("4. Вернуться в главное меню")
        
        choice = input("Выберите функцию (1-4): ")
        
        if choice == "1":
            analyze_transactions_by_period()
        elif choice == "2":
            analyze_client_segments()
        elif choice == "3":
            analyze_client_activity()  # Вызов новой функции
        elif choice == "4":
            return
        else:
            print("Неверный выбор!")
def analyze_client_activity():
    """Анализ активности клиентов по операциям"""
    print("\nАнализ активности клиентов")
    
    # Запрос параметров у пользователя
    start_date = input("Начальная дата (ГГГГ-ММ-ДД, пусто - без ограничений): ").strip()
    end_date = input("Конечная дата (ГГГГ-ММ-ДД, пусто - без ограничений): ").strip()
    
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # 1. Топ клиентов по количеству операций
        print("\nТоп 5 клиентов по количеству операций:")
        query = """
            SELECT 
                c.LastName || ' ' || c.Name AS Client,
                c.Segment,
                COUNT(t.id) AS TransactionCount,
                SUM(t.Amount) AS TotalAmount,
                AVG(t.Amount) AS AvgAmount
            FROM Transactions t
            JOIN Accounts a ON t.Account_id = a.id
            JOIN Clients c ON a.Client_ID = c.id
        """
        params = []
        
        # Добавляем условия по датам если они указаны
        where_clause = []
        if start_date:
            where_clause.append("date(t.Transaction_datetime) >= ?")
            params.append(start_date)
        if end_date:
            where_clause.append("date(t.Transaction_datetime) <= ?")
            params.append(end_date)
            
        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)
            
        query += """
            GROUP BY c.id
            ORDER BY TransactionCount DESC
            LIMIT 5
        """
        
        cursor.execute(query, params)
        top_clients = cursor.fetchall()
        
        headers = ["Клиент", "Сегмент", "Операций", "Общая сумма", "Ср. сумма"]
        print(tabulate(top_clients, headers=headers, tablefmt="grid", floatfmt=".2f"))
    except Exception as e:
        print(f"Ошибка при выполнении анализа: {e}")
    finally:
        if conn:
            conn.close()
            
def analyze_transactions_by_period():
    """Анализ транзакций за выбранный период"""
    print("\nАнализ транзакций за период")
    
    # Запрос параметров у пользователя
    start_date = input("Введите начальную дату (ГГГГ-ММ-ДД): ")
    end_date = input("Введите конечную дату (ГГГГ-ММ-ДД): ")
    transaction_type = input("Введите тип транзакции (оставьте пустым для всех): ")
    
    conn = None  # Инициализируем conn как None
    try:
        # Проверка дат
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
        
        conn = connect_db()
        cursor = conn.cursor()
        
        # Строим запрос в зависимости от введенных параметров
        query = """
            SELECT 
                strftime('%Y-%m', Transaction_datetime) AS Month,
                Transaction_type,
                COUNT(*) AS Transaction_Count,
                SUM(Amount) AS Total_Amount,
                AVG(Amount) AS Avg_Amount
            FROM Transactions
            WHERE date(Transaction_datetime) BETWEEN ? AND ?
        """
        params = [start_date, end_date]
        
        if transaction_type:
            query += " AND Transaction_type = ?"
            params.append(transaction_type)
        
        query += """
            GROUP BY strftime('%Y-%m', Transaction_datetime), Transaction_type
            ORDER BY Month, Transaction_type
        """
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        if not results:
            print("\nНет данных за указанный период")
            return
        
        headers = ["Месяц", "Тип транзакции", "Количество", "Общая сумма", "Средняя сумма"]
        print("\nРезультаты анализа:")
        print(tabulate(results, headers=headers, tablefmt="grid", floatfmt=".2f"))
        
        # Дополнительная аналитика
        cursor.execute("""
            SELECT 
                COUNT(*) AS Total_Transactions,
                SUM(Amount) AS Grand_Total,
                AVG(Amount) AS Overall_Avg
            FROM Transactions
            WHERE date(Transaction_datetime) BETWEEN ? AND ?
        """, [start_date, end_date])
        totals = cursor.fetchone()
        
        print("\nИтого за период:")
        print(f"Всего транзакций: {totals[0]}")
        print(f"Общая сумма: {totals[1]:.2f}")
        print(f"Средняя сумма транзакции: {totals[2]:.2f}")
        
    except ValueError as e:
        print(f"Ошибка формата даты или числового параметра: {e}")
    except Exception as e:
        print(f"Ошибка при выполнении анализа: {e}")
    finally:
        if conn:  # Закрываем соединение только если оно было установлено
            conn.close()

def analyze_client_segments():
    """Анализ клиентов по сегментам"""
    print("\nАнализ клиентов по сегментам")
    
    # Запрос параметров у пользователя
    min_age = input("Минимальный возраст (оставьте пустым для всех): ")
    max_age = input("Максимальный возраст (оставьте пустым для всех): ")
    city_filter = input("Фильтр по городу (оставьте пустым для всех): ")
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Базовый запрос
        query = """
            SELECT 
                c.Segment,
                COUNT(*) AS Client_Count,
                AVG(c.Age) AS Avg_Age,
                COUNT(DISTINCT a.id) AS Avg_Accounts_Per_Client,
                COUNT(DISTINCT d.ID) AS Avg_Deposits_Per_Client,
                COUNT(DISTINCT l.id) AS Avg_Loans_Per_Client
            FROM Clients c
            LEFT JOIN Accounts a ON c.id = a.Client_ID
            LEFT JOIN Deposits d ON c.id = d.Client_ID
            LEFT JOIN Loans l ON c.id = l.Client_ID
            LEFT JOIN Cities ct ON c.ID_City = ct.id
        """
        
        where_clauses = []
        params = []
        
        # Добавляем условия фильтрации
        if min_age:
            where_clauses.append("c.Age >= ?")
            params.append(int(min_age))
        if max_age:
            where_clauses.append("c.Age <= ?")
            params.append(int(max_age))
        if city_filter:
            where_clauses.append("ct.City LIKE ?")
            params.append(f"%{city_filter}%")
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += """
            GROUP BY c.Segment
            ORDER BY Client_Count DESC
        """
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        if not results:
            print("\nНет данных по указанным критериям")
            return
        
        headers = ["Сегмент", "Кол-во клиентов", "Ср. возраст", "Ср. счетов", "Ср. вкладов", "Ср. кредитов"]
        print("\nСтатистика по сегментам:")
        print(tabulate(results, headers=headers, tablefmt="grid", floatfmt=".1f"))
        
        # Дополнительная аналитика
        cursor.execute("""
            SELECT COUNT(DISTINCT id) FROM Clients
        """)
        total_clients = cursor.fetchone()[0]
        
        print(f"\nВсего клиентов в базе: {total_clients}")
        
    except ValueError:
        print("Ошибка ввода числовых параметров!")
    except Exception as e:
        print(f"Ошибка при выполнении анализа: {e}")
    finally:
        conn.close()
        
def main():
    while True:
        print("\nГлавное меню:")
        print("1. Работа с таблицами")
        print("2. Аналитические функции")
        print("3. Выход")
        
        choice = input("Выберите действие (1-3): ")
        
        if choice == "1":
            tables = get_tables()
            
            print("\nДоступные таблицы:")
            for i, table in enumerate(tables, 1):
                print(f"{i}. {table}")
            print(f"{len(tables)+1}. Назад")
            
            try:
                table_choice = input(f"\nВведите номер таблицы (1-{len(tables)}) или {len(tables)+1} для возврата: ")
                
                if table_choice == str(len(tables)+1):
                    continue
                
                table_num = int(table_choice) - 1
                if 0 <= table_num < len(tables):
                    table_name = tables[table_num]
                    show_table_menu(table_name)
                else:
                    print("\nНеверный номер таблицы!")
            except ValueError:
                print("\nОшибка ввода! Введите число.")
        
        elif choice == "2":
            show_analytics_menu()
        elif choice == "3":
            print("\nВыход из программы...")
            break
        else:
            print("Неверный выбор!")

def get_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    return tables

if __name__ == "__main__":
    main()
