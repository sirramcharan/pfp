# pfp

# 💎 FinSight Pro — Personal Finance Dashboard

A production-ready, glassmorphism-themed Streamlit dashboard built for portfolio/interview showcase.

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
app.py            ← Single-file app (modular functions inside)
requirements.txt  ← Python dependencies
.streamlit/
  secrets.toml    ← Google Sheets credentials (create this yourself — never commit!)
```

---

## 🔌 Swapping in Google Sheets

1. Create a Google Cloud project and enable the **Sheets API** and **Drive API**.
2. Create a **Service Account** and download the JSON key.
3. Share your Google Sheet with the service account email.
4. Create `.streamlit/secrets.toml`:

```toml
[gcp_service_account]
type                        = "service_account"
project_id                  = "your-project-id"
private_key_id              = "key-id"
private_key                 = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
client_email                = "your-sa@your-project.iam.gserviceaccount.com"
client_id                   = "123456789"
auth_uri                    = "https://accounts.google.com/o/oauth2/auth"
token_uri                   = "https://oauth2.googleapis.com/token"
```

5. In `app.py`, replace `load_dummy_data(user_profile)` with `load_gsheets_data(user_profile)` and uncomment that function.

---

## 📊 Expected Google Sheet Format

| date       | category         | amount   | type    |
|------------|------------------|----------|---------|
| 2024-01-01 | Salary           | 120000   | Income  |
| 2024-01-01 | Rent             | 30000    | Expense |
| 2024-01-01 | Mutual Funds SIP | 15000    | Savings |

Each user profile = one worksheet tab in the same Google Spreadsheet.

---

## 🎨 Theme

Glassmorphism — dark navy/purple gradient background with frosted-glass cards:
- `backdrop-filter: blur(12px)`  
- `rgba(255,255,255,0.05)` backgrounds  
- Subtle white semi-transparent borders  
- Animated ambient orbs  

---

## 💡 Interview Talking Points

| Feature | Concept to Explain |
|---|---|
| `@st.cache_data` | Avoids re-querying Google Sheets on every widget interaction |
| Sankey Diagram | Flow visualisation: income → buckets → leaf categories |
| Anomaly Detection | Rolling 3-month SPC rule — shift(1) prevents look-ahead bias |
| Confidence Band | ±2% CAGR sensitivity shows quantitative thinking |
| 80C Tracker | Indian IT Act Section 80C — ₹1.5L deduction limit |
