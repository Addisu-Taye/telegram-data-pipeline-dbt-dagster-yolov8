 
# Development of an End-to-End Data Pipeline for Ethiopian Medical Telegram Channels

**Prepared by:** Addisu Taye Dadi  
**Date:** July 12, 2025   
---

## 1. Overview

This Github repo presents  developing a robust data pipeline targeting public Ethiopian medical Telegram channels. The pipeline enables automated **data extraction, transformation, enrichment, and analysis**, facilitating insights into:

- Frequently mentioned products  
- Posting frequency and trends  
- Media content classification  

---

## 2. Methodology Overview


###  Data Scraping & Collection (Extract + Load)

**Targeted Channels**:
-`@chemed123`
- `@lobelia4cosmetics`  
- `@tikvahpharma`  

**Tool Used**: [`Telethon`](https://github.com/LonamiWebs/Telethon)

**Artifacts**:

- Raw JSON: `data/raw/telegram_messages/YYYY-MM-DD/channel_name.json`  
- Images: `data/images/channel_name/`  

**Logging** tracks successful and failed scrapes, including rate-limit handling.

---

### Data Modeling & Transformation (Transform)

Using **dbt Core** with a **PostgreSQL** warehouse:

- JSON → `raw.telegram_messages` table  
- Staging models clean, normalize, and cast types  
- Star schema includes:

  - `dim_channels` – channel metadata  
  - `dim_dates` – time dimension  
  - `fct_messages` – fact table with FK relationships  

#### dbt Testing:

- Built-in: `not_null`, `unique`  
- Custom SQL: validate timestamp ranges, message integrity  

This modular setup supports reliable, extensible analytics.

---

## 3. Tools and Technologies

| Purpose              | Technology                    |
|----------------------|-------------------------------|
| Data Extraction       | Telethon                      |
| Data Storage          | PostgreSQL                    |
| Data Transformation   | dbt Core, dbt-postgres         |
| Containerization      | Docker, docker-compose         |
| Secret Management     | python-dotenv                 |

---



## 4. Conclusion

The project has established a strong foundation, enabling scalable, maintainable, and analyzable data flow from Telegram sources. The combination of **dbt, Docker, Telethon**, and **dimensional modeling** supports a future-ready data product.

With the ingestion + transformation layer operational, the next focus will be **visual enrichment**, **insight delivery**, and **workflow automation**.

---



