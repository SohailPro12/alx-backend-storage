### MySQL Advanced Concepts

#### 1. Creating Tables with Constraints

**Constraints** are rules enforced on data columns to ensure the integrity and accuracy of the data. Common constraints include `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, and `CHECK`.

**Example:**

```sql
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Primary key constraint
    name VARCHAR(100) NOT NULL,        -- Not null constraint
    email VARCHAR(100) UNIQUE,         -- Unique constraint
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id) -- Foreign key constraint
);
```

#### 2. Optimizing Queries by Adding Indexes

**Indexes** are used to speed up the retrieval of data. They can be created on one or more columns of a table.

**Example:**

```sql
-- Creating an index on the email column
CREATE INDEX idx_email ON employees(email);

-- Composite index on two columns
CREATE INDEX idx_name_department ON employees(name, department_id);
```

#### 3. Stored Procedures and Functions

**Stored Procedures** are a set of SQL statements that can be stored and executed on the database server.

**Example of a Stored Procedure:**

```sql
DELIMITER //

CREATE PROCEDURE GetEmployeeById(IN emp_id INT)
BEGIN
    SELECT * FROM employees WHERE id = emp_id;
END //

DELIMITER ;

-- Calling the stored procedure
CALL GetEmployeeById(1);
```

**Stored Functions** are similar to stored procedures but they return a single value.

**Example of a Stored Function:**

```sql
DELIMITER //

CREATE FUNCTION GetEmployeeCount() RETURNS INT
BEGIN
    DECLARE emp_count INT;
    SELECT COUNT(*) INTO emp_count FROM employees;
    RETURN emp_count;
END //

DELIMITER ;

-- Using the stored function
SELECT GetEmployeeCount();
```

#### 4. Views

**Views** are virtual tables that are based on the result set of an SQL query.

**Example:**

```sql
-- Creating a view
CREATE VIEW EmployeeView AS
SELECT id, name, email FROM employees;

-- Using the view
SELECT * FROM EmployeeView;
```

#### 5. Triggers

**Triggers** are SQL statements that are automatically executed or fired when certain events occur.

**Example:**

```sql
-- Creating a trigger that logs changes to the employees table
CREATE TABLE employee_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT,
    old_name VARCHAR(100),
    new_name VARCHAR(100),
    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //

CREATE TRIGGER after_employee_update
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employee_log(emp_id, old_name, new_name)
    VALUES (OLD.id, OLD.name, NEW.name);
END //

DELIMITER ;

-- Updating an employee to trigger the log entry
UPDATE employees SET name = 'John Doe' WHERE id = 1;
```

### Summary

- **Tables with Constraints:** Define rules on data columns to ensure data integrity.
- **Indexes:** Improve the speed of data retrieval operations.
- **Stored Procedures and Functions:** Encapsulate SQL statements for reuse and return results.
- **Views:** Create virtual tables based on SQL query results.
- **Triggers:** Automatically execute SQL statements in response to specific events on a table.
