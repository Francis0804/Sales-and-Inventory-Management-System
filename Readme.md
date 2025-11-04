# 🛒 Sales and Inventory Management System

## 📘 Short Description
The **Sales and Inventory Management System** is a Django-based web application designed to automate sales recording, inventory tracking, and reporting for business operations.  
It ensures **accuracy, efficiency, and real-time monitoring** of product quantities, supplier transactions, and sales performance, helping businesses manage operations more effectively.

---

## ✨ Key Features

### 🧾 Product and Inventory Management
- Add, update, and delete product records (code, name, category, supplier, price).
- Track inventory quantities in real-time.
- Automatically update stock levels after sales or restocking.
- Notify when product stock reaches reorder level.

### 💰 Sales Transaction Processing
- Record and process sales transactions.
- Automatically calculate **12% VAT tax**, total amount, and customer change.
- Generate **Sales Receipts** for every transaction.
- Automatically reduce product quantity after each sale.

### 📦 Purchase and Restocking Management
- Record restocking and supplier purchase transactions.
- Automatically update inventory upon receiving new stock.
- Generate **Purchase Orders (PO)** for documentation.

### 🧑‍🤝‍🧑 Supplier Management
- Store supplier details (name, contact, email, address).
- Track supplier transaction history.

### 📊 Reports and Analytics
- Generate daily, weekly, and monthly sales summaries.
- Display inventory status and fast/slow-moving items.
- Generate **Profit & Loss summaries**.
- Export reports in **PDF** or **Excel** format.

### 🔐 User Account and Role Management
- Multiple user roles:
  - **Administrator** — full access to all records and reports.
  - **Cashier** — can record sales transactions.
  - **Inventory Clerk** — manages products and restocks.
- Role-based permissions using Django’s built-in authentication system.

### 🔍 Search and Filtering
- Search by product name, category, or code.
- Filter reports and transactions by date, type, or status.

### 💾 Backup and Data Security
- Regular database backups for data recovery.
- Secure password encryption (PBKDF2).
- Restricted access to authorized users only.

---

## 🧩 Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Framework** | Django 5.2.7 |
| **Language** | Python 3.13 |
| **Database** | SQLite (Dev) / PostgreSQL (Production) |
| **Frontend** | HTML, CSS (Bootstrap), Django Templates |
| **Reporting** | ReportLab (PDF), OpenPyXL (Excel) |
| **Fake Data Generator** | Faker |
| **Deployment Platform** | PythonAnywhere |
| **Version Control** | Git & GitHub |

