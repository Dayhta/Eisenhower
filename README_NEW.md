# Eisenhower Matrix Todo App

A full-stack web application for task management using the Eisenhower Matrix methodology. This app helps users prioritize tasks based on urgency and importance, with advanced scoring algorithms and automated ranking.

## ✅ Current Status

**WORKING AND TESTED:**
- ✅ Backend API (FastAPI with SQLite)
- ✅ Database models and migrations
- ✅ Task CRUD operations
- ✅ Priority scoring algorithm
- ✅ Eisenhower Matrix data endpoints
- ✅ Frontend React application
- ✅ Docker containerization
- ✅ Multi-environment configuration
- ✅ Security headers and input validation
- ✅ Rate limiting

## 🏗️ Architecture

### Backend (FastAPI + SQLite)
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database (persistent via Docker volumes)
- **Pydantic** - Data validation and serialization

### Frontend (React)
- **React 18** - Component-based UI framework
- **Axios** - HTTP client for API communication
- **Responsive Design** - Mobile-friendly interface

### Infrastructure
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy (production)
- **Environment-based deployment** - dev/staging/production

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd eisenhower-matrix-app
   ```

2. **Start development environment:**
   ```bash
   # Copy development environment
   cp .env.development .env
   
   # Start all services
   docker-compose --profile dev up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

### Production Setup

1. **Set production environment:**
   ```bash
   cp .env.production .env
   ```

2. **Deploy with production profile:**
   ```bash
   docker-compose --profile prod up -d --build
   ```

## 📊 Features

### Task Management
- Create, read, update, delete tasks
- Rich task properties:
  - Title and description
  - Urgency (1-10 scale)
  - Importance (1-10 scale)
  - Impact (1-10 scale)
  - Value alignment (1-10 scale)
  - Effort estimation (1-10 scale)
  - Due dates
  - Automatic priority scoring

### Eisenhower Matrix
- Automatic categorization into 4 quadrants:
  - **Quadrant 1**: Urgent + Important (Do First)
  - **Quadrant 2**: Important + Not Urgent (Schedule)
  - **Quadrant 3**: Urgent + Not Important (Delegate)
  - **Quadrant 4**: Not Urgent + Not Important (Eliminate)

### Advanced Priority Scoring
Configurable algorithm considering:
- Urgency weight (default: 30%)
- Importance weight (default: 30%)
- Impact weight (default: 20%)
- Value alignment weight (default: 20%)
- Effort penalty (default: 15% penalty)
- Due date proximity bonus

## 🔒 Security Features

- **Input Validation**: Comprehensive validation of all user inputs
- **XSS Protection**: HTML tag filtering and sanitization
- **Rate Limiting**: 100 requests per minute per IP
- **Security Headers**: OWASP recommended HTTP headers
- **CORS Configuration**: Restricted cross-origin requests
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries

## 🛠️ Configuration

### Environment Variables

```bash
# Deployment target
TARGET=development|staging|production
NODE_ENV=development|staging|production

# Priority Algorithm Weights
WEIGHT_URGENCY=0.30
WEIGHT_IMPORTANCE=0.30
WEIGHT_IMPACT=0.20
WEIGHT_VALUE=0.20
EFFORT_PENALTY=0.15
DUE_SOON_DAYS=5
DUE_SOON_MAX_BONUS=0.15

# Frontend API Configuration
REACT_APP_API_BASE=http://localhost:8000/api  # or /api for production
```

## 📡 API Endpoints

### Tasks
- `GET /api/tasks/` - List all tasks with rankings
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Matrix Data
- `GET /api/tasks/matrix/data` - Get tasks organized by Eisenhower quadrants

### System
- `GET /api/health` - Health check endpoint
- `GET /` - Root API information

## 🧪 Testing

### Backend API Testing
```bash
# Health check
curl http://localhost:8000/api/health

# Create a task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Important Task",
    "description": "This needs attention",
    "urgency": 8,
    "importance": 9
  }'

# Get matrix data
curl http://localhost:8000/api/tasks/matrix/data
```

### Frontend Testing
The React application includes the following components:
- Task creation form with validation
- Eisenhower Matrix grid visualization
- Task list with priority rankings
- Responsive design for mobile/desktop

## 🔧 Development

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic
python -m app.start
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

### Database Management
- Database file: `backend/tasks.db` (development)
- Docker volume: `sqlite_data` (containerized)
- Automatic migrations via SQLAlchemy

## 📁 Project Structure

```
eisenhower-matrix-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── security.py          # Security utilities
│   │   ├── settings.py          # Application settings
│   │   ├── start.py            # Development server
│   │   ├── models/
│   │   │   └── task.py         # Database models
│   │   ├── routers/
│   │   │   ├── tasks.py        # Task API endpoints
│   │   │   └── config.py       # Configuration endpoints
│   │   └── schemas/
│   │       └── task.py         # Pydantic schemas
│   ├── Dockerfile              # Backend container
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/
│   │   │   └── api.js         # API client
│   │   └── App.js             # Main application
│   ├── Dockerfile             # Frontend container
│   └── package.json           # Node.js dependencies
├── nginx/
│   └── default.conf           # Nginx configuration
├── docker-compose.yml         # Container orchestration
├── .env.development           # Development environment
├── .env.staging              # Staging environment
├── .env.production           # Production environment
└── README.md                 # This file
```

## 🎯 Next Steps & Improvements

### Potential Enhancements
1. **Authentication System**
   - User registration/login
   - JWT token-based auth
   - User-specific tasks

2. **Advanced Features**
   - Task categories/tags
   - Collaborative workspaces
   - Task dependencies
   - Time tracking
   - Notifications

3. **Infrastructure**
   - Database backup/restore
   - Monitoring and logging
   - CI/CD pipeline
   - Performance optimization

4. **Mobile App**
   - React Native mobile client
   - Push notifications
   - Offline functionality

## 📝 License

This project is created for demonstration purposes. See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For questions and support, please open an issue in the repository.
