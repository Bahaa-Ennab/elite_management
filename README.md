🦷 Elite Smile Dental Clinic
A modern, responsive web application to manage dental clinic operations, streamline appointments, and facilitate communication between doctors and patients.

📌 Project Name:
Elite Smile

🛠️ Technologies Used
Backend: Django (Python)

Frontend: HTML, Tailwind CSS, JavaScript, AJAX

Database: MySQL

Other Tools: Django Sessions, Django Messages, Django Templates, Date Filtering, Class-Based & Function-Based Views

🧱 Project Structure (Apps)
patient: Handles patient-related features and UI

doctor: Handles doctor-related features and UI

🖥️ Pages Overview
Public Home Page:
Navigation: Home, Services, Blog, Contact Us, About, Login
Includes clinic introduction and general info

Login Page:
Shared login form for both patients and doctors
Auto-redirects based on user type

Patient Dashboard:

Book appointments

View upcoming/past appointments

See treatment history

Edit personal details

Logout

Doctor Dashboard:

View today’s appointment count and list

Access detailed patient profiles

Patient Details (Doctor view):

Info: Name, ID, Phone, Address, DOB, Gender, Blood type, etc.

Full medical history

Back button to return to previous page

All Patients Page (Doctor):

List of registered patients

Appointments Page (Doctor):

View all appointments

Filter by date range (e.g., weekly, monthly)

🧩 Core Models & Relationships
Patient: name, national ID, phone, address, DOB, medical condition, blood type, smoker, etc.

Doctor: name, specialty, phone

Appointment: Foreign keys to Patient and Doctor, plus date, time, and reason

MedicalRecord: Foreign key to Patient, optional FK to Doctor, date, and notes

🔐 Authentication System
Single login for both roles

Role detection and dashboard redirection

Strict role-based access control

💎 Key Features
Smart login with user-type recognition

Real-time doctor dashboard

Appointment booking and filtering

Full patient history and profile access

Role-based access control

Responsive and user-friendly UI

🌍 Why It Matters
Eliminates manual paperwork and scheduling

Improves doctor-patient communication

Digitally organizes clinic operations

Instant access to patient records

🖋️ Typography
Arabic Support: Cairo or Tajawal

English Support: Inter or Roboto

🎨 UI/UX Stack
Tailwind CSS: Responsive modern styling

JavaScript + AJAX: Interactive UI updates

Mobile-Friendly: Fully responsive design

Let me know if you'd like a badge section (for build, license, etc.) or contribution guidelines added!
