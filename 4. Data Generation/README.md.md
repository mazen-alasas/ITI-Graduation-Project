# AI Data Generation Prompt
## Egyptian Restaurant Delivery Profitability & Competitor Intelligence System

---

## CONTEXT & INSTRUCTIONS FOR THE AI

You are generating **realistic, analytically rich sample data** for a SQL Server database supporting a Business Intelligence system for an Egyptian restaurant operating in the food delivery market. The system tracks delivery orders across platforms (Talabat, Elmenus, Otlob, Akelni, WhatsApp), calculates profit per order, monitors COD refusal risk, and benchmarks competitor pricing.

**Critical rules:**
- All monetary values are in **Egyptian Pounds (EGP)**. Current rate: ~53 EGP = 1 USD.
- All names should use **Egyptian Arabic and English** where bilingual fields exist.
- Data must be **rich and diverse** to support meaningful analysis across dashboards, reports, and ML models (e.g., COD risk prediction, menu optimization, churn analysis).
- Generate each table as a **separate CSV file**, with the filename matching the table name (e.g., `City.csv`, `DeliveryZone.csv`, etc.).
- Respect all **foreign key relationships** — generate parent tables before child tables and use consistent IDs.
- The **Orders table must be very large** (at least **3,000–5,000 rows**) covering the period **2024-01-01 to 2025-12-31** to support time-series analysis, seasonal trends (Ramadan, summer, holidays), hourly heatmaps, and churn analysis.
- Distribute data to reflect **realistic Egyptian market behavior**: peak hours (12–2 PM lunch, 8–11 PM dinner), higher COD usage (~70–80%), weekend spikes (Thursday–Friday nights), Ramadan ordering at Iftar (5–7 PM) and Suhoor (2–4 AM), seasonal ingredient price fluctuations.
- Every table should have enough rows to be analytically meaningful — see per-table size guidance below.

---

## KEY SEASONAL DATES TO EMBED IN DATA

Use the following **exact dates** to drive seasonal patterns in Orders, OrderItems, CODRefusalLog, CompetitorMenuItem, and IngredientPrice:

### Ramadan Periods:
| Year | Start | End |
|---|---|---|
| 2023 | 2023-03-23 | 2023-04-21 |
| 2024 | 2024-03-11 | 2024-04-09 |
| 2025 | 2025-03-01 | 2025-03-30 |

### Eid Al Fitr (3-day celebration each):
| Year | Date Range |
|---|---|
| 2023 | 2023-04-21 to 2023-04-23 |
| 2024 | 2024-04-10 to 2024-04-12 |
| 2025 | 2025-03-30 to 2025-04-01 |

### Eid Al Adha (4-day celebration each):
| Year | Date Range |
|---|---|
| 2023 | 2023-06-28 to 2023-07-01 |
| 2024 | 2024-06-16 to 2024-06-19 |
| 2025 | 2025-06-06 to 2025-06-09 |

**Behavioral rules for seasonal dates:**
- **Ramadan weekdays**: Shift 60–70% of orders to Iftar window (17:00–19:00) and Suhoor (02:00–04:00). Reduce lunch orders (~5%). Family meals and desserts (Qatayef, Kunafa, Om Ali) spike +40%.
- **Eid Al Fitr**: Family meals and desserts spike +60%. Many orders placed in afternoon (14:00–18:00). Platform promotions active. Order volume +30% above average.
- **Eid Al Adha**: Meat dishes (grills, kofta, kabab, lamb) spike +50%. Family meal orders very common. Order volume +25%. Lamb/meat ingredient prices spike.
- **Summer (July–August)**: Lunch orders drop ~20%. Late night orders increase. Juice and cold drink orders spike. Tomato prices extremely volatile (+30–50% spikes possible in Aug).

---

## TABLE-BY-TABLE SPECIFICATIONS

---

### TABLE 1: `City`
**Description:** Egyptian cities where the restaurant operates or has delivery zones.
**Target size:** 10–15 rows

| Column | Description & Egyptian Values |
|---|---|
| CityID | Auto-increment integer starting at 1 |
| CityName_AR | Arabic city name. Use: القاهرة، الإسكندرية، الجيزة، المنصورة، الإسماعيلية، أسيوط، طنطا، الزقازيق، بورسعيد، دمياط، السويس، الفيوم، المنيا، شبين الكوم، الشروق |
| CityName_EN | English: Cairo, Alexandria, Giza, Mansoura, Ismailia, Asyut, Tanta, Zagazig, Port Said, Damietta, Suez, Fayoum, Minya, Shebin El Kom, El Shorouk |

---

### TABLE 2: `DeliveryZone`
**Description:** Specific delivery neighborhoods or districts within each city.
**Target size:** 40–45 rows

Distribute zones across all cities. Use **1 zone for small/simple cities** (e.g., Fayoum, Shebin El Kom, Zagazig), **2–3 zones for mid-size cities** (Mansoura, Ismailia, Tanta, Port Said, Suez, Damietta, Minya), and **4–5 zones for large cities** (Cairo gets 5, Giza gets 4–5, Alexandria gets 4).

**Zone examples per city (use these names):**

**Cairo (5 zones):** مدينة نصر (Nasr City), مصر الجديدة (Heliopolis), التجمع الخامس (New Cairo – 5th Settlement), الزمالك (Zamalek), عين شمس / شبرا (Ain Shams / Shubra)

**Giza (5 zones):** المهندسين / الدقي (Mohandessin / Dokki), حدائق الأهرام (Haram Gardens), الشيخ زايد (Sheikh Zayed), 6 أكتوبر (6 October City), المعادي (Maadi)

**Alexandria (4 zones):** كورنيش الإسكندرية (Alexandria Corniche), المنتزه (Montazah), الرمل (Raml Station), سيدي بشر (Sidi Bishr)

**Mansoura (3 zones):** وسط المنصورة (Mansoura Downtown), دقادوس / بحري (Dakadous / Bahri), ميت غمر (Mit Ghamr area)

**Ismailia (2 zones):** وسط الإسماعيلية (Ismailia Downtown), حي الإفرنج (Al Afrang District)

**Tanta (2 zones):** وسط طنطا (Tanta Downtown), المحلة الكبرى (Mahalla El Kubra area)

**Port Said (2 zones):** وسط بورسعيد (Port Said Downtown), بورفؤاد (Port Fouad)

**Asyut (2 zones):** وسط أسيوط (Asyut Downtown), ديروط (Dayrout area)

**Suez (2 zones):** وسط السويس (Suez Downtown), عتاقة (Ataka area)

**Damietta (2 zones):** وسط دمياط (Damietta Downtown), رأس البر (Ras El Bar)

**Minya (2 zones):** وسط المنيا (Minya Downtown), مطاي (Matay area)

**Zagazig (1 zone):** وسط الزقازيق (Zagazig Downtown)

**Fayoum (1 zone):** وسط الفيوم (Fayoum Downtown)

**Shebin El Kom (1 zone):** وسط شبين الكوم (Shebin El Kom Downtown)

**El Shorouk (1 zone):** مدينة الشروق (El Shorouk City)

| Column | Description & Egyptian Values |
|---|---|
| ZoneID | Auto-increment integer |
| CityID | FK to City |
| ZoneName_AR | Arabic district name — use names from the city breakdown above |
| ZoneName_EN | English transliteration — use names from the city breakdown above |
| TrafficFactor | Between 0.5–3.0. Inner Cairo dense districts (Ain Shams/Shubra, Nasr City): 2.0–2.8. Premium suburbs (New Cairo, Sheikh Zayed, 6 October): 1.0–1.5. Alexandria Corniche: 1.5–2.0. Mid-city provincial zones: 0.8–1.5. Small city single zones: 0.5–0.9 |
| BaseDeliveryMinutes | 15–45 minutes. Dense districts: 30–45. Suburbs: 15–25. Provincial cities: 20–35 |
| MinOrderForDelivery_EGP | Start at 50 EGP minimum. Scale upward based on zone class and area coverage. Budget/popular zones (Shubra, Ain Shams, provincial cities): 50–60 EGP. Mid-class zones (Nasr City, Heliopolis, Mansoura DT): 65–75 EGP. Upper-mid zones (Maadi, Mohandessin, Alexandria Corniche): 75–85 EGP. Premium zones (Zamalek, New Cairo 5th Settlement, Sheikh Zayed, 6 October): 90–100 EGP. Maximum cap: 100 EGP |
| DeliveryFee_EGP | Minimum 20 EGP. Scale up based on zone distance, class, and traffic. Budget/central zones: 20–25 EGP. Mid zones: 25–35 EGP. Premium/distant zones (New Cairo, 6 October, Sheikh Zayed): 35–50 EGP. Provincial cities (flat, less traffic): 20–30 EGP. Leave open-ended upward for very distant premium zones |

---

### TABLE 3: `DeliveryPlatform`
**Description:** The delivery platforms the restaurant uses. This system covers five platforms: Talabat, Elmenus, Otlob, Akelni, and WhatsApp (direct). All platforms support food delivery orders equivalent to restaurant meal delivery — no grocery-only platforms included.
**Target size:** 5 rows (exactly)

| Column | Description & Egyptian Values |
|---|---|
| PlatformID | 1, 2, 3, 4, 5 |
| PlatformName_AR | طلبات، إلمينس، أطلب، أكلني، واتساب |
| PlatformName_EN | Talabat, Elmenus, Otlob, Akelni, WhatsApp |
| CommissionRateDefault | Talabat: 20.00–25.00%. Elmenus: 15.00–18.00%. Otlob: 15.00–20.00% (acquired by Talabat but still operating independently in Egypt, commission similar range). Akelni: 12.00–15.00% (local platform, lower commission to attract restaurants). WhatsApp: 0.00% (direct channel, no commission) |
| HasCODSupport | All five: 1 (true) |
| HasWalletPayment | Talabat: 1 (Talabat wallet). Elmenus: 1. Otlob: 1. Akelni: 0 (cash or card only, no dedicated wallet). WhatsApp: 0 |
| AvgDeliveryFee_EGP | Talabat: 25.00. Elmenus: 22.00. Otlob: 20.00. Akelni: 18.00. WhatsApp: varies — restaurant charges directly, use 20.00 as avg |
| IsNegotiable | Talabat: 1. Elmenus: 1. Otlob: 1. Akelni: 1. WhatsApp: 0 |

**Platform distribution in Orders table:** Talabat ~45%, Elmenus ~22%, Otlob ~13%, Akelni ~8%, WhatsApp ~12% (WhatsApp direct orders remain common in Egypt especially for repeat customers).

---

### TABLE 4: `MenuCategory`
**Description:** Categories grouping menu items. Use typical Egyptian restaurant categories.
**Target size:** 8–12 rows

| Column | Description & Egyptian Values |
|---|---|
| CategoryID | Auto-increment |
| CategoryName_AR | مشويات، أكلات شعبية، مقبلات، مشروبات ساخنة، عصائر، حلويات، وجبات عائلية، برجر، بيتزا، أطفال، سلطات، سندويشات |
| CategoryName_EN | Grills, Traditional Egyptian, Appetizers, Hot Drinks, Juices, Desserts, Family Meals, Burgers, Pizza, Kids Meals, Salads, Sandwiches |

---

### TABLE 5: `Ingredient`
**Description:** Raw ingredients used in menu items. All ingredient names must appear in **Arabic** in a dedicated Arabic name column.
**Target size:** 40–55 rows

| Column | Description & Egyptian Values |
|---|---|
| IngredientID | Auto-increment |
| IngredientName_EN | English ingredient name |
| IngredientName_AR | Arabic ingredient name — **required, no nulls**. See mapping below |
| UnitOfMeasure | kg for meats, vegetables, grains. liter for oils, milk. piece for eggs, pita bread. gram for spices |

**Full ingredient list with Arabic names (use all of these — add more as needed to cover all menu items):**

| English | Arabic | Unit |
|---|---|---|
| Chicken Breast | صدر دجاج | kg |
| Minced Beef | لحم بقري مفروم | kg |
| Lamb Kofta Mix | خلطة كفتة ضأن | kg |
| Lamb Meat | لحم ضأن | kg |
| Pigeon | حمام | piece |
| Liver (Calf) | كبدة عجل | kg |
| Sausage (Basterma) | بسطرمة | kg |
| Okra | بامية | kg |
| Molokhia (Dried) | ملوخية مجففة | kg |
| Tomatoes | طماطم | kg |
| Onions | بصل | kg |
| Garlic | ثوم | kg |
| Eggplant | باذنجان | kg |
| Potatoes | بطاطس | kg |
| Cucumber | خيار | kg |
| Parsley | بقدونس | kg |
| Coriander | كزبرة | kg |
| Green Pepper | فلفل أخضر | kg |
| Lettuce | خس | kg |
| Lemon | ليمون | kg |
| Fava Beans (Ful) | فول مدمس | kg |
| Chickpeas | حمص | kg |
| Lentils | عدس | kg |
| Rice | أرنب / أرز | kg |
| Pasta (Macaroni) | مكرونة | kg |
| Vermicelli | شعرية | kg |
| Pita Bread | عيش بلدي | piece |
| Fino Bread (Roll) | عيش فينو | piece |
| Burger Bun | خبز برجر | piece |
| Pizza Dough | عجينة بيتزا | kg |
| Tahini | طحينة | kg |
| Tomato Paste | صلصة طماطم | kg |
| Béchamel Sauce Mix | خلطة بشاميل | kg |
| Sunflower Oil | زيت عباد الشمس | liter |
| Butter | زبدة | kg |
| Cheese (Romi) | جبنة رومي | kg |
| Mozzarella Cheese | جبنة موزاريلا | kg |
| Eggs | بيض | piece |
| Milk | لبن | liter |
| Cream | قشطة / كريمة | liter |
| Flour | دقيق | kg |
| Sugar | سكر | kg |
| Salt | ملح | kg |
| Black Pepper | فلفل أسود | gram |
| Cumin | كمون | gram |
| Cinnamon | قرفة | gram |
| Cardamom | هيل | gram |
| Chili Powder | فلفل حار | gram |
| Turmeric | كركم | gram |
| Vinegar | خل | liter |
| Yogurt | زبادي | kg |
| Semolina | سميد | kg |
| Mango (Fresh) | مانجو طازجة | kg |
| Hibiscus (Dried) | كركديه مجفف | kg |
| Tea Leaves | شاي | gram |
| Turkish Coffee | قهوة تركي | gram |
| Grape Leaves | ورق عنب | kg |
| Nuts Mix (for Om Ali) | خلطة مكسرات | kg |
| Konafa (Shredded Dough) | كنافة خيوط | kg |
| Ghee (Samn Baladi) | سمن بلدي | kg |

---

### TABLE 6: `MenuItem`
**Description:** All dishes/items on the delivery menu. Ensure **at least 3 items per category**, with richer categories (Grills, Traditional Egyptian, Sandwiches, Desserts) having 5–8 items.
**Target size:** 50–65 rows

**Minimum items per category:**
- Grills (مشويات): ≥ 6 items (kofta, kabab, chicken, liver, mixed, shawarma meat)
- Traditional Egyptian (أكلات شعبية): ≥ 6 items (molokhia, ful, taameya, koshari, moussaka, macarona bechamel, stuffed pigeon, cow feet)
- Sandwiches (سندويشات): ≥ 5 items (shawarma chicken, shawarma meat, liver sandwich, kofta sandwich, falafel sandwich)
- Desserts (حلويات): ≥ 5 items (om ali, kunafa, qatayef, basbousa, muhallabia)
- Appetizers (مقبلات): ≥ 4 items (tahini, baba ganoush, hummus, grape leaves, falafel plate)
- Burgers (برجر): ≥ 4 items (beef burger, chicken burger, double beef, crispy chicken)
- Pizza (بيتزا): ≥ 3 items (margherita, pepperoni-style, mixed)
- Juices (عصائر): ≥ 4 items (lemon, mango, mixed fruit, karkade)
- Hot Drinks (مشروبات ساخنة): ≥ 3 items (tea, Turkish coffee, anise/yansoon)
- Salads (سلطات): ≥ 3 items (green salad, tabbouleh, fattoush)
- Family Meals (وجبات عائلية): ≥ 3 items (mixed grill family, family chicken, family traditional)
- Kids Meals (أطفال): ≥ 3 items (kids chicken, kids burger, kids pasta)

| Column | Description & Egyptian Values |
|---|---|
| ItemID | Auto-increment |
| CategoryID | FK to MenuCategory |
| ItemName_AR | Arabic dish name (see examples in original list plus additions above) |
| ItemName_EN | English name |
| CurrentPrice_EGP | Prices must be 1.5x–2x above calculated ingredient cost for the item. See cost calculation rules in TABLE 8 / IngredientPrice section. Reference ranges: Traditional/popular dishes: 60–140 EGP. Grills (kofta, kabab): 140–280 EGP. Half chicken: 170–220 EGP. Shawarma sandwiches: 80–130 EGP. Burgers: 100–180 EGP. Pizza: 170–280 EGP. Family meals: 350–700 EGP. Appetizers/salads: 50–95 EGP. Juices: 40–70 EGP. Hot drinks: 35–65 EGP. Desserts: 50–110 EGP. Kids meals: 90–150 EGP |
| PackagingCost_EGP | 3–18 EGP depending on item type. Family meals: 12–18. Individual dishes: 4–10. Drinks: 3–5 |
| PrepTimeMinutes | Fast items (drinks, falafel, bread): 3–8 min. Standard (shawarma, burgers): 10–15 min. Complex (grills, stuffed pigeon): 20–35 min. Family meals: 30–50 min |
| IsAvailableForDelivery | Most items: 1. Some fragile/impractical items: 0 |
| IsBundle | Family meals and combo deals: 1. Individual items: 0 |

---

### TABLE 7: `IngredientPrice`
**Description:** Historical price records per ingredient. Prices reflect real Egyptian inflation. Updated **on the 1st of each month** for every ingredient.
**Target size:** 600–800 rows (one record per ingredient per month, covering Jan 2024 – Dec 2025 = 24 months × ~40 ingredients)

| Column | Description & Egyptian Values |
|---|---|
| IngredientPriceID | Auto-increment |
| IngredientID | FK to Ingredient |
| PricePerUnit_EGP | See realistic price ranges and rules below |
| EffectiveDate | Always the **1st day of the month** (e.g., 2024-01-01, 2024-02-01, … 2025-12-01). This must cover **2024-01-01 through 2025-12-01** |

**Price generation rules:**
- Record one price per ingredient per month (EffectiveDate = 1st of each month).
- Prices must show **realistic month-to-month variation** — not only increases. Allow some months to dip slightly (0–5% decrease), but the **overall trend over 24 months must be upward** (reflecting Egyptian food inflation of ~30–50% cumulative over the period).
- **March 2024 shock**: Apply a notable price jump of 10–20% for most ingredients in March–April 2024, reflecting the EGP devaluation event (38% pound devaluation in March 2024).
- **Ramadan months** (March 2024, March 2025): Poultry, meat, and staple prices rise 5–15% due to demand spikes.
- **Summer volatility** (July–August each year): Tomatoes, eggplant, green peppers, and other vegetables can spike 20–40% or drop sharply — show high variance.
- **Starting prices (Jan 2024)** — use these as baseline (slightly higher than what was in the original prompt):

| Ingredient | Jan 2024 Base Price | Unit |
|---|---|---|
| Chicken Breast | 110 EGP | kg |
| Minced Beef | 200 EGP | kg |
| Lamb Meat / Kofta Mix | 290 EGP | kg |
| Pigeon | 55 EGP | piece |
| Liver (Calf) | 130 EGP | kg |
| Tomatoes | 14 EGP | kg |
| Onions | 10 EGP | kg |
| Garlic | 55 EGP | kg |
| Potatoes | 18 EGP | kg |
| Eggplant | 12 EGP | kg |
| Rice | 28 EGP | kg |
| Lentils | 35 EGP | kg |
| Pasta (Macaroni) | 28 EGP | kg |
| Sunflower Oil | 55 EGP | liter |
| Butter | 130 EGP | kg |
| Flour | 20 EGP | kg |
| Tahini | 90 EGP | kg |
| Fava Beans | 30 EGP | kg |
| Cheese (Romi) | 120 EGP | kg |
| Mozzarella Cheese | 150 EGP | kg |
| Eggs | 8 EGP | piece |
| Milk | 22 EGP | liter |
| Sugar | 30 EGP | kg |
| Pita Bread | 2 EGP | piece |
| Fino Bread | 3 EGP | piece |
| Molokhia (Dried) | 80 EGP | kg |
| Grape Leaves | 40 EGP | kg |
| Konafa (Shredded Dough) | 60 EGP | kg |
| Semolina | 25 EGP | kg |
| Nuts Mix | 220 EGP | kg |
| Ghee (Samn Baladi) | 180 EGP | kg |
| Black Pepper | 350 EGP | kg (price per kg; use 0.005 kg per dish) |
| Cumin | 120 EGP | kg |
| Pizza Dough | 25 EGP | kg |
| Burger Bun | 5 EGP | piece |
| Mango (Fresh) | 18 EGP | kg |
| Hibiscus (Dried) | 70 EGP | kg |
| Cream | 60 EGP | liter |
| Yogurt | 30 EGP | kg |

---

### TABLE 8: `MenuItemIngredient`
**Description:** Which ingredients go into each menu item and in what quantities. This table is used to **calculate ingredient cost per item** at the time of each order.
**Target size:** 180–280 rows (each item uses 3–8 ingredients on average)

| Column | Description & Egyptian Values |
|---|---|
| MenuItemIngredientID | Auto-increment |
| ItemID | FK to MenuItem |
| IngredientID | FK to Ingredient |
| QuantityNeeded | In the ingredient's unit. Examples: Chicken breast per shawarma: 0.20 kg. Minced beef per kofta portion: 0.25 kg. Lamb per stuffed pigeon: 0.10 kg. Rice per serving: 0.15 kg. Oil per serving: 0.05 liter. Tahini per plate: 0.03 kg. Spices per dish: 0.005–0.010 kg. Eggs per item: 1–2 pieces. Flour for pizza dough: 0.25 kg. Mozzarella per pizza: 0.20 kg |

**Cost Calculation Rule (important for MenuItem.CurrentPrice_EGP):**
For each menu item, calculate its **IngredientCost** = Σ (QuantityNeeded × PricePerUnit_EGP at the relevant date). Then set **CurrentPrice_EGP = IngredientCost × (1.5 to 2.0)** depending on:
- Category premium: Grills and Family Meals → 1.8–2.0x. Sandwiches/Burgers → 1.6–1.8x. Traditional/Popular → 1.5–1.7x. Drinks/Juices/Desserts → 1.8–2.0x (high margin). Pizza → 1.7–1.9x. Kids Meals → 1.5–1.7x. Appetizers/Salads → 1.6–1.8x.
- Also add PackagingCost on top before finalizing price.

---

### TABLE 9: `Customer`
**Description:** Customers who have placed at least one delivery order.
**Target size:** 400–600 rows

| Column | Description & Egyptian Values |
|---|---|
| CustomerID | Auto-increment |
| PhoneNumber | Egyptian mobile format: 01XXXXXXXXX (11 digits). Operators: 010 (Vodafone), 011 (Etisalat), 012 (Mobinil/Orange), 015 (WE). All unique |
| FullName_AR | Arabic full names — **NOT NULL, no empty values**. All customers must have a full name. Use first name + last name minimum (e.g., محمد أحمد الشافعي، نور إبراهيم حسن، فاطمة محمود علي). Male examples: محمد أحمد الشافعي، أحمد محمود سليمان، عمر إبراهيم حسين، خالد حسن عبد الرحمن، يوسف علي الصباع، مصطفى سامي الغزالي، كريم طارق البدوي. Female: نور محمد السيد، فاطمة أحمد إبراهيم، سارة علي عبد الله، مريم حسن محمود، رنا خالد الشرقاوي، دينا إبراهيم منصور، ياسمين عمر فاروق. A full name consists of 2–4 name parts (e.g., Ali Elsabaa = 2 parts; Ali Abdelrahman Ali Elsabaa = 4 parts) |
| FullName_EN | Transliteration of the Arabic name — **NOT NULL, no empty values**. Must match FullName_AR |
| ZoneID | FK to DeliveryZone. Distribute across all zones, with concentration in Cairo/Giza zones |
| FirstOrderDate | Between **2024-01-01 and 2025-06-30**. Distribute gradually to simulate customer acquisition growth. This ensures customers can be tracked for at least 6 months within the data period |

---

### TABLE 10: `Competitor`
**Description:** Competing restaurants in the same delivery zones. Used for the Competitor Intelligence dashboards.
**Target size:** 25–40 rows

| Column | Description & Egyptian Values |
|---|---|
| CompetitorID | Auto-increment |
| ZoneID | FK to DeliveryZone. Each zone should have 1–4 competitors |
| CompetitorName_AR | Arabic restaurant names. Examples: مطعم البيك، أبو شقرة، كشري الحسين، مطعم فيليكس، عزبة حنفي، مطعم الريف، كنتاكي، ماكدونالدز، بيتزا هت، بابا عمر، حسن بلقطة، مطعم بورتو، سنداوتش ميكر، الأمريكاني، مطعم الهانا، دجاج مارين، مطعم أبو طارق، مطعم زوبا، مطعم كازاز |
| CompetitorName_EN | Al Baik, Abu Shakra, Koshary El Hussein, Felix Restaurant, Azbet Hanafi, El Reef Restaurant, KFC, McDonald's, Pizza Hut, Baba Omar, Hassan Balkutah, Porto Restaurant, Sandwich Maker, El Americani, El Hana Restaurant, Chicken Marin, Abu Tarek, Zooba, Kazaz |
| HasDelivery | Most: 1. A few dine-in only: 0 |
| AverageDeliveryMinutes | 20–60 minutes. Fast food chains: 20–30. Local restaurants: 35–55. NULL for those with no delivery |
| GoogleMapsRating | Between **2.0–4.9**. Apply realistic ratings based on zone class and brand type: Premium zones (Zamalek, New Cairo, Maadi): well-known brands 4.0–4.9, lesser-known 3.5–4.3. Popular local places in mid zones: 3.8–4.5. Budget/popular zones (Shubra, Ain Shams): 3.0–4.2. Provincial cities: 3.2–4.4. Chain restaurants (KFC, McDonald's): 3.5–4.0 (globally recognized, mixed reviews). Poor-quality or new competitors: 2.0–3.2. Do not cluster all ratings around 4.x — ensure spread across the full 2.0–4.9 range |

---

### TABLE 11: `CompetitorPlatform`
**Description:** Which delivery platforms each competitor uses.
**Target size:** 60–90 rows

| Column | Description & Egyptian Values |
|---|---|
| CompetitorPlatformID | Auto-increment |
| CompetitorID | FK to Competitor |
| PlatformID | FK to DeliveryPlatform (Talabat=1, Elmenus=2, Otlob=3, Akelni=4, WhatsApp=5). Most competitors use Talabat. Large chains also on Elmenus and Otlob. Smaller/informal competitors may use WhatsApp. Each competitor has 1–4 platform entries |

---

### TABLE 12: `Orders`
**Description:** The **central fact table** — the most important table for all analysis. Must be large, diverse, and analytically rich.
**Target size: 3,000–5,000 rows**

| Column | Description & Egyptian Values |
|---|---|
| OrderID | Auto-increment |
| CustomerID | FK to Customer. Many customers should have multiple orders (repeat buyers). Some are one-time. Show customer frequency diversity |
| PlatformID | FK to DeliveryPlatform. Distribute: Talabat ~45%, Elmenus ~22%, Otlob ~13%, Akelni ~8%, WhatsApp ~12% |
| ZoneID | FK to DeliveryZone. Must match the customer's ZoneID for that customer |
| OrderStatus | Values: 'Delivered' (~85%), 'Cancelled' (~8%), 'Refunded' (~4%), 'Pending' (~2%), 'Rejected' (~1%) |
| OrderDate | Between **2024-01-01 and 2025-12-31**. Show: higher volume Thursday/Friday (Egyptian weekend). Ramadan spikes post-Iftar (based on exact dates above). Summer slowdown (July–Aug lunch). Holiday peaks (Eid Al Fitr: Apr 2024, Mar/Apr 2025; Eid Al Adha: Jun 2024, Jun 2025) |
| OrderTime | Time of day. Distribution (normal days): Lunch (12:00–14:30): ~30%. Dinner (19:00–23:00): ~50%. Late night (23:00–01:00): ~10%. Other: ~10%. During Ramadan: shift heavily to Iftar window (**17:00–19:00**, not 9 PM) and Suhoor (02:00–04:00). Iftar window should represent ~50% of Ramadan-day orders |
| Subtotal_EGP | Sum of (Quantity × UnitPriceAtTime − Discount) for all items in the order. Range: 120–900 EGP for typical orders, up to 1,800+ for family meals. Average ~320 EGP |
| DeliveryFee_EGP | Minimum 20 EGP. Match the zone's DeliveryFee_EGP from Table 2. Apply **+10 EGP surcharge per category step** as follows: budget zone base 20–25 EGP → mid zone 30–35 EGP → premium zone 40–50 EGP. Show some 0 values for free delivery promotions (Ramadan promos, platform campaigns). WhatsApp orders: restaurant-set fee (20–35 EGP). Talabat/Elmenus/Otlob/Akelni: platform-collected fee |
| PlatformCommissionPercent | Talabat: 20–25%. Elmenus: 15–18%. Otlob: 15–20%. Akelni: 12–15%. WhatsApp: 0% |
| PlatformCommissionAmount_EGP | = Subtotal_EGP × (PlatformCommissionPercent / 100). Must be mathematically consistent |
| Tip_EGP | 0–50 EGP. ~60% are 0 (no tip common in Egypt). When given: typically 5, 10, 15, 20 EGP. Higher for large family orders |
| IsCOD | 1 for Cash on Delivery (~70–75% of orders). 0 for online payment (credit/debit card, wallet) |
| WasCODRefused | Only meaningful when IsCOD=1. ~8–12% of COD orders get refused. NULL when IsCOD=0 |

**Important patterns to encode:**
- Customers in lower-income zones (Ain Shams/Shubra, Haram Gardens, provincial cities): higher COD rate (~85%), higher refusal rate (~15%)
- Customers in affluent zones (Zamalek, New Cairo 5th Settlement, Maadi, Sheikh Zayed): more online payment (~50%), low refusal (~3%)
- Otlob and WhatsApp orders: higher COD refusal risk (~15%)
- Akelni orders: mid-tier COD refusal (~10%)
- New customers (first 2 orders): higher COD refusal risk
- Late-night orders: higher refusal risk
- Eid Al Adha: orders skew heavily toward meat items; family meals dominate; average order value +30%
- Ramadan: Qatayef and Kunafa always appear in Ramadan orders; dessert attach rate doubles

---

### TABLE 13: `OrderItem`
**Description:** Individual line items within each order. Each order has 1–5 items typically.
**Target size:** 7,000–15,000 rows (average ~2.5 items per order)

| Column | Description & Egyptian Values |
|---|---|
| OrderItemID | Auto-increment |
| OrderID | FK to Orders |
| ItemID | FK to MenuItem. Reflect realistic popularity: kofta, chicken shawarma, and koshari are top sellers. Family meals ordered more on weekends and Eid. Qatayef and Kunafa spike during Ramadan |
| Quantity | Usually 1–3. Family meals: always 1. Popular items like falafel/taameya: up to 5 |
| UnitPriceAtTime_EGP | Price at time of order — use the item's CurrentPrice_EGP adjusted for the ingredient cost at that month (since ingredient prices update monthly). Apply the 1.5x–2x margin rule consistently. Minor variance (±5%) allowed for promotions |
| DiscountApplied_EGP | 0 for most (~70%). When > 0: platform promotions (10–40 EGP discount). Ramadan promotions more common. WhatsApp orders rarely discounted |

---

### TABLE 14: `CODRefusalLog`
**Description:** Log of orders where cash-on-delivery was refused at the door. Directly tied to Orders where WasCODRefused=1.
**Target size:** 1 row per refused COD order (auto-calculated from Orders data)

| Column | Description & Egyptian Values |
|---|---|
| RefusalID | Auto-increment |
| OrderID | FK to Orders (only orders where WasCODRefused=1 and IsCOD=1) |
| RefusalReason | Egyptian-context reasons: 'Customer not home at delivery time', 'Customer changed their mind', 'Order amount higher than expected', 'Customer ordered from multiple places and chose another', 'No change available for large bills', 'Customer phone unreachable', 'Wrong address provided', 'Customer requested cancellation after dispatch', 'Customer disputes item quality without seeing it', 'Address not found' |
| RefusedAmount_EGP | = Subtotal_EGP + DeliveryFee_EGP for that order. Range: 120–1,800 EGP |
| RefusalDateTime | DATETIME combining OrderDate + OrderTime from the linked order, plus 30–90 minutes (delivery travel time) |

---

### TABLE 15: `CompetitorMenuItem`
**Description:** Competitor pricing intelligence — tracks how competitor restaurants price items similar to ours.
**Target size:** 150–300 rows

| Column | Description & Egyptian Values |
|---|---|
| CompetitorMenuItemID | Auto-increment |
| CompetitorID | FK to Competitor |
| YourItemID | FK to MenuItem — maps the competitor's item to the equivalent item on our menu |
| CompetitorItemName | Competitor's own item name in English. Use variations of the same dish: 'Mixed Grill Platter', 'Chicken Shawarma Wrap', 'Classic Kofta', 'Crispy Chicken', etc. |
| CompetitorPrice_EGP | Price of the equivalent item at the competitor. Often ±10–30% vs our price. KFC/McDonald's/Pizza Hut: fixed higher prices. Local competitors: similar or lower |
| IsOnPromotion | ~20% of tracked items are on promotion (IsOnPromotion=1). During Ramadan: more promotions |
| DateTracked | Dates from **2024-01-01 to 2025-12-31**, one entry per item per competitor per week or bi-weekly. Show price changes over time reflecting market inflation |

---

## DATA QUALITY REQUIREMENTS

1. **Referential integrity**: All FK values must reference valid existing PKs in parent tables.
2. **Mathematical consistency**: 
   - PlatformCommissionAmount_EGP must equal Subtotal_EGP × PlatformCommissionPercent / 100 (within EGP rounding).
   - RefusedAmount_EGP must match the linked order's financials.
   - MenuItem.CurrentPrice_EGP must be ≥ 1.5× the calculated ingredient cost at the item's reference date, plus PackagingCost.
   - UnitPriceAtTime_EGP in OrderItem must reflect the ingredient cost at that month's IngredientPrice, maintaining the 1.5–2.0× margin.
3. **Business logic consistency**: WasCODRefused can only be 1 when IsCOD=1. CODRefusalLog only references orders where WasCODRefused=1.
4. **Temporal consistency**: 
   - Customer.FirstOrderDate must be ≤ the earliest order date for that customer in the Orders table.
   - Customer.FirstOrderDate must fall between **2024-01-01 and 2025-06-30** to allow at least 6 months of tracking.
   - IngredientPrice.EffectiveDate must always be the 1st of each month.
   - Orders and CompetitorMenuItem dates must fall within **2024-01-01 to 2025-12-31**.
5. **Realistic distributions**: Don't generate uniformly random data — apply Egyptian market behavioral patterns described above, including the exact Ramadan and Eid dates provided.
6. **Full names rule**: FullName_AR and FullName_EN in Customer must **never be NULL or empty**. Every customer must have at least a two-part name (first + last). Anonymous platform orders are still assigned a reconstructed name based on available platform data.
7. **Analytical richness**: Ensure enough variation in zones, platforms, time periods, customer segments, and item combinations so that BI dashboards produce meaningful insights rather than flat trends.

---

## OUTPUT FORMAT

- Generate **one CSV file per table**, named exactly after the table (e.g., `City.csv`).
- First row must be the **column header row** using exact column names from the schema.
- Use **UTF-8 encoding** to support Arabic text.
- Use **comma as delimiter**; wrap fields containing commas or Arabic text in double quotes.
- **Date format**: YYYY-MM-DD. **Time format**: HH:MM:SS. **DateTime format**: YYYY-MM-DD HH:MM:SS.
- Decimal values: use period as decimal point (e.g., 120.50).
- BIT fields: use 1 or 0.
- NULL values: leave the field empty (no quotes, just empty between commas). Note: FullName fields must never be NULL.

---

## ⚠️ FIELDS TO MANUALLY VERIFY BEFORE USE

1. **DeliveryPlatform.CommissionRateDefault** — Platform commission rates are negotiated and change. Verify current Talabat, Elmenus, Otlob, and Akelni rates for Egyptian restaurants.
2. **IngredientPrice.PricePerUnit_EGP** — Ingredient prices are extremely volatile in Egypt due to inflation. Cross-check with current wholesale market prices.
3. **DeliveryZone.DeliveryFee_EGP and MinOrderForDelivery_EGP** — Adjust to reflect your restaurant's actual pricing policy per zone.
4. **MenuItem.CurrentPrice_EGP** — Replace with your actual menu prices after verifying the cost-margin calculation.
5. **Orders.PlatformCommissionPercent** — Verify the exact agreed commission rate in your Talabat, Elmenus, Otlob, and Akelni contracts.
6. **GoogleMapsRating for Competitor** — Verify against current Google Maps data for each listed competitor and zone.

---

*Generated for: Restaurant Delivery Profitability & Competitor Intelligence System — Egyptian Market Edition*
*Schema version: SQL Server 2019+*
*Prompt version: Adjusted v2 — Jan 2024–Dec 2025 data range*
