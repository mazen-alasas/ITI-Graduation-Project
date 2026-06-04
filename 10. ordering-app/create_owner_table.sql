-- ============================================================
-- FoodFlow — AppOwner Table
-- Run this ONCE in SSMS on RestaurantProfitability_EG
-- BEFORE running setup_owners.py
-- ============================================================

USE RestaurantProfitability_EG;
GO

CREATE TABLE AppOwner (
    OwnerID      INT           PRIMARY KEY IDENTITY(1,1),
    Username     NVARCHAR(50)  NOT NULL UNIQUE,
    PasswordHash NVARCHAR(64)  NOT NULL,
    FullName     NVARCHAR(100) NOT NULL,
    Role         NVARCHAR(50)  NOT NULL DEFAULT 'Manager',
    CreatedAt    DATETIME      NOT NULL DEFAULT GETDATE()
);
GO

-- Verify the table was created
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'AppOwner';
GO
