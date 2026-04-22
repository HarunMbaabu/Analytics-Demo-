# SQL Data Types, Schemas, and Table Basics

## 14.2 VARCHAR

`VARCHAR` stores text with a maximum length.

**Example:**
```sql
student_name VARCHAR(100)
```

This means the column can store text up to 100 characters long.

**Use it for:**
- names
- towns
- email addresses
- phone numbers
- course names

`VARCHAR` is useful when you want text but also want to limit how long it can be.

---

## 14.3 TEXT

`TEXT` stores long text.

**Use it for:**
- comments
- descriptions
- notes
- messages

**Example:**
```sql
description TEXT
```

### Difference between VARCHAR and TEXT
- `VARCHAR(100)` has a limit.
- `TEXT` usually does not need a limit.

For beginners, both store text, but `TEXT` is better when the content may be long.

---

## 14.4 DATE

`DATE` stores calendar dates.

**Example:**
```sql
admission_date DATE
```

**Example value:**
```sql
'2026-04-23'
```

**Use it for:**
- date of birth
- joining date
- payment date
- exam date

Using the `DATE` type makes sorting and filtering dates much easier.

---

## 14.5 NUMERIC

`NUMERIC` stores numbers with decimal places.

**Example:**
```sql
fee_balance NUMERIC(10,2)
```

This means:
- up to 10 digits in total
- 2 digits after the decimal point

**Use it for:**
- prices
- salaries
- balances
- fees
- money values

**Example values:**
- `4500.00`
- `120.50`
- `99999.99`

Money should usually not be stored as plain integer if cents or decimal values matter.

---

## 14.6 BOOLEAN

`BOOLEAN` stores true or false values.

**Example:**
```sql
is_active BOOLEAN
```

**Possible values:**
- `TRUE`
- `FALSE`

**Use it for:**
- whether a student is active
- whether a payment is complete
- whether a staff member is on leave
- whether an item is available

This is useful when the answer is simply yes/no, true/false.

---

## 14.7 SERIAL

`SERIAL` is used for auto-incrementing whole numbers.

**Example:**
```sql
student_id SERIAL
```

This means PostgreSQL automatically generates values such as:
- `1`
- `2`
- `3`
- `4`

`SERIAL` is commonly used for primary keys because it gives each row a unique number automatically.

---

## 15. Why phone numbers are usually stored as text

This is an important teaching point because many beginners think phone numbers should be stored as integers.

Phone numbers are usually stored as text because:
- we do not calculate with phone numbers
- some numbers start with zero
- some may contain `+254`
- some may contain spaces or formatting symbols

Because of this, phone numbers are usually better stored as `VARCHAR`, not `INTEGER`.

---

## 16. Simple example of columns and their data types

| Column Name    | Data Type      | Reason                        |
|----------------|----------------|-------------------------------|
| student_id     | SERIAL         | unique automatic ID           |
| student_name   | VARCHAR(100)   | stores names                  |
| age            | INTEGER        | stores whole numbers          |
| phone_number   | VARCHAR(20)    | stores phone numbers as text  |
| fee_balance    | NUMERIC(10,2)  | stores money                  |
| admission_date | DATE           | stores dates                  |
| is_active      | BOOLEAN        | stores true/false             |
| comments       | TEXT           | stores long text              |

---

## 17. What is a schema?

A schema is a container inside a database that holds tables and other database objects.

Think of it as a folder inside the database.

Inside a schema, you may find:
- tables
- views
- functions
- indexes
- sequences

At this stage, students mainly need to understand schemas as a way of organizing tables.

**Simple definition:**
A schema is a section inside a database used to group related database objects.

---

## 18. Why schemas are important

Schemas are important because they help organize a database more clearly.

They help with:
- grouping related tables
- separating work by department or purpose
- avoiding name conflicts
- keeping large systems organized

For example, one database may have:
- `school.students`
- `finance.payments`
- `hr.employees`

Here:
- `school` is a schema
- `finance` is a schema
- `hr` is a schema
- `students`, `payments`, and `employees` are tables

This helps keep the database clean and organized.

---

## 19. Default schema in PostgreSQL

In PostgreSQL, the default schema is usually called `public`.

That means if you create a table without specifying a schema, PostgreSQL will often create it inside the `public` schema.

**Example:**
```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100)
);
```

This usually creates:
- `public.students`

Even if you did not type `public`, PostgreSQL normally places it there by default.

---

## 20. Database hierarchy

Students should understand this structure clearly:

1. Database
2. Schema
3. Table
4. Rows
5. Columns

So:
- a database can contain many schemas
- a schema can contain many tables
- a table contains rows and columns

This hierarchy helps students know where each concept fits.

---

## 21. Schema analogy

Think of a school:
- the whole school is like the database
- departments in the school are like schemas
- files in each department are like tables

Examples:
- finance department = `finance` schema
- academics department = `school` schema
- library department = `library` schema

Inside those departments, there are files such as:
- student records
- fee records
- book records
- exam records

Those files are like tables.

So:
- database = whole school
- schema = department
- table = file

---

## 22. Difference between a database and a schema

A database is the bigger container.
A schema is a smaller container inside the database.

Relationship:
- database contains schemas
- schemas contain tables

A schema is not the same thing as a database.

---

## 23. SQL example: creating a schema

```sql
CREATE SCHEMA school;
```

This command creates a schema called `school`.

---

## 24. SQL example: creating a table inside a schema

```sql
CREATE TABLE school.students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    age INTEGER,
    gender VARCHAR(10),
    phone_number VARCHAR(20),
    fee_balance NUMERIC(10,2),
    admission_date DATE,
    is_active BOOLEAN
);
```

Explanation:
- `CREATE TABLE school.students` means create a table called `students` inside the `school` schema.
- `student_id SERIAL PRIMARY KEY` creates an automatic unique ID.
- `student_name VARCHAR(100) NOT NULL` stores student names and requires a value.
- `age INTEGER` stores whole numbers.
- `gender VARCHAR(10)` stores short text.
- `phone_number VARCHAR(20)` stores phone numbers as text.
- `fee_balance NUMERIC(10,2)` stores money values.
- `admission_date DATE` stores dates.
- `is_active BOOLEAN` stores true/false values.

---

## 25. What does NOT NULL mean?

`NOT NULL` means the column must always have a value.

If a column is marked as `NOT NULL`, you are not allowed to leave it empty when inserting data.

**Example:**
```sql
student_name VARCHAR(100) NOT NULL
```

This means every row must have a student name.

---

## 26. Difference between table structure and table data

### Table structure
Table structure means the design of the table:
- table name
- column names
- data types
- rules such as primary key or not null

### Table data
Table data means the actual values stored inside the table.

**Example of structure:**
```sql
CREATE TABLE school.students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100),
    age INTEGER
);
```

**Example of data:**
```sql
INSERT INTO school.students (student_name, age)
VALUES
('Amina', 21),
('Brian', 24),
('Faith', 22);
```

So:
- `CREATE TABLE` defines the structure.
- `INSERT INTO` adds the actual data.

**Easy analogy:**
- Structure is like building shelves in a shop.
- Data is like placing goods on those shelves.

---

## 27. SQL example: inserting data

```sql
INSERT INTO school.students (
    student_name,
    age,
    gender,
    phone_number,
    fee_balance,
    admission_date,
    is_active
)
VALUES
('Amina', 21, 'Female', '0712345678', 4500.00, '2026-01-10', TRUE),
('Brian', 24, 'Male', '0722334455', 0.00, '2026-02-01', TRUE),
('Faith', 22, 'Female', NULL, 1500.00, '2026-03-15', FALSE);
```

This query adds three student records into the table.

Notice:
- Amina, Brian, and Faith each become one row.
- Faith has `NULL` for phone number.
- `TRUE` and `FALSE` are boolean values.
- money values use decimals.
- dates use `YYYY-MM-DD`.

---

## 28. SQL example: viewing data

```sql
SELECT * FROM school.students;
```

This query means:
- `SELECT` = retrieve data
- `*` = all columns
- `FROM school.students` = from the students table in the `school` schema

---

## 29. Another example with products

```sql
CREATE SCHEMA shop;

CREATE TABLE shop.products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(10,2),
    stock_quantity INTEGER,
    date_added DATE
);

INSERT INTO shop.products (
    product_name,
    category,
    price,
    stock_quantity,
    date_added
)
VALUES
('Sugar', 'Grocery', 180.00, 50, '2026-04-01'),
('Bread', 'Bakery', 65.00, 30, '2026-04-10'),
('Milk', 'Dairy', 55.00, 40, '2026-04-15');

SELECT * FROM shop.products;
```

---

## 30. Important beginner warning

Students often confuse these five terms:
- database
- schema
- table
- row
- column

Repeat this relationship:
- A database contains schemas.
- A schema contains tables.
- A table contains rows and columns.
- A row is one record.
- A column is one field.

---

## 31. Class activity

Ask students to imagine a college database.

**Possible schemas:**
- `school`
- `finance`
- `library`

**Possible tables:**
- `school.students`
- `school.courses`
- `finance.payments`
- `library.books`

Then ask:
- What columns would go inside `school.students`?
- What data type should each column have?
- Which column should be the primary key?
- Which columns may allow `NULL`?
- Which columns should be `NOT NULL`?

---

## 32. Questions for students

1. What is a table?
2. What is a row?
3. What is a column?
4. What is the difference between a row and a column?
5. What is a primary key?
6. Why is a primary key important?
7. What is a duplicate?
8. What does `NULL` mean?
9. What is a data type?
10. Why do data types matter?
11. Why are phone numbers often stored as text?
12. What is a schema?
13. What is the difference between a database and a schema?
14. What is the default schema in PostgreSQL?
15. What does `SELECT * FROM school.students;` do?

---

## 33. Practice exercise 1

Create a schema called `company`.

Then create a table called `employees` inside that schema with the following columns:
- `employee_id`
- `employee_name`
- `department`
- `salary`
- `hire_date`
- `is_active`

Try to choose appropriate data types.

**Suggested answer:**
```sql
CREATE SCHEMA company;

CREATE TABLE company.employees (
    employee_id SERIAL PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    salary NUMERIC(10,2),
    hire_date DATE,
    is_active BOOLEAN
);
```

---

## 34. Practice exercise 2

Insert three employee records into the table.

**Suggested answer:**
```sql
INSERT INTO company.employees (
    employee_name,
    department,
    salary,
    hire_date,
    is_active
)
VALUES
('John Kamau', 'IT', 65000.00, '2026-01-10', TRUE),
('Mercy Achieng', 'Finance', 72000.00, '2025-11-01', TRUE),
('David Otieno', 'HR', 58000.00, '2026-02-15', FALSE);
```

---

## 35. Practice exercise 3

Display all employees.

**Suggested answer:**
```sql
SELECT * FROM company.employees;
```

---

## 36. Practice exercise 4

After creating and filling the table, identify:
- the schema name
- the table name
- the primary key
- the columns
- the rows
- the data type of each column

This exercise helps students connect theory to real table design.

---

## 37. End of lesson summary

Today we learned that databases organize information using tables. A table stores related data. A row is one full record, and a column is one piece of information about that record. A primary key uniquely identifies each row. `NULL` means a value is missing or unknown. Data types tell the database what kind of values belong in each column. Schemas help group related tables inside a database.

These ideas may seem basic, but they are the foundation of SQL. If a student understands tables, rows, columns, data types, and schemas clearly, then future topics such as filtering, sorting, joins, grouping, and relationships become much easier to learn.

---

## 38. Homework

Create a schema called `business`.

Inside it, create a table called `customers` with the following columns:
- `customer_id`
- `customer_name`
- `phone_number`
- `town`
- `join_date`
- `is_active`

Tasks:
- Choose appropriate data types.
- Insert at least 5 customer records.
- Run:

```sql
SELECT * FROM business.customers;
```

Then identify:
- the schema name
- the table name
- the primary key
- the number of rows
- the number of columns
- the data type of each column

---

## 39. Preview of the next lesson

In the next class, we will begin asking the database questions using SQL queries.

That means we will start learning:
- `SELECT`
- choosing specific columns
- `WHERE`
- filtering records
- `ORDER BY`
- sorting data

That is the stage where students move from understanding structure to actually retrieving useful information from the database.
