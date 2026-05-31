# Database Population & Programming

This folder contains everything needed to populate and operate the **RestaurantProfitability_EG** database — from raw data insertion scripts to the full set of stored procedures used across the system.

---

## 🗄️ Database Backup

The `.bak` file is a complete, fully populated SQL Server backup of the database.

**To restore:**
```sql
RESTORE DATABASE RestaurantProfitability_EG
FROM DISK = 'path_to_your_file\RestaurantProfitability_EG.bak'
WITH REPLACE;
```

---

## 📥 Bulk Insert

All raw data was generated as CSV files and loaded into SQL Server using `BULK INSERT`.

**Example:**
```sql
BULK INSERT csvfile
FROM 'path_to_your_file\csvfile.csv'
WITH (
    FIRSTROW = 2,           -- Skip header row
    FIELDTERMINATOR = ',',  -- CSV delimiter
    ROWTERMINATOR = '0x0a', -- New line character
    CODEPAGE = '65001'      -- UTF-8 encoding
);
```

> Make sure to run the table creation scripts from **[3. Database Design]** before running the bulk insert scripts.

---

## ⚙️ Stored Procedures

`StoredProcedures.sql` contains all procedures used throughout the project, including:

- **CRUD Operations** — Insert, Update, Delete, and Select for all core tables
- **Reporting Procedures** — Used by SSRS reports (Zone Performance, Customer Profitability, Platform Performance, Competitor Comparison, Top Selling Items)
- **DWH Reporting** — Order & Customer Payment Details report running on the Data Warehouse
