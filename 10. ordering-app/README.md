# FoodFlow — Customer Ordering App

Part of the **Restaurant Delivery Profitability & Competitor Intelligence System**
ITI Graduation Project 2025

---

## What This App Does

FoodFlow is a locally-hosted web application built with **Python + Streamlit** that serves two roles:

**For customers:**
A mobile-friendly Arabic ordering interface accessible via QR code. Customers enter their phone number, browse the menu by category, add items to a cart with live price tracking, and place a cash-on-delivery order. New customers register with a simple form. Returning customers are recognized by phone number.

**For the restaurant owner:**
A password-protected dashboard showing this month's key stats (total orders, revenue, COD refusals, refusal rate, top platform), quick-access buttons to all 5 BI dashboards published on Power BI Service and Tableau Public, and a scrollable grid of all 6 SSRS paginated reports.

---

## How It Connects to the Full System

```
Customer places order via browser (QR code → ngrok → Streamlit)
        ↓
Streamlit writes directly to SQL Server OLTP database
        ↓
N8N automation polls every 1 minute
        ↓
Executes sp_UpdateCustomerRisk → checks COD refusal history
        ↓
If customer refusal rate ≥ 15% → sends Telegram alert to owner
```

The app inserts into the `Orders` and `OrderItem` tables of the OLTP database (`RestaurantProfitability_EG`). All orders are placed as Cash on Delivery via the WhatsApp platform (PlatformID = 5, 0% commission), simulating a direct restaurant order.

---

## Tech Stack

| Layer | Tool |
|-------|------|
| UI | Streamlit (Python) |
| Database connection | pyodbc |
| Database | SQL Server (local) |
| Public access | ngrok |
| Automation | N8N (local, Node.js) |
| Alerts | Telegram Bot API |

---

## Project Structure

```
ordering-app/
├── app.py                   ← Main Streamlit application (all screens)
├── db.py                    ← All SQL Server queries and insert functions
├── setup_owners.py          ← CLI tool to create owner login accounts
├── create_owner_table.sql   ← Run once in SSMS to create AppOwner table
├── requirements.txt         ← Python dependencies
├── .env.template            ← Copy → rename to .env → fill your server name
├── Logo2.png                ← FoodFlow brand logo
├── TOP Selling Items.png            ┐
├── Order & Customer Payment Details.png  │
├── Platform Performance.png         │  SSRS report screenshots
├── Competitor Comparison.png        │  displayed in owner dashboard
├── Zone Performance.png             │
└── Customer Profitability.png       ┘
```

> `.env` is excluded from the repository — it contains your local SQL Server credentials.

---

## First-Time Setup

### Prerequisites
- Python 3.10+
- SQL Server (local) with `RestaurantProfitability_EG` database populated
- ODBC Driver 17 for SQL Server
- Node.js + N8N installed (`npm install -g n8n`)
- ngrok account (free) with authtoken configured

### Step 1 — Install Python dependencies
```bash
pip install streamlit pyodbc python-dotenv
```

### Step 2 — Configure database connection
```bash
# Copy the template and fill in your SQL Server instance name
cp .env.template .env
```
Open `.env` and set `DB_SERVER` to your SQL Server instance name (e.g. `localhost`, `.\SQLEXPRESS`).

### Step 3 — Create the AppOwner table
Open `create_owner_table.sql` in SSMS and run it against `RestaurantProfitability_EG`.

### Step 4 — Create owner login accounts
```bash
python setup_owners.py
```
Choose option 1 and follow the prompts to create username and password for the owner dashboard.

### Step 5 — Run the app
```bash
python -m streamlit run app.py
```

### Step 6 — Expose publicly via ngrok (for QR code demo)
In a second terminal:
```bash
ngrok http 8501
```
Copy the `https://xxxx.ngrok-free.app` URL and generate a QR code at [qr-code-generator.com](https://www.qr-code-generator.com).

---

## Demo Day Startup Sequence

Open three separate terminals and run one command in each:

```bash
# Terminal 1 — N8N automation
n8n start

# Terminal 2 — Streamlit app
python -m streamlit run app.py

# Terminal 3 — ngrok public URL
ngrok http 8501
```

Then open `http://localhost:5678` in Chrome, confirm the N8N workflow is Published/Active, generate the QR code from the ngrok URL, and the demo is ready.

---

## App Screens

| Screen | Description |
|--------|-------------|
| Role Selection | Choose between Customer or Owner login |
| Phone Entry | Customer identifies by phone number |
| Registration | New customers provide name, gender, city, zone |
| Menu Browser | Browse 12 Arabic categories, add items, live cart total |
| Order Confirmation | Review items, subtotal, delivery fee, total |
| Order Placed | Confirmation with estimated delivery time |
| Owner Login | Username + password authentication |
| Owner Dashboard | Monthly stats, BI dashboard links, SSRS report screenshots |

---

## Team

| Member | Responsibility |
|--------|---------------|
| Ali Elsabaa | Streamlit app, N8N workflow, Menu & Ingredients dashboards (#9–12) |
| Abdullah Elsayed | Executive & Operations dashboards (#1–4) |
| Abdelrahman Rafaat | COD & Zones dashboards (#5–8) |
| Mazen | Customer Analytics dashboards (#17–20) |
| Mohamed Salah | Platforms & Competitors Tableau dashboards (#13–16) |
