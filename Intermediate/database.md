# Databases 📊

A **database** is a structured collection of data, enabling easy access, management, and updates. It's used to store and retrieve information in various applications.

### Relational Models 🗂️

The **relational model** organizes data in **tables** with rows (records) and columns (attributes), linked by **keys**.

### Key Concepts 🔑

- **Table**: A collection of related data organized in rows and columns.
- **Row (Tuple)**: A single record in a table.
- **Column (Attribute)**: A specific type of data in a table.

### Keys 🛠️

- **Primary Key**: Unique identifier for a row.
- **Foreign Key**: Links a row in one table to a row in another.

### Relationships 🔗

- **One-to-One**: One record in one table is linked to one in another.
- **One-to-Many**: One record in a table can link to multiple records in another.
- **Many-to-Many**: Multiple records in one table link to multiple in another.

### Examples

**One-to-One**:  
Users & User Profiles

| Users Table         | User Profiles Table   |
|---------------------|-----------------------|
| user_id (PK)        | profile_id (PK)       |
| username            | user_id (FK)          |
| email               | first_name            |

**One-to-Many**:  
Departments & Employees

| Departments Table   | Employees Table       |
|---------------------|-----------------------|
| department_id (PK)  | employee_id (PK)      |
| department_name     | department_id (FK)    |

**Many-to-Many**:  
Students & Courses

| Students Table      | Courses Table         | Enrollment Table       |
|---------------------|-----------------------|------------------------|
| student_id (PK)     | course_id (PK)        | enrollment_id (PK)     |
| student_name        | course_name           | student_id (FK)        |
|                     |                       | course_id (FK)         |

### Normalization 📉

**Normalization** minimizes data redundancy by dividing large tables into smaller ones, defining relationships.

### SQL 📑

**SQL** is used to manage and query relational databases. Common commands: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`.

### Example

**Customers Table**:

| CustomerID | Name   | Email            |
|------------|--------|------------------|
| 1          | Alice  | alice@domain.com |
| 2          | Bob    | bob@domain.com   |

**Orders Table**:

| OrderID | CustomerID | Product    | Quantity |
|---------|------------|------------|----------|
| 101     | 1          | Product A  | 2        |
| 102     | 2          | Product B  | 3        |

In this example, `CustomerID` links the tables with a **one-to-many** relationship.

---

This version keeps the main points while being more concise and adding emojis 
