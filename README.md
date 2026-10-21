# MallDesk

MallDesk is a simple multi-store retail management application. A business can operate several branches, with staff assigned to one or more locations and given different levels of access. Staff can manage products and store users, while an AI assistant helps answer questions about the selected store.

## 🛠 Tech Stack
- **Backend:** Python, Django, Django REST Framework, PostgreSQL
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, React Query
- **Infrastructure:** Docker (for PostgreSQL)

## 🚀 Setup Instructions

### 1. Database (Docker)
Make sure Docker is running, then start the PostgreSQL container from the root directory:
```bash
docker compose up -d
```
**(If you don't have Docker, skip this step. The backend will automatically fall back to using SQLite)**

### 2. Backend(Django)
Open a terminal and navigate to the backend

```bash
cd backend
#for Mac/Linux
python3 -m venv .venv   #for windows use python -m venv  .venv && to activate .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
```
create your .env file(copy the example)
```bash
cp .env.example .env
```
Please Ensure the POSTGRES_PORT in .env matches the port in docker-compose.yml, which is 5433

#### Database Setup
Because the database migration files are included in this repository, you do not need to run makemigrations. Just run:
```bash
python manage.py migrate
python manage.py seed
```
The seed command will populate the database with the demo branches, users, and products

start the backend server:
```bash
python manage.py runserver
```
### 3. Frontend(React)
Open a new terminal and navigate to the frontend:
```bash
cd frontend
npm install
npm run dev
```
The app will be available at http://localhost:5173.

###  Demo Credentials
All seeded users have the password: password123

Username|Role	       | Downtown Flagship | Airport Terminal 2	| Westfield Mall
admin	|Administrator | ADMIN	           |  ADMIN	            | ADMIN
manager	|Store Manager | MANAGER	       |  ❌  No Access	   | ❌ No Access
staff	|Staff Member  | STAFF	           |  ❌ No Access	   | ❌ No Access
air_mgr	|Store Manager | ❌ No Access	  |  MANAGER	       | ❌ No Access
west_mgr|Store Manager | ❌ No Access	  |  ❌ No Access	  | MANAGER

Creating New Users:
If you use the "Assign Staff" form in the UI to create a new user (e.g., peter.parker), the system will automatically generate their email (peter.parker@malldesk.com), assign them the default password password123, and add them to the branch.


### Running Automated Tests
The backend includes automated tests proving the security and isolation rules requested in the brief.

To run the tests:
```bash
cd backend
source .venv/bin/activate
python manage.py test tests
```
### Test Coverage:

    1.Store Access (test_store_access.py): Proves users cannot view or change data for a store they are not assigned to.

    2.Role Permissions (test_role_permissions.py): Proves staff cannot create products, managers cannot assign users, and restricted actions return 403 Forbidden.

    3.Assistant Isolation (test_assistant_isolation.py): Proves the AI assistant only uses data from the active store and never leaks data from other branches.

    4.Combined Updates (test_combined_updates.py): Proves that if a Manager tries to update a product but includes a restricted field (like cost_price), the entire request is rejected (atomic transaction), ensuring no partial updates occur.

### Security & Business Logic Implemented
Store Isolation: Every API request checks the authenticated user's StoreMembership in the database before returning data. The frontend store ID is never trusted as proof of access.

Restricted Fields: cost_price and internal_notes are visible and editable only by Administrators. Managers are blocked on the server level.

Role Hierarchy: Managers can add new Staff, but cannot create Admins (enforced on both frontend and backend).

Atomic Transactions: All POST and PATCH requests use @transaction.atomic to guarantee that invalid data never partially saves.