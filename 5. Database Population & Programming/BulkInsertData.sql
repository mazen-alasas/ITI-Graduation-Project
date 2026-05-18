-- Import Orders data from CSV file into SQL Server

BULK INSERT csvfile
FROM 'path_to_your_file\csvfile.csv'
WITH (
    FIRSTROW = 2,              -- Skip header row
    FIELDTERMINATOR = ',',     -- CSV delimiter
    ROWTERMINATOR = '0x0a',    -- New line character
    CODEPAGE = '65001'         -- UTF-8 encoding
);
