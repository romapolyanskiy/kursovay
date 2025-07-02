drop table if exists Cities;
drop table if exists Clients;
drop table if exists Deposits;
drop table if exists Transactions;
drop table if exists Cards;
drop table if exists Accounts;
drop table if exists Loans;
drop table if exists Employees;
drop table if exists Chats;
drop table if exists Calls;

CREATE TABLE Cities (
    id INTEGER PRIMARY KEY,
    City VARCHAR NOT NULL,
    Region VARCHAR  NOT NULL,
    District VARCHAR NOT NULL
);

CREATE TABLE Clients (
    id INTEGER PRIMARY KEY,
    LastName TEXT,
    Name TEXT,
    FatherName TEXT,
    Sex TEXT,
    Age INTEGER,
    Segment VARCHAR,
    PhoneNumber VARCHAR  NOT NULL,
    Email VARCHAR,
    ID_City INTEGER,
    Birthdate DATETIME,
    FOREIGN KEY (ID_City) REFERENCES Cities(id)
);

CREATE TABLE Deposits (
    ID INTEGER PRIMARY KEY,
    Client_ID INTEGER,
    Amount FLOAT NOT NULL,
    Term_days INTEGER NOT NULL,
    Interest_rate INTEGER NOT NULL,
    Opening_date DATETIME NOT NULL,
    FOREIGN KEY (Client_ID) REFERENCES Clients(id)
);

CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY,
    Transaction_type VARCHAR NOT NULL,
    Amount FLOAT NOT NULL,
    Transaction_datetime DATETIME NOT NULL,
    Account_id integer NOT NULL,
    FOREIGN KEY (Account_id) REFERENCES Accounts(id)
);

CREATE TABLE Cards (
    id INTEGER PRIMARY KEY,
    Card_type VARCHAR NOT NULL,
    Balance FLOAT,
    Credit_limit INTEGER,
    Debt FLOAT,
    Next_payment_date DATETIME,
    Is_overdue BOOLEAN,
    Account_id integer,
    FOREIGN KEY (Account_id) REFERENCES Accounts(id)
);

CREATE TABLE Accounts (
    id INTEGER PRIMARY KEY,
    Client_ID INTEGER,
    Account_type VARCHAR NOT NULL,
    Balance FLOAT,
    Debt FLOAT,
    Account_number INTEGER NOT NULL,
    FOREIGN KEY (Client_ID) REFERENCES Clients(id)
);

CREATE TABLE Loans (
    id INTEGER PRIMARY KEY,
    Client_ID INTEGER NOT NULL,
    Amount FLOAT,
    Term_days INTEGER,
    Issue_date DATETIME,
    Interest_rate INTEGER,
    Remaining_debt FLOAT,
    Next_payment_date DATETIME,
    Is_overdue BOOLEAN,
    FOREIGN KEY (Client_ID) REFERENCES Clients(id)
);

CREATE TABLE Employees (
    id INTEGER PRIMARY KEY,
    Last_name VARCHAR NOT NULL,
    First_name VARCHAR NOT NULL,
    Middle_name VARCHAR,
    Birth_date DATETIME,
    Position VARCHAR NOT NULL,
    Department VARCHAR NOT NULL,
    Gender varchar,
    City_id INTEGER,
    FOREIGN KEY (City_id) REFERENCES Cities(id),
    CHECK (Gender IN ('М','Ж'))
);

CREATE TABLE Chats (
    id INTEGER PRIMARY KEY,
    Client_ID INTEGER NOT NULL,
    Employee_ID INTEGER NOT NULL,
    Product varchar,
    Offer_number INTEGER,
    Start_datetime DATETIME NOT NULL,
    End_datetime DATETIME,
    Result varchar,
    FOREIGN KEY (Client_ID) REFERENCES Clients(id),
    FOREIGN KEY (Employee_ID) REFERENCES Employees(id),
    CHECK (Start_datetime <= End_datetime)
);

CREATE TABLE Calls (
    id INTEGER PRIMARY KEY,
    Product varchar,
    Start_datetime DATETIME NOT NULL,
    End_datetime DATETIME,
    Client_ID INTEGER NOT NULL,
    Employee_ID INTEGER NOT NULL,
    Offer_number INTEGER,
    Result varchar,
    FOREIGN KEY (Client_ID) REFERENCES Clients(id),
    FOREIGN KEY (Employee_ID) REFERENCES Employees(id),
    CHECK (Start_datetime <= End_datetime)
);


INSERT INTO Calls (id, Product, Start_datetime, End_datetime, Client_ID, Employee_ID, Offer_number, Result) VALUES
(1, 'Кредиты', '2025-05-01 09:00:00', '2025-05-01 09:10:00', 1, 1, 1001, 1),
(2, 'КК', '2025-05-02 10:30:00', '2025-05-02 10:45:00', 2, 2, 1002, 1),
(3, 'НС', '2025-05-03 13:20:00', '2025-05-03 13:35:00', 3, 3, 1003, 0),
(4, 'Кредиты', '2025-05-04 15:10:00', '2025-05-04 15:20:00', 4, 4, 1004, 1),
(5, 'КК', '2025-05-05 08:15:00', '2025-05-05 08:25:00', 5, 5, 1005, 2),
(6, 'НС', '2025-05-06 12:40:00', '2025-05-06 12:55:00', 6, 6, 1006, 1),
(7, 'Кредиты', '2025-05-07 14:20:00', '2025-05-07 14:30:00', 7, 7, 1007, 0),
(8, 'КК', '2025-05-08 09:50:00', '2025-05-08 10:00:00', 8, 8, 1008, 1),
(9, 'НС', '2025-05-09 11:30:00', '2025-05-09 11:40:00', 9, 9, 1009, 2),
(10, 'Кредиты', '2025-05-10 16:00:00', '2025-05-10 16:10:00', 10, 10, 1010, 1);
INSERT INTO Chats (id, Client_ID, Employee_ID, Product, Offer_number, Start_datetime, End_datetime, Result) VALUES
(1, 1, 1, 'НС', 1001, '2025-05-01 10:00:00', '2025-05-01 10:15:00', 1),
(2, 2, 2, 'КК', 1002, '2025-05-02 11:30:00', '2025-05-02 11:45:00', 1),
(3, 3, 3, 'Кредиты', 1003, '2025-05-03 14:20:00', '2025-05-03 14:50:00', 0),
(4, 4, 4, 'НС', 1004, '2025-05-04 16:10:00', '2025-05-04 16:25:00', 1),
(5, 5, 5, 'Кредиты', 1005, '2025-05-05 09:15:00', '2025-05-05 09:30:00', 2),
(6, 6, 6, 'КК', 1006, '2025-05-06 13:40:00', '2025-05-06 14:10:00', 1),
(7, 7, 7, 'КК', 1007, '2025-05-07 15:20:00', '2025-05-07 15:35:00', 0),
(8, 8, 8, 'Кредиты', 1008, '2025-05-08 10:50:00', '2025-05-08 11:05:00', 1),
(9, 9, 9, 'НС', 1009, '2025-05-09 12:30:00', '2025-05-09 12:45:00', 2),
(10, 10, 10, 'НС', 1010, '2025-05-10 17:00:00', '2025-05-10 17:15:00', 1);
INSERT INTO Employees (id, Last_name, First_name, Middle_name, Birth_date, Position, Department, Gender, City_id) VALUES
(1, 'Смирнов', 'Александр', 'Игоревич', '1991-02-18', 'Менеджер', 'Кредитный отдел', 'М', 1),
(2, 'Ковалева', 'Екатерина', 'Сергеевна', '1995-05-25', 'Специалист', 'Отдел вкладов', 'Ж', 2),
(3, 'Попов', 'Дмитрий', 'Анатольевич', '1988-08-12', 'Руководитель', 'Операционный отдел', 'М', 3),
(4, 'Лебедева', 'Ольга', 'Владимировна', '1993-03-30', 'Консультант', 'Клиентский сервис', 'Ж', 4),
(5, 'Новиков', 'Максим', 'Алексеевич', '1994-07-22', 'Аналитик', 'Аналитический отдел', 'М', 5),
(6, 'Волкова', 'Ирина', 'Дмитриевна', '1996-09-15', 'Менеджер', 'Кредитный отдел', 'Ж', 6),
(7, 'Козлов', 'Андрей', 'Сергеевич', '1983-04-05', 'Директор', 'Управление', 'М', 7),
(8, 'Соколова', 'Наталья', 'Викторовна', '1992-11-28', 'Специалист', 'Отдел вкладов', 'Ж', 8),
(9, 'Морозов', 'Иван', 'Петрович', '1990-01-17', 'Консультант', 'Клиентский сервис', 'М', 9),
(10, 'Зайцева', 'Марина', 'Андреевна', '1997-06-09', 'Ассистент', 'Операционный отдел', 'Ж', 10);
INSERT INTO Loans (id, Client_ID, Amount, Term_days, Issue_date, Interest_rate, Remaining_debt, Next_payment_date, Is_overdue) VALUES
(1, 1, 300000.00, 730, '2025-01-10', 12, 280000.00, '2025-06-10', 0),
(2, 2, 150000.00, 365, '2025-02-15', 15, 135000.00, '2025-06-15', 0),
(3, 3, 500000.00, 1095, '2025-03-20', 10, 480000.00, '2025-06-20', 0),
(4, 4, 100000.00, 365, '2025-04-05', 14, 95000.00, '2025-06-05', 0),
(5, 5, 200000.00, 730, '2025-01-25', 11, 185000.00, '2025-06-25', 0),
(6, 6, 75000.00, 180, '2025-05-10', 16, 70000.00, '2025-06-10', 0),
(7, 7, 400000.00, 1095, '2025-03-15', 9, 390000.00, '2025-06-15', 0),
(8, 8, 50000.00, 365, '2025-06-01', 17, 50000.00, '2025-07-01', 0),
(9, 9, 250000.00, 730, '2025-02-20', 12, 240000.00, '2025-06-20', 0),
(10, 10, 180000.00, 365, '2025-04-10', 13, 170000.00, '2025-06-10', 0);
INSERT INTO Accounts (id, Client_ID, Account_type, Balance, Debt, Account_number) VALUES
(1, 1, 'Расчетный', 150000.00, 0.00, 1001001),
(2, 2, 'Кредитный', 50000.00, 25000.00, 1001002),
(3, 3, 'Накопительный', 750000.00, 0.00, 1001003),
(4, 4, 'Расчетный', 80000.00, 0.00, 1001004),
(5, 5, 'Кредитный', 120000.00, 50000.00, 1001005),
(6, 6, 'Накопительный', 200000.00, 0.00, 1001006),
(7, 7, 'Расчетный', 350000.00, 0.00, 1001007),
(8, 8, 'Кредитный', 30000.00, 15000.00, 1001008),
(9, 9, 'Накопительный', 500000.00, 0.00, 1001009),
(10, 10, 'Расчетный', 180000.00, 0.00, 1001010);
INSERT INTO Cards (id, Card_type, Balance, Credit_limit, Debt, Next_payment_date, Is_overdue,Account_id) VALUES
(101, 'Дебетовая', 150000.00, 0, 0.00, NULL, 0,1),
(102, 'Кредитная', 50000.00, 100000, 25000.00, '2025-06-15', 0,2),
(103, 'Премиальная', 750000.00, 500000, 0.00, NULL, 0,3),
(104, 'Дебетовая', 80000.00, 0, 0.00, NULL, 0,4),
(105, 'Кредитная', 120000.00, 200000, 50000.00, '2025-06-20', 0,5),
(106, 'Дебетовая', 200000.00, 0, 0.00, NULL, 0,6),
(107, 'Премиальная', 350000.00, 300000, 0.00, NULL, 0,7),
(108, 'Кредитная', 30000.00, 50000, 15000.00, '2025-06-10', 1,8),
(109, 'Дебетовая', 500000.00, 0, 0.00, NULL, 0,9),
(110, 'Кредитная', 180000.00, 250000, 0.00, '2025-06-25', 0,10);
INSERT INTO Transactions (id, Transaction_type, Amount, Transaction_datetime,Account_id) VALUES
(1, 'Пополнение', 50000.00, '2025-05-15 12:30:00',1),
(2, 'Снятие', 10000.00, '2025-05-16 15:45:00',2),
(3, 'Перевод', 25000.00, '2025-05-17 09:20:00',3),
(4, 'Пополнение', 15000.00, '2025-05-18 11:15:00',4),
(5, 'Снятие', 30000.00, '2025-05-19 14:25:00',5),
(6, 'Перевод', 18000.00, '2025-05-20 16:40:00',6),
(7, 'Пополнение', 70000.00, '2025-05-21 10:10:00',7),
(8, 'Снятие', 5000.00, '2025-05-22 13:55:00',8),
(9, 'Перевод', 35000.00, '2025-05-23 17:30:00',9),
(10, 'Пополнение', 45000.00, '2025-05-24 09:45:00',10);
INSERT INTO Deposits (ID, Client_ID, Amount, Term_days, Interest_rate, Opening_date) VALUES
(1, 1, 500000.00, 365, 5, '2025-01-15'),
(2, 2, 100000.00, 180, 4, '2025-03-22'),
(3, 3, 1000000.00, 730, 6, '2025-02-10'),
(4, 4, 75000.00, 90, 3, '2025-04-05'),
(5, 5, 300000.00, 365, 5, '2025-01-30'),
(6, 6, 150000.00, 180, 4, '2025-05-12'),
(7, 7, 800000.00, 730, 6, '2025-03-18'),
(8, 8, 60000.00, 90, 3, '2025-06-01'),
(9, 9, 400000.00, 365, 5, '2025-02-25'),
(10, 10, 200000.00, 180, 4, '2025-04-14');
INSERT INTO Clients (id, LastName, Name, FatherName, Sex, Age, Segment, PhoneNumber, Email, ID_City, Birthdate) VALUES
(1, 'Иванов', 'Иван', 'Иванович', 'М', 35, 'VIP', '+79161234567', 'ivanov@mail.ru', 1, '1988-05-15'),
(2, 'Петрова', 'Мария', 'Сергеевна', 'Ж', 28, 'Стандарт', '+79269876543', 'petrova@gmail.com', 2, '1995-11-22'),
(3, 'Сидоров', 'Алексей', 'Дмитриевич', 'М', 42, 'Премиум', '+79035671234', 'sidorov@yandex.ru', 3, '1981-03-08'),
(4, 'Кузнецова', 'Елена', 'Владимировна', 'Ж', 31, 'Стандарт', '+79114567890', 'kuznetsova@mail.ru', 4, '1992-07-19'),
(5, 'Васильев', 'Дмитрий', 'Александрович', 'М', 45, 'VIP', '+79263215476', 'vasilev@gmail.com', 5, '1978-09-25'),
(6, 'Николаева', 'Ольга', 'Игоревна', 'Ж', 29, 'Стандарт', '+79087654321', 'nikolaeva@yandex.ru', 6, '1994-12-03'),
(7, 'Федоров', 'Сергей', 'Петрович', 'М', 38, 'Премиум', '+79152345678', 'fedorov@mail.ru', 7, '1985-04-17'),
(8, 'Морозова', 'Анна', 'Сергеевна', 'Ж', 27, 'Стандарт', '+79268765432', 'morozova@gmail.com', 8, '1996-08-29'),
(9, 'Павлов', 'Андрей', 'Викторович', 'М', 33, 'VIP', '+79094567812', 'pavlov@yandex.ru', 9, '1990-01-14'),
(10, 'Семенова', 'Татьяна', 'Алексеевна', 'Ж', 40, 'Премиум', '+79163456789', 'semenova@mail.ru', 10, '1983-06-22');
INSERT INTO Cities (id, City, Region, District) VALUES
(1, 'Москва', 'Московская область', 'Центральный'),
(2, 'Санкт-Петербург', 'Ленинградская область', 'Северо-Западный'),
(3, 'Новосибирск', 'Новосибирская область', 'Сибирский'),
(4, 'Екатеринбург', 'Свердловская область', 'Уральский'),
(5, 'Казань', 'Татарстан', 'Приволжский'),
(6, 'Нижний Новгород', 'Нижегородская область', 'Приволжский'),
(7, 'Челябинск', 'Челябинская область', 'Уральский'),
(8, 'Самара', 'Самарская область', 'Приволжский'),
(9, 'Омск', 'Омская область', 'Сибирский'),
(10, 'Ростов-на-Дону', 'Ростовская область', 'Южный');