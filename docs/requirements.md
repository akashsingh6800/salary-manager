# Salary Management System - Requirements

## 1. Goal 

Build a web-based salary management system for ACME that replaces spreadsheet-based salary management and enables the HR Manager to efficiently manage employee compensation data for approximately 10,000 employees across multiple countries.

The system should allow HR to manage salary information, preserve salary history, and quickly answer questions about how the organization pays its employees. 

## 2. User 

### Primary User - HR Manager 

The HR Manager will use the system to:

* Search and view employee information
* Filter employees by country, department, and employment status.
* View current salary and salary history.
* Update employee salary information.
* Analyze salary information across countries and departments.

The initial version focuses on the HR Manager as the only user persona.

## 3. Features

### Employee Management

* View a paginated list of employees.
* Search employees by employee ID or name.
* Filter by country, department, and employment status.
* View employee details


### Salary Mangement 

* View an employee's current salary.
* View salary history.
* Add/update salary information.
* Store salary amount, current, and effective date.
* Preserce previous salary records when salary is updated.

### Compensation Analytics 

Provide a dashboard showing:

* Total number of employees. 
* Salary statistics.
* Employee count by country.
* Salary information by country.
* Employee count by department.
* Salary information by department.
* Salary-range distribution.

The system will retain salaries in their original currency. Salary values from different currencies will not be directly combined unless a valid currency conversion mechanism is introduced.

### Data Seeding

* Provide a seed script that generates approximately 10,000 employees. 
* Generates realistic countries, departments, job titles, employment statuses, salaries, currencies, and salary history.
* Seed data should be deterministic and repeatable.


## Out of Scope

The following are intentionally excluded from the initial version:

### Payroll Processing

Taxes, deductions, bonuses, payslips, and payroll payments.

### Employee Self-Service

Employees will not directly access or modify their salary information.

Reason: The assessment defines the HR Manager as the primary user.

### Enterprise SSO 

Okta, Azure AD, or other enterprise authentication integrations.

Reason: Authentication is not central to demonstrating the core product workflow and can be added later.

### Excel Import/Export

Bulk Excel upload and download.

Reason: The initial goal is to replace spreadsheet-based management with a structured application. Import/export can be added as a future enhancement.

### Real-Time Currency Conversion

Live foreign-exchance rate integration.

Reason: This introduces and external dependency and additional complexity that is not required for the core MVP.

AI Chatbot

A generative-AI chatbot for querying salary data.

Reason: The initial analytics requirements can be reliably handled using deterministic database queries. An AI-based interface can be considered as a future enhancement.


## Success Criteria 

The solution will be considered successful if the HR Manager can:

* Find an employee quickly using search and filters. 
* View employee and current salary information.
* Update and employee's salary without losing previous salary history.
* View salary information by country and department.
* Understand overall compensation patterns through the dashboard. 
* Manage the initial dataset of approximately 10,000 employees through the web application.
* Use the application through a deployed end-to-end web interface. 
* Run the application's automated tests successfully.

The solution should demonstrate clean code structure, appropriate database design, meaningful test coverage, and a maintable architecture.

