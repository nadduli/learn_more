# Learn More API

A production-ready FastAPI authentication and user management system with JWT tokens, role-based access control, and PostgreSQL database.

## 🚀 Features

- ✅ **User Authentication** - Register, login, and token-based authentication
- ✅ **JWT Tokens** - Secure access tokens with configurable expiration
- ✅ **Role-Based Access Control** - User and Admin roles
- ✅ **Password Security** - Argon2 password hashing
- ✅ **Async Database** - PostgreSQL with async SQLAlchemy
- ✅ **Database Migrations** - Alembic for schema management
- ✅ **Repository Pattern** - Clean architecture with service layer
- ✅ **API Documentation** - Auto-generated OpenAPI/Swagger docs

## 📋 Requirements

- Python 3.12+
- PostgreSQL database
- UV package manager (recommended) or pip

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd learn_more
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
SECRET_KEY=your_secret_key_here_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_STR=/api/v1
```

### 3. Install dependencies

Using UV (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Seed initial roles

```bash
python -m app.db.init_db
```

This creates the default `user` and `admin` roles.

## 🏃 Running the Application

### Development mode

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register a new user | No |
| POST | `/api/v1/auth/login` | Login and get access token | No |
| GET | `/api/v1/auth/me` | Get current user info | Yes |
| POST | `/api/v1/auth/refresh` | Refresh access token | Yes |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/users/me` | Get current user profile | Yes |

## 🔐 Authentication Flow

### 1. Register a new user

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "role_id": "your-role-uuid-here"
  }'
```

### 2. Login to get access token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Use the token for authenticated requests

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🗄️ Database Schema

### Users Table
- `id` - UUID (Primary Key)
- `email` - String (Unique)
- `hashed_password` - String
- `full_name` - String
- `phone` - String (Optional)
- `is_verified` - Boolean
- `is_active` - Boolean
- `role_id` - UUID (Foreign Key to roles)
- `created_at` - DateTime
- `updated_at` - DateTime

### Roles Table
- `id` - UUID (Primary Key)
- `name` - String (Unique)
- `created_at` - DateTime
- `updated_at` - DateTime

## 🏗️ Project Structure

```
learn_more/
├── app/
│   ├── api/
│   │   ├── deps.py              # Shared dependencies
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py      # Authentication endpoints
│   │           └── users.py     # User management endpoints
│   ├── core/
│   │   ├── config.py            # Configuration settings
│   │   └── security.py          # Password hashing & JWT
│   ├── db/
│   │   ├── database.py          # Database connection
│   │   ├── init_db.py           # Database seeding
│   │   └── repositories/
│   │       └── user_repository.py
│   ├── models/
│   │   ├── base.py              # Base model with timestamps
│   │   ├── role.py              # Role model
│   │   └── user.py              # User model
│   ├── schemas/
│   │   ├── token.py             # Token schemas
│   │   └── user.py              # User schemas
│   ├── services/
│   │   └── user_service.py      # User business logic
│   └── main.py                  # FastAPI application
├── alembic/                     # Database migrations
├── main.py                      # Application entry point
├── pyproject.toml               # Project dependencies
└── .env                         # Environment variables
```

## 🧪 Getting Role IDs

To get the role IDs for registration, you can query the database or use the seeding script output:

```bash
python -m app.db.init_db
```

This will print the role IDs:
```
INFO:__main__:Created 'user' role with ID: 123e4567-e89b-12d3-a456-426614174000
INFO:__main__:Created 'admin' role with ID: 123e4567-e89b-12d3-a456-426614174001
```

## 🔧 Development

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

## 🚀 Next Steps

Phase 1 is complete! Here's what you can implement next:

- [ ] Email verification flow
- [ ] Password reset functionality
- [ ] Admin endpoints for user management
- [ ] User listing with pagination
- [ ] CORS configuration
- [ ] Rate limiting
- [ ] Request logging
- [ ] Unit and integration tests

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
