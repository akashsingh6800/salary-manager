# ACME Salary Management System — Architecture

## 1. Architecture Overview

The application will use a **modular monolith architecture** consisting of a React frontend, FastAPI backend, and PostgreSQL database.

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │   TypeScript + MUI   │
                    └──────────┬───────────┘
                               │
                            REST API
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │                      │
                    │  API / Routes        │
                    │  Services            │
                    │  Repositories        │
                    │  Validation          │
                    └──────────┬───────────┘
                               │
                           SQLAlchemy
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    │                      │
                    │  Employees           │
                    │  Salaries            │
                    │  Countries           │
                    │  Departments        │
                    └──────────────────────┘
```

## 2. Technology Stack

### Frontend

* React
* TypeScript
* Material UI
* REST API integration

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic

### Database

* PostgreSQL

### Testing

* Pytest for backend
* React Testing Library for frontend

### Deployment

* Docker
* Docker Compose for local development
* Cloud deployment for the final application

---

## 3. Backend Structure

The backend will follow a simple separation of responsibilities:

```text
API Layer
   ↓
Service Layer
   ↓
Repository / Data Access Layer
   ↓
Database
```

### API Layer

Responsible for:

* HTTP endpoints
* Request/response handling
* Input validation
* HTTP status codes

### Service Layer

Contains business logic such as:

* Determining current salary.
* Creating salary history records.
* Employee filtering logic.
* Compensation calculations.

### Repository Layer

Responsible for database operations such as:

* Fetching employees.
* Saving salary records.
* Querying salary history.
* Running database aggregations.

### Models

SQLAlchemy models will represent the database entities.

### Schemas

Pydantic schemas will define and validate API request and response structures.

---

## 4. Database Design

The application will initially use four main entities:

```text
Country
   │
   └──────< Employee >────── Department
                    │
                    │
                    └──────< SalaryHistory
```

### Countries

Stores supported countries.

Fields:

* id
* name
* code

### Departments

Stores organization departments.

Fields:

* id
* name

### Employees

Stores employee information.

Fields:

* id
* employee_id
* first_name
* last_name
* email
* country_id
* department_id
* job_title
* employment_status
* created_at
* updated_at

### Salary History

Stores historical employee compensation.

Fields:

* id
* employee_id
* salary
* currency
* effective_from
* created_at

An employee can have multiple salary history records.

This prevents salary updates from destroying historical compensation information.

---

## 5. Salary Design

Salary information will be stored separately from the employee record.

For example:

```text
Employee: EMP001

Salary History
--------------------------------
2024-01-01    80,000 USD
2025-01-01    90,000 USD
2026-01-01   100,000 USD
```

The current salary will be determined from the latest salary record whose effective date is not in the future.

This design allows the application to preserve historical compensation changes.

---

## 6. API Design

The backend will expose REST APIs under `/api/v1`.

### Employee APIs

```text
GET /api/v1/employees
GET /api/v1/employees/{id}
```

The employee list will support:

* Search
* Country filtering
* Department filtering
* Employment status filtering
* Pagination

### Salary APIs

```text
GET  /api/v1/employees/{id}/salary-history
POST /api/v1/employees/{id}/salary
```

### Analytics APIs

```text
GET /api/v1/analytics/overview
GET /api/v1/analytics/by-country
GET /api/v1/analytics/by-department
GET /api/v1/analytics/distribution
```

---

## 7. Performance Considerations

The initial dataset contains approximately 10,000 employees.

The application will therefore:

* Use server-side pagination for employee lists.
* Perform search and filtering at the database level.
* Add indexes to commonly searched and filtered fields.
* Use database aggregation for analytics.
* Avoid loading all employee records into application memory.

Examples of database operations used for analytics include:

```text
COUNT
AVG
MIN
MAX
GROUP BY
```

---

## 8. Architecture Decision — Modular Monolith

A modular monolith is intentionally chosen instead of microservices.

The expected dataset of approximately 10,000 employees does not require the operational complexity of multiple independently deployed services.

The modular structure still keeps API, business logic, and data access separated, making the application easier to maintain and allowing individual modules to be extracted into services in the future if the product grows significantly.

---

## 9. Currency Handling

Employees may have salaries in different currencies.

The application will store:

```text
salary
currency
```

together.

The MVP will not use live exchange rates.

Analytics will avoid combining values from different currencies without conversion.

A currency conversion service can be introduced later if cross-country normalized compensation analysis becomes a requirement.
