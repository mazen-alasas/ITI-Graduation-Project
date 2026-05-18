/****** 1. City Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_City_SelectAll
AS
BEGIN
    SELECT * FROM City;
END;
GO

-- INSERT
CREATE PROCEDURE sp_City_Insert
    @CityName_AR NVARCHAR(100),
    @CityName_EN NVARCHAR(100)
AS
BEGIN
    INSERT INTO City (CityName_AR, CityName_EN)
    VALUES (@CityName_AR, @CityName_EN);

    SELECT SCOPE_IDENTITY() AS CityID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_City_Update
    @CityID INT,
    @CityName_AR NVARCHAR(100),
    @CityName_EN NVARCHAR(100)
AS
BEGIN
    UPDATE City
    SET 
        CityName_AR = @CityName_AR,
        CityName_EN = @CityName_EN
    WHERE CityID = @CityID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_City_Delete
    @CityID INT
AS
BEGIN
    DELETE FROM City WHERE CityID = @CityID;
END;
GO





/****** 2. Customer Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_Customer_Select
AS
BEGIN
    SELECT * FROM Customer;
END;
GO

-- INSERT
CREATE PROCEDURE sp_Customer_Insert
    @PhoneNumber NVARCHAR(20),
    @FullName_AR NVARCHAR(100),
    @FullName_EN NVARCHAR(100),
    @ZoneID INT,
    @FirstOrderDate DATE,
    @Gender CHAR(1)
AS
BEGIN
    INSERT INTO Customer (
        PhoneNumber, FullName_AR, FullName_EN,
        ZoneID, FirstOrderDate, Gender
    )
    VALUES (
        @PhoneNumber, @FullName_AR, @FullName_EN,
        @ZoneID, @FirstOrderDate, @Gender
    );

    SELECT SCOPE_IDENTITY() AS CustomerID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_Customer_Update
    @CustomerID INT,
    @PhoneNumber NVARCHAR(20),
    @FullName_AR NVARCHAR(100),
    @FullName_EN NVARCHAR(100),
    @ZoneID INT,
    @FirstOrderDate DATE,
    @Gender CHAR(1)
AS
BEGIN
    UPDATE Customer
    SET PhoneNumber = @PhoneNumber,
        FullName_AR = @FullName_AR,
        FullName_EN = @FullName_EN,
        ZoneID = @ZoneID,
        FirstOrderDate = @FirstOrderDate,
        Gender = @Gender
    WHERE CustomerID = @CustomerID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_Customer_Delete
    @CustomerID INT
AS
BEGIN
    DELETE FROM Customer WHERE CustomerID = @CustomerID;
END;
GO






/****** 3. Orders Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_Orders_Select
AS
BEGIN
    SELECT * FROM Orders;
END;
GO

-- INSERT
CREATE PROCEDURE sp_Orders_Insert
    @CustomerID INT,
    @PlatformID INT,
    @ZoneID INT,
    @OrderStatus NVARCHAR(50),
    @OrderDate DATE,
    @OrderTime TIME,
    @Subtotal_EGP DECIMAL(10,2),
    @DeliveryFee_EGP DECIMAL(5,2),
    @PlatformCommissionPercent DECIMAL(5,2),
    @Tip_EGP DECIMAL(5,2),
    @IsCOD BIT,
    @WasCODRefused BIT
AS
BEGIN
    DECLARE @CommissionAmount DECIMAL(8,2);

    SET @CommissionAmount = (@Subtotal_EGP * @PlatformCommissionPercent) / 100;

    INSERT INTO Orders (
        CustomerID, PlatformID, ZoneID,
        OrderStatus, OrderDate, OrderTime,
        Subtotal_EGP, DeliveryFee_EGP,
        PlatformCommissionPercent,
        PlatformCommissionAmount_EGP,
        Tip_EGP, IsCOD, WasCODRefused
    )
    VALUES (
        @CustomerID, @PlatformID, @ZoneID,
        @OrderStatus, @OrderDate, @OrderTime,
        @Subtotal_EGP, @DeliveryFee_EGP,
        @PlatformCommissionPercent,
        @CommissionAmount,
        @Tip_EGP, @IsCOD, @WasCODRefused
    );

    SELECT SCOPE_IDENTITY() AS OrderID;
END;
GO


-- UPDATE
CREATE PROCEDURE sp_Orders_Update
    @OrderID INT,
    @OrderStatus NVARCHAR(50),
    @DeliveryFee_EGP DECIMAL(5,2),
    @Tip_EGP DECIMAL(5,2),
    @WasCODRefused BIT
AS
BEGIN
    UPDATE Orders
    SET OrderStatus = @OrderStatus,
        DeliveryFee_EGP = @DeliveryFee_EGP,
        Tip_EGP = @Tip_EGP,
        WasCODRefused = @WasCODRefused
    WHERE OrderID = @OrderID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_Orders_Delete
    @OrderID INT
AS
BEGIN
    DELETE FROM Orders WHERE OrderID = @OrderID;
END;
GO





/****** 4. OrderItem Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_OrderItem_Select
AS
BEGIN
    SELECT * FROM OrderItem;
END;
GO

-- INSERT
CREATE PROCEDURE sp_OrderItem_Insert
    @OrderID INT,
    @ItemID INT,
    @Quantity INT,
    @UnitPriceAtTime_EGP DECIMAL(8,2),
    @DiscountApplied_EGP DECIMAL(5,2)
AS
BEGIN
    INSERT INTO OrderItem (
        OrderID, ItemID, Quantity,
        UnitPriceAtTime_EGP, DiscountApplied_EGP
    )
    VALUES (
        @OrderID, @ItemID, @Quantity,
        @UnitPriceAtTime_EGP, @DiscountApplied_EGP
    );

    SELECT SCOPE_IDENTITY() AS OrderItemID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_OrderItem_Update
    @OrderItemID INT,
    @Quantity INT,
    @DiscountApplied_EGP DECIMAL(5,2)
AS
BEGIN
    UPDATE OrderItem
    SET Quantity = @Quantity,
        DiscountApplied_EGP = @DiscountApplied_EGP
    WHERE OrderItemID = @OrderItemID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_OrderItem_Delete
    @OrderItemID INT
AS
BEGIN
    DELETE FROM OrderItem WHERE OrderItemID = @OrderItemID;
END;
GO





/****** 5. DeliveryZone Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_DeliveryZone_Select
AS
BEGIN
    SELECT * FROM DeliveryZone;
END;
GO

-- INSERT
CREATE PROCEDURE sp_DeliveryZone_Insert
    @CityID INT,
    @ZoneName_AR NVARCHAR(100),
    @ZoneName_EN NVARCHAR(100),
    @TrafficFactor DECIMAL(3,2),
    @BaseDeliveryMinutes INT,
    @MinOrderForDelivery_EGP DECIMAL(8,2),
    @DeliveryFee_EGP DECIMAL(5,2)
AS
BEGIN
    INSERT INTO DeliveryZone (
        CityID, ZoneName_AR, ZoneName_EN,
        TrafficFactor, BaseDeliveryMinutes,
        MinOrderForDelivery_EGP, DeliveryFee_EGP
    )
    VALUES (
        @CityID, @ZoneName_AR, @ZoneName_EN,
        @TrafficFactor, @BaseDeliveryMinutes,
        @MinOrderForDelivery_EGP, @DeliveryFee_EGP
    );

    SELECT SCOPE_IDENTITY() AS ZoneID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_DeliveryZone_Update
    @ZoneID INT,
    @CityID INT,
    @ZoneName_AR NVARCHAR(100),
    @ZoneName_EN NVARCHAR(100),
    @TrafficFactor DECIMAL(3,2),
    @BaseDeliveryMinutes INT,
    @MinOrderForDelivery_EGP DECIMAL(8,2),
    @DeliveryFee_EGP DECIMAL(5,2)
AS
BEGIN
    UPDATE DeliveryZone
    SET CityID = @CityID,
        ZoneName_AR = @ZoneName_AR,
        ZoneName_EN = @ZoneName_EN,
        TrafficFactor = @TrafficFactor,
        BaseDeliveryMinutes = @BaseDeliveryMinutes,
        MinOrderForDelivery_EGP = @MinOrderForDelivery_EGP,
        DeliveryFee_EGP = @DeliveryFee_EGP
    WHERE ZoneID = @ZoneID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_DeliveryZone_Delete
    @ZoneID INT
AS
BEGIN
    DELETE FROM DeliveryZone WHERE ZoneID = @ZoneID;
END;
GO





/****** 6. DeliveryPlatform Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_DeliveryPlatform_Select
AS
BEGIN
    SELECT * FROM DeliveryPlatform;
END;
GO

-- INSERT
CREATE PROCEDURE sp_DeliveryPlatform_Insert
    @PlatformName_AR NVARCHAR(50),
    @PlatformName_EN NVARCHAR(50),
    @CommissionRateDefault DECIMAL(5,2),
    @HasCODSupport BIT,
    @HasWalletPayment BIT,
    @AvgDeliveryFee_EGP DECIMAL(5,2),
    @IsNegotiable BIT
AS
BEGIN
    INSERT INTO DeliveryPlatform (
        PlatformName_AR, PlatformName_EN,
        CommissionRateDefault, HasCODSupport,
        HasWalletPayment, AvgDeliveryFee_EGP, IsNegotiable
    )
    VALUES (
        @PlatformName_AR, @PlatformName_EN,
        @CommissionRateDefault, @HasCODSupport,
        @HasWalletPayment, @AvgDeliveryFee_EGP, @IsNegotiable
    );

    SELECT SCOPE_IDENTITY() AS PlatformID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_DeliveryPlatform_Update
    @PlatformID INT,
    @PlatformName_AR NVARCHAR(50),
    @PlatformName_EN NVARCHAR(50),
    @CommissionRateDefault DECIMAL(5,2),
    @HasCODSupport BIT,
    @HasWalletPayment BIT,
    @AvgDeliveryFee_EGP DECIMAL(5,2),
    @IsNegotiable BIT
AS
BEGIN
    UPDATE DeliveryPlatform
    SET PlatformName_AR = @PlatformName_AR,
        PlatformName_EN = @PlatformName_EN,
        CommissionRateDefault = @CommissionRateDefault,
        HasCODSupport = @HasCODSupport,
        HasWalletPayment = @HasWalletPayment,
        AvgDeliveryFee_EGP = @AvgDeliveryFee_EGP,
        IsNegotiable = @IsNegotiable
    WHERE PlatformID = @PlatformID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_DeliveryPlatform_Delete
    @PlatformID INT
AS
BEGIN
    DELETE FROM DeliveryPlatform WHERE PlatformID = @PlatformID;
END;
GO




/****** 7. MenuCategory Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_MenuCategory_Select
AS
BEGIN
    SELECT * FROM MenuCategory;
END;
GO

-- INSERT
CREATE PROCEDURE sp_MenuCategory_Insert
    @CategoryName_AR NVARCHAR(50),
    @CategoryName_EN NVARCHAR(50)
AS
BEGIN
    INSERT INTO MenuCategory (CategoryName_AR, CategoryName_EN)
    VALUES (@CategoryName_AR, @CategoryName_EN);

    SELECT SCOPE_IDENTITY() AS CategoryID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_MenuCategory_Update
    @CategoryID INT,
    @CategoryName_AR NVARCHAR(50),
    @CategoryName_EN NVARCHAR(50)
AS
BEGIN
    UPDATE MenuCategory
    SET CategoryName_AR = @CategoryName_AR,
        CategoryName_EN = @CategoryName_EN
    WHERE CategoryID = @CategoryID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_MenuCategory_Delete
    @CategoryID INT
AS
BEGIN
    DELETE FROM MenuCategory WHERE CategoryID = @CategoryID;
END;
GO





/****** 8. Ingredient Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_Ingredient_Select
AS
BEGIN
    SELECT * FROM Ingredient;
END;
GO

-- INSERT
CREATE PROCEDURE sp_Ingredient_Insert
    @IngredientName_EN NVARCHAR(100),
    @IngredientName_AR NVARCHAR(100),
    @UnitOfMeasure NVARCHAR(20)
AS
BEGIN
    INSERT INTO Ingredient (IngredientName_EN, IngredientName_AR, UnitOfMeasure)
    VALUES (@IngredientName_EN, @IngredientName_AR, @UnitOfMeasure);

    SELECT SCOPE_IDENTITY() AS IngredientID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_Ingredient_Update
    @IngredientID INT,
    @IngredientName_EN NVARCHAR(100),
    @IngredientName_AR NVARCHAR(100),
    @UnitOfMeasure NVARCHAR(20)
AS
BEGIN
    UPDATE Ingredient
    SET IngredientName_EN = @IngredientName_EN,
        IngredientName_AR = @IngredientName_AR,
        UnitOfMeasure = @UnitOfMeasure
    WHERE IngredientID = @IngredientID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_Ingredient_Delete
    @IngredientID INT
AS
BEGIN
    DELETE FROM Ingredient WHERE IngredientID = @IngredientID;
END;
GO





/****** 9. MenuItem Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_MenuItem_Select
AS
BEGIN
    SELECT * FROM MenuItem;
END;
GO

-- INSERT
CREATE PROCEDURE sp_MenuItem_Insert
    @CategoryID INT,
    @ItemName_AR NVARCHAR(100),
    @ItemName_EN NVARCHAR(100),
    @CurrentPrice_EGP DECIMAL(8,2),
    @PackagingCost_EGP DECIMAL(4,2),
    @PrepTimeMinutes INT,
    @IsAvailableForDelivery BIT,
    @IsBundle BIT
AS
BEGIN
    INSERT INTO MenuItem (
        CategoryID, ItemName_AR, ItemName_EN,
        CurrentPrice_EGP, PackagingCost_EGP,
        PrepTimeMinutes, IsAvailableForDelivery, IsBundle
    )
    VALUES (
        @CategoryID, @ItemName_AR, @ItemName_EN,
        @CurrentPrice_EGP, @PackagingCost_EGP,
        @PrepTimeMinutes, @IsAvailableForDelivery, @IsBundle
    );

    SELECT SCOPE_IDENTITY() AS ItemID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_MenuItem_Update
    @ItemID INT,
    @CategoryID INT,
    @ItemName_AR NVARCHAR(100),
    @ItemName_EN NVARCHAR(100),
    @CurrentPrice_EGP DECIMAL(8,2),
    @PackagingCost_EGP DECIMAL(4,2),
    @PrepTimeMinutes INT,
    @IsAvailableForDelivery BIT,
    @IsBundle BIT
AS
BEGIN
    UPDATE MenuItem
    SET CategoryID = @CategoryID,
        ItemName_AR = @ItemName_AR,
        ItemName_EN = @ItemName_EN,
        CurrentPrice_EGP = @CurrentPrice_EGP,
        PackagingCost_EGP = @PackagingCost_EGP,
        PrepTimeMinutes = @PrepTimeMinutes,
        IsAvailableForDelivery = @IsAvailableForDelivery,
        IsBundle = @IsBundle
    WHERE ItemID = @ItemID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_MenuItem_Delete
    @ItemID INT
AS
BEGIN
    DELETE FROM MenuItem WHERE ItemID = @ItemID;
END;
GO




/****** 10. IngredientPrice Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_IngredientPrice_Select
AS
BEGIN
    SELECT * FROM IngredientPrice;
END;
GO

-- INSERT
CREATE PROCEDURE sp_IngredientPrice_Insert
    @IngredientID INT,
    @PricePerUnit_EGP DECIMAL(8,2),
    @EffectiveDate DATE
AS
BEGIN
    INSERT INTO IngredientPrice (IngredientID, PricePerUnit_EGP, EffectiveDate)
    VALUES (@IngredientID, @PricePerUnit_EGP, @EffectiveDate);

    SELECT SCOPE_IDENTITY() AS IngredientPriceID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_IngredientPrice_Update
    @IngredientPriceID INT,
    @PricePerUnit_EGP DECIMAL(8,2),
    @EffectiveDate DATE
AS
BEGIN
    UPDATE IngredientPrice
    SET PricePerUnit_EGP = @PricePerUnit_EGP,
        EffectiveDate = @EffectiveDate
    WHERE IngredientPriceID = @IngredientPriceID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_IngredientPrice_Delete
    @IngredientPriceID INT
AS
BEGIN
    DELETE FROM IngredientPrice WHERE IngredientPriceID = @IngredientPriceID;
END;
GO






/****** 11. MenuItemIngredient Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_MenuItemIngredient_Select
AS
BEGIN
    SELECT * FROM MenuItemIngredient;
END;
GO

-- INSERT
CREATE PROCEDURE sp_MenuItemIngredient_Insert
    @ItemID INT,
    @IngredientID INT,
    @QuantityNeeded DECIMAL(6,2)
AS
BEGIN
    INSERT INTO MenuItemIngredient (ItemID, IngredientID, QuantityNeeded)
    VALUES (@ItemID, @IngredientID, @QuantityNeeded);

    SELECT SCOPE_IDENTITY() AS MenuItemIngredientID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_MenuItemIngredient_Update
    @MenuItemIngredientID INT,
    @QuantityNeeded DECIMAL(6,2)
AS
BEGIN
    UPDATE MenuItemIngredient
    SET QuantityNeeded = @QuantityNeeded
    WHERE MenuItemIngredientID = @MenuItemIngredientID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_MenuItemIngredient_Delete
    @MenuItemIngredientID INT
AS
BEGIN
    DELETE FROM MenuItemIngredient WHERE MenuItemIngredientID = @MenuItemIngredientID;
END;
GO





/****** 12. Competitor Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_Competitor_Select
AS
BEGIN
    SELECT * FROM Competitor;
END;
GO

-- INSERT
CREATE PROCEDURE sp_Competitor_Insert
    @ZoneID INT,
    @CompetitorName_AR NVARCHAR(100),
    @CompetitorName_EN NVARCHAR(100),
    @HasDelivery BIT,
    @AverageDeliveryMinutes INT,
    @GoogleMapsRating DECIMAL(3,2)
AS
BEGIN
    INSERT INTO Competitor (
        ZoneID, CompetitorName_AR, CompetitorName_EN,
        HasDelivery, AverageDeliveryMinutes, GoogleMapsRating
    )
    VALUES (
        @ZoneID, @CompetitorName_AR, @CompetitorName_EN,
        @HasDelivery, @AverageDeliveryMinutes, @GoogleMapsRating
    );

    SELECT SCOPE_IDENTITY() AS CompetitorID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_Competitor_Update
    @CompetitorID INT,
    @ZoneID INT,
    @CompetitorName_AR NVARCHAR(100),
    @CompetitorName_EN NVARCHAR(100),
    @HasDelivery BIT,
    @AverageDeliveryMinutes INT,
    @GoogleMapsRating DECIMAL(3,2)
AS
BEGIN
    UPDATE Competitor
    SET ZoneID = @ZoneID,
        CompetitorName_AR = @CompetitorName_AR,
        CompetitorName_EN = @CompetitorName_EN,
        HasDelivery = @HasDelivery,
        AverageDeliveryMinutes = @AverageDeliveryMinutes,
        GoogleMapsRating = @GoogleMapsRating
    WHERE CompetitorID = @CompetitorID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_Competitor_Delete
    @CompetitorID INT
AS
BEGIN
    DELETE FROM Competitor WHERE CompetitorID = @CompetitorID;
END;
GO






/****** 13. CompetitorPlatform Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_CompetitorPlatform_Select
AS
BEGIN
    SELECT * FROM CompetitorPlatform;
END;
GO

-- INSERT
CREATE PROCEDURE sp_CompetitorPlatform_Insert
    @CompetitorID INT,
    @PlatformID INT
AS
BEGIN
    INSERT INTO CompetitorPlatform (CompetitorID, PlatformID)
    VALUES (@CompetitorID, @PlatformID);

    SELECT SCOPE_IDENTITY() AS CompetitorPlatformID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_CompetitorPlatform_Update
    @CompetitorPlatformID INT,
    @CompetitorID INT,
    @PlatformID INT
AS
BEGIN
    UPDATE CompetitorPlatform
    SET CompetitorID = @CompetitorID,
        PlatformID = @PlatformID
    WHERE CompetitorPlatformID = @CompetitorPlatformID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_CompetitorPlatform_Delete
    @CompetitorPlatformID INT
AS
BEGIN
    DELETE FROM CompetitorPlatform WHERE CompetitorPlatformID = @CompetitorPlatformID;
END;
GO







/****** 14. CODRefusalLog Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_CODRefusalLog_Select
AS
BEGIN
    SELECT * FROM CODRefusalLog;
END;
GO

-- INSERT
CREATE PROCEDURE sp_CODRefusalLog_Insert
    @OrderID INT,
    @RefusalReason NVARCHAR(200),
    @RefusedAmount_EGP DECIMAL(10,2)
AS
BEGIN
    INSERT INTO CODRefusalLog (OrderID, RefusalReason, RefusedAmount_EGP)
    VALUES (@OrderID, @RefusalReason, @RefusedAmount_EGP);

    SELECT SCOPE_IDENTITY() AS RefusalID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_CODRefusalLog_Update
    @RefusalID INT,
    @RefusalReason NVARCHAR(200),
    @RefusedAmount_EGP DECIMAL(10,2)
AS
BEGIN
    UPDATE CODRefusalLog
    SET RefusalReason = @RefusalReason,
        RefusedAmount_EGP = @RefusedAmount_EGP
    WHERE RefusalID = @RefusalID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_CODRefusalLog_Delete
    @RefusalID INT
AS
BEGIN
    DELETE FROM CODRefusalLog WHERE RefusalID = @RefusalID;
END;
GO






/****** 15. CompetitorMenuItem Table ******/
-- SELECT ALL
CREATE PROCEDURE sp_CompetitorMenuItem_Select
AS
BEGIN
    SELECT * FROM CompetitorMenuItem;
END;
GO

-- INSERT
CREATE PROCEDURE sp_CompetitorMenuItem_Insert
    @CompetitorID INT,
    @YourItemID INT,
    @CompetitorItemName NVARCHAR(100),
    @CompetitorPrice_EGP DECIMAL(8,2),
    @IsOnPromotion BIT,
    @DateTracked DATE
AS
BEGIN
    INSERT INTO CompetitorMenuItem (
        CompetitorID, YourItemID,
        CompetitorItemName, CompetitorPrice_EGP,
        IsOnPromotion, DateTracked
    )
    VALUES (
        @CompetitorID, @YourItemID,
        @CompetitorItemName, @CompetitorPrice_EGP,
        @IsOnPromotion, @DateTracked
    );

    SELECT SCOPE_IDENTITY() AS CompetitorMenuItemID;
END;
GO

-- UPDATE
CREATE PROCEDURE sp_CompetitorMenuItem_Update
    @CompetitorMenuItemID INT,
    @CompetitorItemName NVARCHAR(100),
    @CompetitorPrice_EGP DECIMAL(8,2),
    @IsOnPromotion BIT,
    @DateTracked DATE
AS
BEGIN
    UPDATE CompetitorMenuItem
    SET CompetitorItemName = @CompetitorItemName,
        CompetitorPrice_EGP = @CompetitorPrice_EGP,
        IsOnPromotion = @IsOnPromotion,
        DateTracked = @DateTracked
    WHERE CompetitorMenuItemID = @CompetitorMenuItemID;
END;
GO

-- DELETE
CREATE PROCEDURE sp_CompetitorMenuItem_Delete
    @CompetitorMenuItemID INT
AS
BEGIN
    DELETE FROM CompetitorMenuItem WHERE CompetitorMenuItemID = @CompetitorMenuItemID;
END;
GO




