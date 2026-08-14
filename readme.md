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
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── expenses/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── approvals/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── media/
│
├── requirements.txt
└── README.md
```

> App names and file organization may evolve as the project grows.

## 🛠️ Tech Stack

### Backend

-   Python
-   Django
-   Django REST Framework
-   Simple JWT
-   SQLite during development
-   PostgreSQL-ready architecture for production

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

### 1. Clone the repository

``` bash
git clone <repository-url>
cd ExpenseOS
```

### 2. Create a virtual environment

Windows:

``` bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Apply migrations

``` bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an admin user

``` bash
python manage.py createsuperuser
```

### 6. Start the development server

``` bash
python manage.py runserver
```

The API will then be available at:

``` text
http://127.0.0.1:8000/
```

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

Planned functionality includes:

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

### Receipt OCR

Future OCR functionality can extract information from uploaded receipts
such as:

``` text
Merchant
Amount
Date
Tax
Invoice Number
```

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

Possible notification channels:

-   Email
-   In-app notifications
-   Approval reminders
-   Expense status updates

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
-   [ ] Advanced finance processing
-   [ ] Budget management
-   [ ] Analytics
-   [ ] Audit logs
-   [ ] OCR receipt processing
-   [ ] Notifications
-   [ ] Automated test suite
-   [ ] Production deployment

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
