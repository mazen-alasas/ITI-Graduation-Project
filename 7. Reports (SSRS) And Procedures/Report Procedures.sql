/****** 1. Zone Performance Report Procedure ******/

ALTER PROCEDURE sp_ZonePerformanceReport
    @DateFrom DATE,
    @DateTo DATE,
    @Top INT = 10
AS
BEGIN

    SELECT TOP (@Top)
        DZ.ZoneID AS "Zone ID", 
        DZ.ZoneName_EN AS "Zone Name",
        COUNT(O.OrderID) AS "Total Orders",
        SUM(O.Subtotal_EGP) AS "Total Sales",
        CAST(AVG(O.Subtotal_EGP) AS DECIMAL(10,2)) AS "Avg Order Value",
        SUM(O.DeliveryFee_EGP) AS "Total Delivery Fees"
        
    FROM DeliveryZone DZ INNER JOIN Orders O
        ON DZ.ZoneID = O.ZoneID

    WHERE O.OrderDate BETWEEN @DateFrom AND @DateTo

    GROUP BY
        DZ.ZoneID,
        DZ.ZoneName_EN

    ORDER BY "Total Sales" DESC;
END;
GO







/****** 2. Customer Profitability Report Procedure ******/

ALTER PROCEDURE sp_CustomerProfitabilityReport
    @DateFrom DATE,
    @DateTo DATE,
    @Top INT = 10
AS
BEGIN

    SELECT TOP (@Top)
        C.CustomerID AS "Customer ID",
        C.FullName_EN AS "Customer Name",
        C.PhoneNumber AS "Phone Number",
        COUNT(O.OrderID) AS "Total Orders",
        SUM(O.Subtotal_EGP) AS "Total Spent",
        CAST(AVG(O.Subtotal_EGP) AS DECIMAL(10,2)) AS "Avg Order Value"
        
    FROM Customer C INNER JOIN Orders O
        ON C.CustomerID = O.CustomerID

    WHERE O.OrderDate BETWEEN @DateFrom AND @DateTo

    GROUP BY
        C.CustomerID,
        C.FullName_EN,
        C.PhoneNumber

    ORDER BY "Total Spent" DESC;
END;
GO





/******** 3. Platform Performance Report Procedure *******/

ALTER PROCEDURE sp_PlatformPerformanceReport
    @DateFrom DATE,
    @DateTo DATE
AS
BEGIN

    SELECT
        DP.PlatformID AS "Platform ID",
        DP.PlatformName_EN AS "Platform Name",
        COUNT(O.OrderID) AS "Total Orders",
        SUM(O.Subtotal_EGP) AS "Total Sales",
        SUM(O.PlatformCommissionAmount_EGP) AS "Total Commission",
        CAST(AVG(O.Subtotal_EGP) AS DECIMAL(10,2)) AS "Avg Order Value"

    FROM DeliveryPlatform DP INNER JOIN Orders O
        ON DP.PlatformID = O.PlatformID

    WHERE O.OrderDate BETWEEN @DateFrom AND @DateTo

    GROUP BY
        DP.PlatformID,
        DP.PlatformName_EN

    ORDER BY "Total Sales" DESC;
END;
GO




/****** 4. Competitor Comparison Report Procedure ******/

ALTER PROCEDURE sp_CompetitorComparisonMatrixReport
AS
BEGIN

    SELECT
        C.CompetitorName_EN AS "Competitor Name",
        CAST(AVG(C.AverageDeliveryMinutes * 1.0) AS DECIMAL(10,2)) AS "Avg Delivery Time",
        CAST(AVG(C.GoogleMapsRating) AS DECIMAL(10,2)) AS "Avg Google Rating",
        COUNT(C.CompetitorID) AS "Number Of Branches",
        COUNT(DISTINCT CP.PlatformID) AS "Number Of Platforms"

    FROM Competitor C LEFT JOIN CompetitorPlatform CP
        ON C.CompetitorID = CP.CompetitorID

    GROUP BY
        C.CompetitorName_EN

    ORDER BY
        "Avg Google Rating" DESC;

END;
GO





/****** 5. Order Details Report Procedure (Top Selling Items) ******/

ALTER PROCEDURE sp_TopSellingItemsReport
    @DateFrom DATE,
    @DateTo DATE,
    @TOP INT
AS
BEGIN

    SELECT TOP (@TOP)
        MI.ItemID AS "Item ID",
        MI.ItemName_EN AS "Item Name",
        SUM(OI.Quantity) AS "Total Quantity Sold",
        SUM(OI.Quantity * (OI.UnitPriceAtTime_EGP - ISNULL(OI.DiscountApplied_EGP, 0))) AS "Total Revenue",
        CAST(MI.CurrentPrice_EGP AS DECIMAL(10,0)) AS "Unit Price",
        COUNT(DISTINCT OI.OrderID) AS "Number Of Orders"

    FROM OrderItem OI 
        INNER JOIN MenuItem MI ON OI.ItemID = MI.ItemID
        INNER JOIN Orders O ON OI.OrderID = O.OrderID

    WHERE O.OrderDate BETWEEN @DateFrom AND @DateTo

    GROUP BY
        MI.ItemID,
        MI.ItemName_EN,
        MI.CurrentPrice_EGP

    ORDER BY "Total Revenue" DESC;

END;
GO





/*
ALTER PROCEDURE sp_TopSellingItemsReport
    @DateFrom DATE,
    @DateTo DATE,
    @TOP INT
AS
BEGIN

    SELECT TOP (@TOP)
        MI.ItemID AS "Item ID",
        MI.ItemName_EN AS "Item Name",
        SUM(OI.Quantity) AS "Total Quantity Sold",
        SUM(OI.Quantity * MI.CurrentPrice_EGP) AS "Total Revenue",
        CAST(MI.CurrentPrice_EGP AS DECIMAL(10,0)) AS "Unit Price",
        COUNT(DISTINCT OI.OrderID) AS "Number Of Orders"

    FROM OrderItem OI INNER JOIN MenuItem MI
            ON OI.ItemID = MI.ItemID
        INNER JOIN Orders O
            ON OI.OrderID = O.OrderID

    WHERE O.OrderDate BETWEEN @DateFrom AND @DateTo

    GROUP BY
        MI.ItemID,
        MI.ItemName_EN,
        MI.CurrentPrice_EGP

    ORDER BY "Total Revenue" DESC;

END;
GO

ALTER PROCEDURE sp_TopSellingItemsReport
    @DateFrom DATE,
    @DateTo DATE,
    @TOP INT
AS
BEGIN

    SELECT TOP (@TOP)
        MI.ItemID AS "Item ID",
        MI.ItemName_EN AS "Item Name",
        SUM(OI.Quantity) AS "Total Quantity Sold",
        SUM(OI.Quantity * (OI.UnitPriceAtTime_EGP - ISNULL(OI.DiscountApplied_EGP, 0))) AS "Total Revenue",
        CAST(AVG(OI.UnitPriceAtTime_EGP) AS DECIMAL(10,0)) AS "Unit Price",
        COUNT(DISTINCT OI.OrderID) AS "Number Of Orders"

    FROM OrderItem OI 
        INNER JOIN MenuItem MI ON OI.ItemID = MI.ItemID
        INNER JOIN Orders O ON OI.OrderID = O.OrderID

    WHERE O.OrderDate BETWEEN @DateFrom AND @DateTo

    GROUP BY
        MI.ItemID,
        MI.ItemName_EN

    ORDER BY "Total Revenue" DESC;

END;
GO






UPDATE OI
SET OI.UnitPriceAtTime_EGP = MI.CurrentPrice_EGP
FROM OrderItem OI
INNER JOIN MenuItem MI ON OI.ItemID = MI.ItemID





SELECT 
    OI.OrderItemID,
    OI.UnitPriceAtTime_EGP,
    MI.CurrentPrice_EGP,
    CASE 
        WHEN OI.UnitPriceAtTime_EGP = MI.CurrentPrice_EGP THEN 'SAME - مش بيتحفظ صح'
        ELSE 'DIFFERENT - OK'
    END AS Check_Result
FROM OrderItem OI
INNER JOIN MenuItem MI ON OI.ItemID = MI.ItemID



SELECT TOP 20
    OI.OrderItemID,
    OI.Quantity,
    OI.UnitPriceAtTime_EGP,
    OI.Quantity * OI.UnitPriceAtTime_EGP AS Calculated,
    O.Subtotal_EGP
FROM OrderItem OI INNER JOIN Orders O ON OI.OrderID = O.OrderID
ORDER BY OI.OrderItemID


SELECT 
    OI.OrderItemID,
    OI.ItemID,
    MI.ItemName_EN,
    MI.CurrentPrice_EGP,
    OI.UnitPriceAtTime_EGP,
    OI.DiscountApplied_EGP,
    CASE 
        WHEN OI.UnitPriceAtTime_EGP = ROUND(OI.UnitPriceAtTime_EGP, 0) THEN 'Round Number'
        ELSE 'Fractional - suspicious'
    END AS PriceCheck
FROM OrderItem OI
INNER JOIN MenuItem MI ON OI.ItemID = MI.ItemID
WHERE OI.UnitPriceAtTime_EGP != ROUND(OI.UnitPriceAtTime_EGP, 0)
ORDER BY OI.OrderItemID




*/