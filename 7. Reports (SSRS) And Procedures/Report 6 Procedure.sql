/****** Order + Customer Payment Details Report Procedure ******/

ALTER PROCEDURE sp_OrderCustomerPaymentDetailsReport
    @DateFrom DATE,
    @DateTo DATE,
    @PlatformName NVARCHAR(50) = NULL,
    @PaymentType NVARCHAR(20) = NULL
AS
BEGIN

    SELECT
        FO.OrderID AS "Order ID",
        DC.FullName_EN AS "Customer Name",
        DC.PhoneNumber AS "Phone Number",
        DP.PlatformName_EN AS "Platform Name",
        FO.Subtotal_EGP AS "Subtotal",
        FO.DeliveryFee_EGP AS "Delivery Fee",
        FO.Tip_EGP AS "Tip",
        FO.TotalAmount_EGP AS "Total Amount",
        FO.PlatformCommissionAmount_EGP AS "Commission Amount",
        FO.TotalAmount_EGP - FO.PlatformCommissionAmount_EGP AS "Net Amount",

        CASE
            WHEN FO.IsCOD = 1 THEN 'Cash On Delivery'
            ELSE 'Online'
        END AS "Payment Type",

        CASE
            WHEN FO.IsCOD = 0 THEN 'Completed (Online)'
            WHEN FO.WasCODRefused = 1 THEN 'Refused'
            ELSE 'Completed'
        END AS "Payment Status"

    FROM Fact_Orders FO
        INNER JOIN Dim_Customer DC
            ON FO.CustomerKey = DC.CustomerKey
        INNER JOIN Dim_Platform DP
            ON FO.PlatformKey = DP.PlatformKey

    WHERE FO.DateKey BETWEEN
            YEAR(@DateFrom) * 10000 + MONTH(@DateFrom) * 100 + DAY(@DateFrom)
        AND
            YEAR(@DateTo) * 10000 + MONTH(@DateTo) * 100 + DAY(@DateTo)
        AND (
            @PlatformName IS NULL
            OR DP.PlatformName_EN = @PlatformName
        )
        AND (
            @PaymentType IS NULL
            OR (
                @PaymentType = 'Cash On Delivery'
                AND FO.IsCOD = 1
            )
            OR (
                @PaymentType = 'Online'
                AND FO.IsCOD = 0
            )
        )

    ORDER BY
        FO.TotalAmount_EGP DESC;

END;


