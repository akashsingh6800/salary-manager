# Performance Considerations

## Employee Search and Pagination

Employee records are retrieved using server-side pagination. The API limits page size to avoid returning thousands of records in a single request.

Search is performed at the database level using indexed employee identifiers and email fields where applicable.

---

## Database Indexing

Indexes are used on frequently queried columns, including:

- `employees.employee_id`
- `employees.email`
- `employees.country_id`
- `employees.department_id`
- `employees.employment_status`
- `salary_history.employee_id`
- `salary_history.effective_from`

These indexes reduce lookup and filtering costs as the employee population grows.

---

## Analytics Queries

Analytics use database-side aggregation rather than loading all employee and salary records into application memory.

Current salary analytics first identify the latest salary record for each employee and then perform aggregation.

Salary averages are grouped by currency because salaries in different currencies cannot be meaningfully averaged without an exchange-rate assumption.

---

## API Response Size

Employee list APIs return only the fields required by the employee list UI and use pagination.

This keeps network payloads and browser rendering work bounded even with 10,000 employees.

---

## Seed Data

The seed process generates 10,000 deterministic employees.

Deterministic data makes development, testing, and demonstrations repeatable while avoiding the need for external data sources.

---

## Potential Future Optimizations

If the system grows significantly beyond the assessment scale, potential optimizations include:

- Database query-plan analysis and additional targeted indexes.
- Caching frequently accessed analytics.
- Precomputed/materialized analytics for expensive reporting queries.
- Read replicas for reporting workloads.
- Background processing for long-running reporting operations.

These optimizations are intentionally not included in the current implementation because the assessment scale does not require the additional infrastructure complexity.