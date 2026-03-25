# Cloud DevOpsSec Project Report

**Title:** Design, Secure Development, and CI/CD Deployment of a Cloud-Based Library Management System  
**Student Name:** [Your Name]  
**Student ID:** [Your Student ID]  
**Module:** Cloud DevOpsSec  
**Institution:** National College of Ireland  
**Submission Date:** [Insert Date]  

## Abstract
This project presents the design, implementation, security review, and deployment of a cloud-based Library Management System developed using Django. The application supports book management and borrowing workflows, including user input validation and CRUD operations. A GitHub Actions pipeline was configured to automate code checks and deployment to an Amazon EC2 instance. Static code analysis tools such as Flake8 and Bandit were integrated into the CI/CD workflow to support secure software development practices. The project also applied secure deployment improvements, including environment-based configuration, restricted host validation, and POST-only state-changing operations. The final system demonstrates the practical application of DevOps and DevSecOps principles across the software lifecycle.

**Keywords:** DevOps, DevSecOps, Django, GitHub Actions, EC2, CI/CD, static analysis, secure deployment

## I. Introduction
Modern cloud applications require more than functional correctness. They must also be maintainable, secure, and deployable through automated workflows. The purpose of this project was to develop a dynamic web application and deploy it to a public cloud platform using a full lifecycle CI/CD pipeline. In addition, the project aimed to apply secure development practices and static code analysis as part of the delivery process.

The implemented solution is a Library Management System (LMS) built with Django. The application allows users to add, update, delete, view, borrow, and return books. The project was deployed to an Amazon EC2 instance and managed through GitHub Actions for continuous integration and delivery.

This report evaluates the project against the module learning outcomes:

1. Critical analysis and implementation of static code analysis.
2. Planning and implementation of CI/CD for provisioning and deployment.
3. Evaluation and implementation of secure software development and secure execution in production.

## II. Project Overview
The application is a server-rendered Django web system designed for small-scale library inventory management. It enables library staff or users to manage books and track borrow records.

### A. Core Features
The implemented features are:

1. Add a new book.
2. View all books and borrow records.
3. Edit book details.
4. Delete a book.
5. Borrow a book.
6. Return a borrowed book.

### B. Dynamic Input Handling and Validation
The application accepts user input through Django forms. Validation is performed both by Django form handling and custom business logic. In particular, the borrowing process validates that the requested quantity does not exceed available stock. This prevents invalid transactions and protects data integrity.

### C. Data Storage
The project currently uses SQLite as the primary data store. SQLite is suitable for lightweight application development and demonstration projects because it is easy to configure and requires minimal operational overhead. However, for stronger production readiness and cloud scalability, PostgreSQL would be a better choice due to improved concurrency handling, operational robustness, and industry adoption in cloud deployments.

## III. System Design and Implementation
The project follows the standard Django Model-View-Template architecture.

### A. Data Model
Two core models were developed:

1. `Book`, which stores title, author, and available quantity.
2. `Borrow`, which stores the borrower name, related book, quantity borrowed, borrow date, and return status.

This design supports inventory tracking and borrowing operations while remaining simple and easy to maintain.

### B. Application Logic
The application logic is implemented in Django views. The `book_list` view retrieves books and borrowing records. The `add_book`, `edit_book`, and `delete_book` views provide CRUD functionality for books. The borrowing workflow reduces the available quantity of a selected book, while the return workflow restores stock and marks the borrow record as returned.

An additional security improvement was applied by enforcing `POST` for the return operation. This prevents state-changing actions from being triggered through a plain `GET` request.

### C. User Interface
The user interface is intentionally simple and functional. HTML templates are used to render book records, forms, deletion confirmation, and borrowing details. This lightweight interface is appropriate for demonstrating backend logic, validation, and cloud deployment without adding unnecessary frontend complexity.

## IV. Static Code Analysis and Secure Development
Static analysis was integrated to satisfy the secure software engineering requirements of the module.

### A. Flake8
Flake8 was added to check Python code style and potential quality issues. This supports code consistency, readability, and early detection of structural problems. Static linting is important in collaborative DevOps environments because poor code quality often leads to maintainability and deployment issues later in the lifecycle.

### B. Bandit
Bandit was integrated to perform security-oriented static analysis of the Python codebase. Bandit is valuable for identifying insecure coding patterns, weak defaults, and risky constructs before production release.

### C. Analysis of Current Implementation
The inclusion of Flake8 and Bandit demonstrates a valid approach to LO1. However, the current pipeline still uses `|| true`, meaning the workflow does not fail if these tools detect issues. This weakens the enforcement of secure coding standards. A stronger implementation would remove these bypasses so that the CI stage blocks unsafe or poor-quality changes.

### D. Secure Coding Improvements Applied
Several secure-development improvements were made during the project review:

1. The application now uses environment-based configuration for production settings.
2. `DEBUG` is configured through environment variables instead of being permanently enabled.
3. `ALLOWED_HOSTS` is handled through configuration to restrict incoming host headers.
4. The return action was changed to a `POST` request, reducing exposure to unsafe state changes.
5. Tests were added to validate key application behaviors and security-sensitive flows.

## V. CI/CD Pipeline Design
The project uses GitHub Actions to automate integration and deployment.

### A. Continuous Integration Stage
The CI stage is triggered on pushes to the `main` branch. It performs the following steps:

1. Checks out the source code.
2. Sets up Python 3.12.
3. Installs dependencies from `requirements.txt`.
4. Runs Flake8.
5. Runs Bandit.
6. Runs `python manage.py check`.

This structure provides an automated validation stage before deployment.

### B. Continuous Deployment Stage
After CI completes, the CD stage uses an SSH-based GitHub Action to connect to an EC2 instance and deploy the latest version of the application. The workflow performs the following actions:

1. Connects to the EC2 instance through SSH.
2. Navigates to the application directory.
3. Fetches the latest code from GitHub.
4. Verifies the existence of the `.env` file.
5. Creates a virtual environment if one is missing.
6. Installs Python dependencies.
7. Runs Django deployment checks.
8. Applies database migrations.
9. Collects static files.
10. Restarts the Gunicorn service.

This deployment process reflects a practical CI/CD lifecycle and addresses LO2 by automating update and release activities after code changes.

### C. CI/CD Challenges Encountered
During deployment, issues were encountered with SSH connectivity, EC2 host validation, and environment configuration. These issues included:

1. SSH timeout errors due to network or security group configuration.
2. Django `400 Bad Request` errors due to incorrect `ALLOWED_HOSTS`.
3. Incorrect `.env` formatting where Python code was mistakenly inserted instead of environment variables.

Resolving these issues highlighted the importance of infrastructure validation, secure secret management, and configuration separation between code and runtime environments.

## VI. Secure Deployment on AWS EC2
The application was deployed on Amazon EC2, which provides a flexible environment for hosting custom Django applications. The deployment strategy used Gunicorn as the application server. Access control and runtime configuration were managed through environment variables and AWS security settings.

### A. Production Configuration
The project uses environment variables for the following runtime values:

1. `SECRET_KEY`
2. `DEBUG`
3. `ALLOWED_HOSTS`

This is preferable to hardcoding sensitive values in the source code repository. It also supports safer separation between local development and production deployment.

### B. Security Considerations
The secure execution of the application in production was evaluated against basic web application security principles:

1. Django's default CSRF protection is retained for form submissions.
2. Host validation is enabled through `ALLOWED_HOSTS`.
3. Sensitive values are moved to `.env`.
4. State-changing actions were converted to `POST`.
5. Deployment checks are executed before migration and restart.

Although these measures improve the deployment posture, there is still room for enhancement. Examples include stricter pipeline failure rules, reverse proxy hardening with Nginx, HTTPS configuration, and migration to a more production-ready database engine.

## VII. Testing and Validation
Automated tests were added to validate the most important workflows in the application. These tests cover:

1. Loading the main book list page.
2. Creating a book record.
3. Updating a book record.
4. Deleting a book record.
5. Borrowing a book and reducing available quantity.
6. Rejecting an invalid borrow quantity.
7. Requiring `POST` for returns.
8. Returning a book and restoring quantity.

These tests improve confidence in the core behavior of the system and support safe code changes during future pipeline executions.

## VIII. Critical Evaluation
The project successfully demonstrates the foundation of a DevOpsSec workflow, but its maturity level is moderate rather than fully production-grade.

### A. Strengths
The project strengths include:

1. A functional dynamic Django application with validated user input.
2. Full CRUD support for book management.
3. Automated CI/CD pipeline using GitHub Actions.
4. Public cloud deployment using AWS EC2.
5. Integration of static code analysis tools.
6. Improved security posture through environment-based settings and safer request handling.

### B. Limitations
The current limitations include:

1. SQLite is not ideal for long-term cloud production use.
2. Static analysis is configured but not yet strictly enforced.
3. The deployment depends on SSH access and a preconfigured EC2 instance instead of full infrastructure-as-code.
4. HTTPS termination and reverse proxy hardening are not yet fully documented in this project.
5. The application interface is minimal and prioritizes function over user experience.

### C. Recommended Future Improvements
To improve the system further, the following steps are recommended:

1. Replace SQLite with PostgreSQL, preferably using Amazon RDS.
2. Remove `|| true` from Flake8 and Bandit so CI fails on detected issues.
3. Add infrastructure automation using Terraform or Ansible.
4. Configure Nginx with HTTPS and a domain name.
5. Expand automated tests to include integration and security-focused cases.
6. Add monitoring and logging for runtime observability.

## IX. Conclusion
This project demonstrates the implementation of a cloud-hosted dynamic web application with CI/CD automation and secure development considerations. The Django-based Library Management System satisfies the core functional requirements of user input handling, validation, CRUD operations, and database-backed persistence. The project also addresses the module's DevOpsSec focus by incorporating static analysis, automated deployment, and runtime hardening measures.

While the current solution is appropriate as an academic cloud DevOpsSec project, the evaluation also shows areas for enhancement, particularly around database choice, stricter pipeline enforcement, infrastructure automation, and production hardening. Overall, the project provides a practical and reflective demonstration of applying DevOps and security principles across the application lifecycle.

## References
[1] Django Software Foundation, "Django Documentation," 2026.  
[2] GitHub, "GitHub Actions Documentation," 2026.  
[3] Amazon Web Services, "Amazon EC2 Documentation," 2026.  
[4] OWASP Foundation, "OWASP Top 10: The Ten Most Critical Web Application Security Risks," 2021.  
[5] Python Software Foundation, "Python 3 Documentation," 2026.  
[6] OpenSSF, "Bandit Documentation," 2026.  
[7] PyCQA, "Flake8 Documentation," 2026.  
[8] Gunicorn Developers, "Gunicorn Documentation," 2026.  

## Appendix A. Submission Notes
Before final submission, replace the placeholders in this report and add the following evidence:

1. Your public application URL.
2. Screenshots of the application running on EC2.
3. Screenshots of a successful GitHub Actions pipeline run.
4. A short reflection on deployment issues encountered and how they were resolved.
