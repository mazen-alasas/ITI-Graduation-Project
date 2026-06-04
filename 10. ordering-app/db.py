import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    conn_str = (
        f"DRIVER={{{os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')}}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)


# ─── Customer ────────────────────────────────────────────────────────────────

def get_customer_by_phone(phone: str):
    """Returns customer dict with zone info, or None if not found."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            c.CustomerID, c.FullName_EN, c.FullName_AR, c.Gender, c.ZoneID,
            dz.ZoneName_AR, dz.ZoneName_EN,
            dz.DeliveryFee_EGP, dz.BaseDeliveryMinutes, dz.TrafficFactor
        FROM Customer c
        JOIN DeliveryZone dz ON c.ZoneID = dz.ZoneID
        WHERE c.PhoneNumber = ?
    """, phone)
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'CustomerID':         row[0],
            'FullName_EN':        row[1],
            'FullName_AR':        row[2],
            'Gender':             row[3],
            'ZoneID':             row[4],
            'ZoneName_AR':        row[5],
            'ZoneName_EN':        row[6],
            'DeliveryFee_EGP':    float(row[7]),
            'BaseDeliveryMinutes': int(row[8]),
            'TrafficFactor':      float(row[9]),
        }
    return None


def insert_customer(phone: str, full_name_en: str, full_name_ar: str,
                    gender: str, zone_id: int) -> int:
    """Inserts a new customer and returns the new CustomerID."""
    from datetime import date
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Customer
            (PhoneNumber, FullName_EN, FullName_AR, Gender, ZoneID, FirstOrderDate)
        OUTPUT INSERTED.CustomerID
        VALUES (?, ?, ?, ?, ?, ?)
    """, phone, full_name_en, full_name_ar, gender, zone_id, date.today())
    customer_id = int(cursor.fetchone()[0])
    conn.commit()
    conn.close()
    return customer_id


# ─── Geography ───────────────────────────────────────────────────────────────

def get_cities() -> list:
    """Returns all cities ordered by Arabic name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT CityID, CityName_AR, CityName_EN
        FROM City
        ORDER BY CityName_AR
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{'CityID': r[0], 'CityName_AR': r[1], 'CityName_EN': r[2]} for r in rows]


def get_zones_by_city(city_id: int) -> list:
    """Returns all delivery zones for a given city."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ZoneID, ZoneName_AR, ZoneName_EN,
               DeliveryFee_EGP, BaseDeliveryMinutes, TrafficFactor
        FROM DeliveryZone
        WHERE CityID = ?
        ORDER BY ZoneName_AR
    """, city_id)
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            'ZoneID':              r[0],
            'ZoneName_AR':         r[1],
            'ZoneName_EN':         r[2],
            'DeliveryFee_EGP':     float(r[3]),
            'BaseDeliveryMinutes': int(r[4]),
            'TrafficFactor':       float(r[5]),
        }
        for r in rows
    ]


# ─── Menu ────────────────────────────────────────────────────────────────────

def get_menu_items() -> list:
    """Returns all delivery-available items with their category info."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            mi.ItemID, mi.ItemName_AR, mi.ItemName_EN,
            mi.CurrentPrice_EGP, mi.PrepTimeMinutes,
            mc.CategoryID, mc.CategoryName_AR, mc.CategoryName_EN
        FROM MenuItem mi
        JOIN MenuCategory mc ON mi.CategoryID = mc.CategoryID
        WHERE mi.IsAvailableForDelivery = 1
        ORDER BY mc.CategoryName_AR, mi.ItemName_AR
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            'ItemID':           r[0],
            'ItemName_AR':      r[1],
            'ItemName_EN':      r[2],
            'CurrentPrice_EGP': float(r[3]),
            'PrepTimeMinutes':  int(r[4]),
            'CategoryID':       r[5],
            'CategoryName_AR':  r[6],
            'CategoryName_EN':  r[7],
        }
        for r in rows
    ]


# ─── Orders ──────────────────────────────────────────────────────────────────

def insert_order(customer_id: int, zone_id: int, phone: str,
                 subtotal: float, delivery_fee: float) -> int:
    """Inserts an order and returns the new OrderID."""
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
        INSERT INTO Orders (
            CustomerID, PlatformID, ZoneID, OrderStatus,
            OrderDate, OrderTime,
            Subtotal_EGP, DeliveryFee_EGP,
            PlatformCommissionPercent, PlatformCommissionAmount_EGP,
            Tip_EGP, IsCOD, WasCODRefused, PhoneNumber
        )
        OUTPUT INSERTED.OrderID
        VALUES (?, 5, ?, 'Pending', ?, ?, ?, ?, 0.00, 0.00, 0, 1, 0, ?)
    """,
        customer_id, zone_id,
        now.date(), now.time(),
        round(subtotal, 2), round(delivery_fee, 2),
        phone
    )
    order_id = int(cursor.fetchone()[0])
    conn.commit()
    conn.close()
    return order_id


def get_owner_by_username(username: str):
    """Returns owner dict if found, None otherwise."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT OwnerID, Username, PasswordHash, FullName, Role
        FROM AppOwner
        WHERE Username = ?
    """, username)
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'OwnerID':      row[0],
            'Username':     row[1],
            'PasswordHash': row[2],
            'FullName':     row[3],
            'Role':         row[4],
        }
    return None


def get_monthly_stats() -> dict:
    """Returns current month stats. Includes Pending orders in revenue."""
    from datetime import datetime
    now = datetime.now()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            COUNT(*)                                                        AS TotalOrders,
            SUM(CASE WHEN OrderStatus IN ('Delivered','Pending')
                THEN Subtotal_EGP + DeliveryFee_EGP + ISNULL(Tip_EGP,0)
                ELSE 0 END)                                                 AS TotalRevenue,
            SUM(CASE WHEN IsCOD=1 AND WasCODRefused=1 THEN 1 ELSE 0 END)  AS CODRefusals,
            SUM(CASE WHEN IsCOD=1 THEN 1 ELSE 0 END)                       AS TotalCOD,
            COUNT(DISTINCT CustomerID)                                      AS UniqueCustomers,
            SUM(CASE WHEN IsCOD=1 AND WasCODRefused=1
                THEN Subtotal_EGP + DeliveryFee_EGP ELSE 0 END)            AS TotalRefusedAmount
        FROM Orders
        WHERE MONTH(OrderDate) = ? AND YEAR(OrderDate) = ?
    """, now.month, now.year)
    row = cursor.fetchone()

    cursor.execute("""
        SELECT TOP 1 dp.PlatformName_EN, COUNT(*) AS Cnt
        FROM Orders o
        JOIN DeliveryPlatform dp ON o.PlatformID = dp.PlatformID
        WHERE MONTH(o.OrderDate) = ? AND YEAR(o.OrderDate) = ?
        GROUP BY dp.PlatformName_EN
        ORDER BY Cnt DESC
    """, now.month, now.year)
    prow = cursor.fetchone()
    conn.close()

    total_cod    = int(row[3]) if row[3] else 0
    cod_refusals = int(row[2]) if row[2] else 0
    refusal_rate = round(cod_refusals / total_cod * 100, 1) if total_cod > 0 else 0.0

    return {
        'Month':              now.strftime('%B %Y'),
        'TotalOrders':        int(row[0])   if row[0] else 0,
        'TotalRevenue':       float(row[1]) if row[1] else 0.0,
        'CODRefusals':        cod_refusals,
        'CODRefusalRate':     refusal_rate,
        'TotalRefusedAmount': float(row[5]) if row[5] else 0.0,
        'UniqueCustomers':    int(row[4])   if row[4] else 0,
        'TopPlatform':        prow[0]       if prow else 'N/A',
        'TopPlatformOrders':  int(prow[1])  if prow else 0,
    }


def insert_order_items(order_id: int, cart: dict):
    """
    Inserts one OrderItem row per cart entry.
    cart structure: { item_id: { quantity, price, name_ar, prep_time } }
    """
    conn = get_connection()
    cursor = conn.cursor()
    for item_id, item in cart.items():
        cursor.execute("""
            INSERT INTO OrderItem
                (OrderID, ItemID, Quantity, UnitPriceAtTime_EGP,
                 DiscountApplied_EGP, CostAtTime_EGP)
            VALUES (?, ?, ?, ?, 0.00, 0.00)
        """,
            order_id,
            item_id,
            item['quantity'],
            round(item['price'], 2)
        )
    conn.commit()
    conn.close()
