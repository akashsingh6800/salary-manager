# Engineering Tradeoffs

## 1. Modular Monolith vs Microservices

### Decision
Use a modular monolith for the application.

### Reasoning
The system is primarily an employee salary management application with a relatively focused domain. A modular monolith keeps deployment and development simple while allowing clear separation between employee management, salary management, and analytics.

Microservices would introduce additional operational complexity without providing meaningful benefits at the current scale.

---

## 2. PostgreSQL vs NoSQL

### Decision
Use PostgreSQL as the relational database.

### Reasoning
Employee, department, country, and salary history data have clear relationships and require structured queries and aggregations.

PostgreSQL provides strong consistency, relational integrity, indexing, and efficient aggregation capabilities.

---

## 3. Salary History vs Overwriting Salary

### Decision
Store salary changes as historical records instead of overwriting the existing salary.

### Reasoning
HR needs visibility into how employee compensation has changed over time. Keeping salary history provides an audit-friendly record and allows historical compensation analysis.

The analytics APIs use the latest effective salary when calculating current compensation metrics.

---

## 4. Currency Conversion

### Decision
Do not perform currency conversion.

### Reasoning
Employees can be paid in different currencies. Converting salaries would require exchange-rate sources and introduce additional assumptions around exchange-rate dates.

Instead, analytics are grouped by currency so that salaries are only compared within the same currency.

---

## 5. Authentication and Authorization

### Decision
Authentication and role-based access control are intentionally excluded from the assessment implementation.

### Reasoning
The assessment focuses on salary management functionality, backend engineering, database design, analytics, testing, and product thinking.

In a production implementation, authentication, authorization, audit logging, and integration with the organization's identity provider would be required.

---

## 6. Background Processing

### Decision
Use synchronous API operations rather than introducing a task queue.

### Reasoning
Salary updates and employee queries are short database operations and do not require asynchronous processing.

Introducing Celery, Redis, or another queue would add infrastructure complexity without improving the core use case.

---

## 7. API Pagination

### Decision
Paginate employee results.

### Reasoning
The organization has 10,000 employees, and returning the entire employee dataset to the browser would increase response size and frontend rendering cost.

The API therefore supports pagination and search so that the UI only retrieves the required records.