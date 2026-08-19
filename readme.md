# ExpenseOS

> An enterprise-grade Expense Management Platform built with Django REST
> Framework.

ExpenseOS is a role-based expense management system designed to manage
the complete reimbursement lifecycle --- from an employee submitting an
expense to manager approval and finance processing.

The project is being developed as a portfolio-grade backend application
with a strong focus on Django REST Framework, authentication,
authorization, workflow management, clean API design, and scalable
architecture.

## 🚀 Project Overview

ExpenseOS provides a centralized platform where organizations can:

-   Manage employees and organizational roles
-   Organize users by departments
-   Define expense categories
-   Submit and track reimbursement requests
-   Upload and associate receipts with expenses
-   Route expenses to the appropriate manager
-   Allow managers to approve or decline expenses
-   Provide finance managers with approved expenses for further
    processing
-   Track expense status throughout its lifecycle
-   Manage departmental budgets
-   Maintain a foundation for analytics, audit logs, OCR, and data
    imports

## 🎯 Main Goal

The primary goal of ExpenseOS is to replace manual or fragmented expense
reimbursement processes with a structured, secure, API-driven workflow.

The system is designed around this basic lifecycle:

``` text
Employee
   │
   ▼
Create Expense
   │
   ▼
Manager Review
   │
   ├── Declined ──► Rejected
   │
   └── Approved
          │
          ▼
     Finance Review
          │
          ▼
       Processing
          │
          ▼
       Reimbursed
```

## 👥 User Roles

ExpenseOS follows role-based access control.

### Employee

Employees can:

-   Create expense claims
-   Select an expense category
-   Enter amount, date, reason, and other details
-   Upload receipts
-   View their submitted expenses
-   Track reimbursement status

### Manager

Managers can:

-   View expenses submitted by employees under their responsibility
-   Review expense details and receipts
-   Approve expenses
-   Decline expenses
-   Participate in the approval workflow

### Finance Manager

Finance managers can:

-   View expenses approved by managers
-   Review approved reimbursement requests
-   Handle the finance-side processing workflow
-   Work with organizational/department-level financial information

### Admin

Administrators can manage:

-   Users
-   Roles
-   Departments
-   Expense categories
-   Managers
-   Finance managers
-   Budgets
-   Other system-level configuration

## 🏗️ Current Architecture

The backend is built using Django and Django REST Framework.

``` text
ExpenseOS/
│
├── manage.py
├── ExpenseOs/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
├── expenses/
├── receipt/
├── reimbursement/
├── notifications/
│
├── media/
├── requirements.txt
└── README.md
```

> App names and file organization may evolve as the project grows.

## 🛠️ Tech Stack

### Backend

-   Python 3.13+
-   Django
-   Django REST Framework
-   Django Channels
-   Simple JWT
-   SQLite during development
-   PostgreSQL-ready architecture for production

### Real-Time Communication

-   Django Channels
-   Redis
-   `channels_redis` as the Redis channel layer backend
-   WebSocket-based real-time notifications

### Containerization

-   Docker
-   Redis running as a Docker container during development

### API & Authentication

-   RESTful APIs
-   JWT Authentication
-   Access Tokens
-   Refresh Tokens
-   Role-Based Permissions
-   Django REST Framework permissions

### Development Tools

-   Git
-   GitHub
-   Postman
-   VS Code

## 🔐 Authentication

ExpenseOS uses JWT-based authentication.

The authentication flow is:

``` text
Login
  │
  ▼
JWT Access + Refresh Token
  │
  ├── Access Token → API Requests
  │
  └── Refresh Token → New Access Token
```

Example token endpoints:

``` http
POST /api/token/
POST /api/token/refresh/
```

Authenticated API requests use:

``` http
Authorization: Bearer <access_token>
```

## 📦 Core Domain Concepts

The system is centered around several important entities.

### User

Represents an organization member and contains role-related information.

### Department

Represents an organizational department.

Examples:

``` text
Engineering
Human Resources
Finance
Marketing
Operations
```

### Expense Category

Defines the type of expense.

Examples:

``` text
Travel
Food
Accommodation
Office Supplies
Transportation
Training
Software
```

### Expense

Represents an employee reimbursement request.

Typical information includes:

-   Employee
-   Department
-   Category
-   Amount
-   Date
-   Reason/description
-   Receipt
-   Manager
-   Finance manager
-   Status
-   Approval information

### Approval

Represents the review action performed during the expense approval
workflow.

Possible outcomes include:

``` text
Pending
Approved
Declined
```

### Budget

Represents the spending limit associated with an organizational unit or
department.

## 🔄 Expense Workflow

A typical expense moves through the following states:

``` text
PENDING
   │
   ▼
MANAGER REVIEW
   │
   ├──────────────► DECLINED
   │
   ▼
APPROVED
   │
   ▼
FINANCE REVIEW
   │
   ▼
PROCESSING
   │
   ▼
REIMBURSED
```

The exact status model can evolve as additional finance and
reimbursement functionality is implemented.

## 🔌 Real-Time Notification Architecture

ExpenseOS uses Django Channels and Redis alongside the normal REST API.

```text
                    ┌──────────────────┐
                    │     Frontend     │
                    └────────┬─────────┘
                             │
                    HTTP / WebSocket
                             │
                             ▼
              ┌──────────────────────────┐
              │ Django + DRF + Channels  │
              └────────────┬─────────────┘
                           │
              ┌────────────┴─────────────┐
              │                          │
              ▼                          ▼
        REST / Database          Notification Event
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │    Redis    │
                                  │    :6379    │
                                  └──────┬──────┘
                                         │
                                         ▼
                                  WebSocket Client
```

Redis acts as the communication layer for Django Channels. It is separate
from the application's relational database.

## 🌐 API Structure

The API is organized by application responsibility.

Example URL structure:

``` text
/api/
/api/token/
/api/token/refresh/
/api-auth/
```

Application-specific routes are grouped under their respective Django
apps.

For example:

``` text
/core/
```

for core/user-related functionality and:

``` text
/api/
```

for expense-related functionality.

## 🧪 API Testing

Postman can be used to test the API.

Recommended testing flow:

1.  Create/login as a user.
2.  Obtain the JWT access token.
3.  Add the access token as a Bearer token.
4.  Create the required department/category data.
5.  Create an employee expense.
6.  Verify that the expense is assigned to the appropriate workflow.
7.  Login as the responsible manager.
8.  Approve or decline the expense.
9.  Login as the finance manager.
10. Verify that approved expenses are available for finance processing.

## ⚙️ Installation

Follow these steps to run ExpenseOS locally.

### Prerequisites

Make sure the following are installed:

- Python 3.13+
- Git
- Docker Desktop
- Node.js/npm if you are also running the frontend

Docker is required for the Redis service used by Django Channels.

### 1. Clone the repository

```bash
git clone <repository-url>
cd ExpenseOS
```

### 2. Create and activate a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Redis with Docker

ExpenseOS uses Redis as the channel layer for Django Channels and real-time notifications.

If the Redis container already exists:

```bash
docker start expenseos-redis
```

If it does not exist yet:

```bash
docker run -d --name expenseos-redis -p 6379:6379 redis:latest
```

Verify that the container is running:

```bash
docker ps
```

You can also verify that Redis is responding:

```bash
docker exec -it expenseos-redis redis-cli ping
```

Expected output:

```text
PONG
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Start the Django backend

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

### Redis and Django Channels

Redis is not the database for ExpenseOS. It is used by Django Channels as the **channel layer** that allows different parts of the application to communicate through real-time messaging.

The current development configuration connects Channels to:

```text
127.0.0.1:6379
```

The relationship is:

```text
Frontend
    │
    │ HTTP / WebSocket
    ▼
Django + DRF + Channels
    │
    ├── REST APIs
    │
    └── Real-time notifications
             │
             ▼
        Redis :6379
```

For example, when an employee submits an expense, the expense can be persisted normally and the notification layer can use Redis/Channels to deliver a real-time notification to the appropriate user.

### Recommended development startup

Run Redis first:

```bash
docker start expenseos-redis
```

Then run Django:

```bash
python manage.py runserver
```

If Redis is unavailable, REST endpoints that trigger real-time notifications may raise a Redis connection error. Therefore, Redis should be running during normal local development.

## 🔧 Environment Variables

For production, sensitive configuration should be stored in environment
variables rather than committed to Git.

Example:

``` env
SECRET_KEY=your-secret-key
DEBUG=False

DB_NAME=expenseos
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

Never commit real credentials, secret keys, database passwords, or JWT
secrets to the repository.

## 📈 Planned Enterprise Features

ExpenseOS is intended to grow beyond a basic CRUD application.

Current functionality includes role-based expense management, approval
workflows, receipt handling, OCR support, and real-time notifications.
Additional enterprise functionality is planned, including:

### Advanced Approval Workflow

-   Multi-level approvals
-   Conditional approval rules
-   Approval delegation
-   Escalation mechanisms
-   Approval history

### Finance Management

-   Reimbursement processing
-   Payment status tracking
-   Finance reports
-   Budget utilization
-   Department-level spending analysis

### Analytics Dashboard

Potential metrics:

-   Total expenses
-   Approved expenses
-   Rejected expenses
-   Pending expenses
-   Department spending
-   Category-wise spending
-   Monthly expense trends
-   Budget utilization

### Receipt Upload & OCR

ExpenseOS includes receipt handling as part of the expense workflow.

Receipts can be uploaded and associated with expenses, and the OCR scanner is
used to extract useful information from receipt images.

Typical OCR data can include:

``` text
Merchant
Amount
Date
Tax
Invoice Number
Expense Category
```

OCR-extracted values are used to assist expense creation. Fields that represent
relationships in the database, such as `expense_category`, must ultimately
resolve to the corresponding database record rather than being stored as an
arbitrary category string.

### Audit Logs

The system can maintain an immutable history of important actions:

``` text
User
Action
Timestamp
Object
Previous Value
New Value
```

### Data Import

Future support may include importing expense data from:

-   CSV
-   Excel
-   External financial systems

### Notifications

ExpenseOS includes a notification layer for workflow events and real-time
updates.

The current real-time notification architecture uses:

-   Django Channels
-   Redis
-   WebSocket communication
-   In-app expense/approval status notifications

Additional notification channels such as email can be added as the project
evolves.

## 🧠 Engineering Focus

ExpenseOS is intentionally designed to demonstrate backend engineering
skills rather than simply building CRUD endpoints.

Important areas include:

-   Django project architecture
-   Django REST Framework
-   API design
-   Serializers and validation
-   Authentication
-   JWT
-   Custom permissions
-   Role-based authorization
-   Relational database modeling
-   Foreign key relationships
-   Approval workflows
-   Query optimization
-   Transactions
-   File uploads
-   Error handling
-   Pagination
-   Filtering and searching
-   Testing
-   Auditability
-   Production-oriented architecture

## 🔒 Security Considerations

Security is an important part of the project.

The application aims to enforce:

-   Authentication for protected endpoints
-   Role-based authorization
-   Object-level access control
-   Validation of user input
-   Secure file handling
-   Protection of sensitive configuration
-   Proper JWT handling
-   Restricted access to financial information

An employee should not be able to access another employee's private
expense data simply by changing an ID in the URL.

## 🧪 Future Testing Strategy

The project will progressively include automated tests for:

``` text
Authentication
Permissions
User roles
Expense creation
Expense validation
Approval workflow
Manager authorization
Finance authorization
Budget rules
Receipt uploads
API responses
Edge cases
```

Testing will eventually include unit tests, API tests, and integration
tests.

## 📌 Project Status

### Completed / In Progress

-   [x] Django project setup
-   [x] Core application
-   [x] User and role foundation
-   [x] JWT authentication
-   [x] Expense management foundation
-   [x] Approval workflow foundation
-   [x] Manager approval/decline flow
-   [x] Finance-side approved expense flow
-   [x] Receipt upload foundation
-   [x] OCR-based receipt scanning
-   [x] Django Channels integration
-   [x] Redis channel layer for real-time notifications

## 🤝 Contributing

This project is primarily being developed as a portfolio and learning
project.

If you want to contribute:

1.  Fork the repository.
2.  Create a feature branch.

``` bash
git checkout -b feature/your-feature
```

3.  Make your changes.
4.  Add tests where appropriate.
5.  Commit your changes.

``` bash
git commit -m "Add your feature"
```

6.  Push the branch.

``` bash
git push origin feature/your-feature
```

7.  Open a pull request.

## 📄 License

This project can be released under the MIT License.

If a different license is selected for the repository, update this
section accordingly.

## 👨‍💻 Author

**Prashant Shekhar**

ExpenseOS is being developed as a long-term backend-focused portfolio
project to demonstrate practical expertise in Django REST Framework and
enterprise application development.

------------------------------------------------------------------------

⭐ If you find the project useful, consider giving the repository a
star.
