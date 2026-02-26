# Design Document

## Overview

KrishiAI is an AI-powered Agriculture & Rural Development platform designed as a distributed system with three primary client applications (React Native mobile app, React web dashboard) communicating with a FastAPI backend that orchestrates ML inference, database operations, and external service integrations. The architecture prioritizes offline-first mobile experience, horizontal scalability, and modular service design.

### Key Design Principles

- **Offline-First**: Mobile app uses on-device TFLite models for core disease detection
- **Modular Architecture**: Clear separation between API layer, business logic, data access, and ML services
- **Scalability**: Stateless backend services, cloud storage, and containerized deployment
- **Security**: JWT authentication, input validation, rate limiting, and encrypted data storage
- **Observability**: Structured logging, health checks, and metrics exposure

## Architecture

### High-Level System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Mobile[React Native Mobile App]
        Web[React Web Dashboard]
    end
    
    subgraph "API Gateway Layer"
        Gateway[API Gateway / Load Balancer]
    end
    
    subgraph "Application Layer"
        FastAPI[FastAPI Backend]
        Auth[Auth Service]
        ML[ML Inference Service]
        Weather[Weather Service]
        Chatbot[Chatbot Service]
    end
    
    subgraph "Data Layer"
        Postgres[(PostgreSQL)]
        S3[AWS S3 / Object Storage]
        Cache[Redis Cache]
    end
    
    subgraph "External Services"
        WeatherAPI[Weather API]
        MLModel[TensorFlow Models]
    end
    
    Mobile -->|HTTPS/REST| Gateway
    Web -->|HTTPS/REST| Gateway
    Gateway --> FastAPI
    FastAPI --> Auth
    FastAPI --> ML
    FastAPI --> Weather
    FastAPI --> Chatbot
    FastAPI --> Postgres
    FastAPI --> S3
    FastAPI --> Cache
    Weather --> WeatherAPI
    ML --> MLModel
    Mobile -.->|Offline| TFLite[On-Device TFLite Model]
```

### Technology Stack Summary

**Frontend:**
- Mobile: React Native + TypeScript + Expo
- Web: React + TypeScript + Material UI
- State Management: React Context API / Redux Toolkit
- HTTP Client: Axios with interceptors

**Backend:**
- Framework: FastAPI (Python 3.10+)
- Authentication: JWT with PyJWT
- ORM: SQLAlchemy with Alembic migrations
- Validation: Pydantic models
- Async: asyncio with asyncpg

**ML/AI:**
- Training: TensorFlow/Keras 2.x
- Base Models: MobileNetV3 / EfficientNetB0
- Deployment: TensorFlow Lite for mobile
- Chatbot: Retrieval-based with sentence transformers

**Infrastructure:**
- Containerization: Docker with multi-stage builds
- Orchestration: Docker Compose (local) / Kubernetes (production)
- IaC: Terraform for AWS resources
- CI/CD: GitHub Actions
- Monitoring: Prometheus + Grafana

**Data:**
- Database: PostgreSQL 14+
- Cache: Redis 7+
- Storage: AWS S3 or MinIO (local)

## Components and Interfaces

### 1. Mobile Application (React Native)

**Structure:**
```
mobile/
├── src/
│   ├── screens/          # Screen components
│   │   ├── AuthScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── CameraScreen.tsx
│   │   ├── FieldsScreen.tsx
│   │   ├── ChatbotScreen.tsx
│   │   └── ProfileScreen.tsx
│   ├── components/       # Reusable components
│   │   ├── DiseaseCard.tsx
│   │   ├── FieldCard.tsx
│   │   ├── WeatherWidget.tsx
│   │   └── ChatMessage.tsx
│   ├── services/         # API and business logic
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   ├── inference.ts
│   │   ├── storage.ts
│   │   └── tflite.ts
│   ├── models/           # TypeScript interfaces
│   ├── utils/            # Helper functions
│   ├── navigation/       # React Navigation setup
│   └── assets/           # Images, fonts, models
│       └── models/
│           └── disease_model.tflite
```

**Key Features:**
- Camera integration with expo-camera
- On-device inference using react-native-tensorflow-lite
- Offline storage with @react-native-async-storage/async-storage
- Background sync queue for offline operations
- Push notifications with expo-notifications
- GPS location with expo-location

**Offline Strategy:**
- Store TFLite model in app bundle (5-10MB)
- Cache API responses in AsyncStorage
- Queue failed requests for retry
- Sync queue when connectivity restored
- Display offline indicator in UI

### 2. Web Dashboard (React)

**Structure:**
```
web/
├── src/
│   ├── pages/            # Page components
│   │   ├── LoginPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── ImagesPage.tsx
│   │   ├── UsersPage.tsx
│   │   └── AnalyticsPage.tsx
│   ├── components/       # Reusable components
│   │   ├── Sidebar.tsx
│   │   ├── MetricsCard.tsx
│   │   ├── ImageGallery.tsx
│   │   └── DataTable.tsx
│   ├── services/         # API clients
│   │   └── api.ts
│   ├── hooks/            # Custom React hooks
│   ├── types/            # TypeScript types
│   └── utils/            # Utilities
```

**Key Features:**
- Material UI components for consistent design
- Data visualization with recharts
- Image gallery with lightbox
- Filtering and pagination for large datasets
- Export functionality (CSV, PDF)
- Real-time metrics updates

### 3. Backend API (FastAPI)

**Structure:**
```
backend/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration management
│   ├── dependencies.py         # Dependency injection
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── inference.py
│   │       │   ├── irrigation.py
│   │       │   ├── chatbot.py
│   │       │   ├── fields.py
│   │       │   ├── weather.py
│   │       │   └── admin.py
│   │       └── router.py
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── field.py
│   │   ├── crop_record.py
│   │   ├── image_inference.py
│   │   ├── recommendation.py
│   │   └── chat_history.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── auth.py
│   │   ├── inference.py
│   │   ├── field.py
│   │   └── chatbot.py
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   ├── ml_service.py
│   │   ├── weather_service.py
│   │   ├── chatbot_service.py
│   │   ├── irrigation_service.py
│   │   └── storage_service.py
│   ├── repositories/           # Data access layer
│   │   ├── user_repository.py
│   │   ├── field_repository.py
│   │   └── inference_repository.py
│   ├── middleware/             # Custom middleware
│   │   ├── auth_middleware.py
│   │   ├── rate_limit.py
│   │   └── logging_middleware.py
│   └── utils/                  # Utilities
│       ├── security.py
│       ├── validators.py
│       └── logger.py
```

**API Design Patterns:**
- Repository pattern for data access
- Service layer for business logic
- Dependency injection for testability
- Async/await for I/O operations
- Pydantic for request/response validation

**Middleware Stack:**
1. CORS middleware
2. Request logging middleware
3. Rate limiting middleware
4. JWT authentication middleware
5. Error handling middleware

### 4. ML Service

**Structure:**
```
ml/
├── training/
│   ├── train_disease_model.py
│   ├── data_loader.py
│   ├── augmentation.py
│   └── evaluate.py
├── inference/
│   ├── disease_predictor.py
│   └── model_loader.py
├── conversion/
│   └── convert_to_tflite.py
├── models/
│   ├── disease_model.h5
│   └── disease_model.tflite
├── data/
│   └── knowledge_base/
│       └── agriculture_qa.json
└── notebooks/
    └── model_experiments.ipynb
```

**Disease Detection Model:**
- Base: MobileNetV3-Small (pre-trained on ImageNet)
- Input: 224x224x3 RGB images
- Output: Softmax probabilities for N disease classes
- Augmentation: RandomRotation, RandomFlip, RandomBrightness, RandomZoom
- Training: Transfer learning with frozen base, fine-tuning top layers
- Optimization: Adam optimizer, categorical crossentropy loss
- Metrics: Accuracy, precision, recall, F1-score per class

**TFLite Conversion:**
- Post-training quantization (dynamic range)
- Model size target: <10MB
- Inference time target: <500ms on mobile devices

**Chatbot Knowledge Base:**
- JSON structure with Q&A pairs
- Categories: pest management, fertilizers, irrigation, crop selection
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Retrieval: Cosine similarity search
- Response generation: Template-based with retrieved context

## Data Models

### Database Schema

```mermaid
erDiagram
    User ||--o{ Field : owns
    User ||--o{ ChatHistory : has
    Field ||--o{ CropRecord : contains
    Field ||--o{ ImageInference : has
    ImageInference ||--o{ Recommendation : generates
    
    User {
        uuid id PK
        string email UK
        string password_hash
        enum role
        timestamp created_at
        timestamp updated_at
    }
    
    Field {
        uuid id PK
        uuid user_id FK
        string name
        float latitude
        float longitude
        float area_hectares
        string soil_type
        string crop_type
        date sowing_date
        timestamp created_at
    }
    
    CropRecord {
        uuid id PK
        uuid field_id FK
        string crop_type
        date sowing_date
        date harvest_date
        float yield_kg
        timestamp created_at
    }
    
    ImageInference {
        uuid id PK
        uuid field_id FK
        string image_url
        json predictions
        float confidence
        string disease_detected
        enum inference_type
        timestamp created_at
    }
    
    Recommendation {
        uuid id PK
        uuid inference_id FK
        string treatment_type
        text description
        json products
        int priority
        timestamp created_at
    }
    
    ChatHistory {
        uuid id PK
        uuid user_id FK
        text query
        text response
        string language
        float confidence
        timestamp created_at
    }
```

### Pydantic Schemas (Request/Response)

**Authentication:**
```python
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: Literal["farmer", "admin"] = "farmer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
```

**Inference:**
```python
class InferenceRequest(BaseModel):
    image: UploadFile
    crop_type: str
    latitude: Optional[float]
    longitude: Optional[float]
    field_id: Optional[str]

class PredictionResult(BaseModel):
    disease: str
    confidence: float
    severity: Literal["low", "medium", "high"]

class InferenceResponse(BaseModel):
    status: str
    predictions: List[PredictionResult]
    top_prediction: PredictionResult
    recommendations: List[str]
    image_url: str
    inference_id: str
```

**Irrigation:**
```python
class IrrigationRequest(BaseModel):
    field_id: str
    soil_moisture: float = Field(ge=0, le=100)
    crop_type: str

class IrrigationResponse(BaseModel):
    next_irrigation_time: datetime
    water_volume_liters: float
    reasoning: str
    weather_forecast: dict
```

**Chatbot:**
```python
class ChatbotQuery(BaseModel):
    query: str = Field(max_length=500)
    language: str = "en"
    field_id: Optional[str]

class ChatbotResponse(BaseModel):
    response: str
    confidence: float
    sources: List[str]
    disclaimer: str
```

## Error Handling

### Error Response Format

```python
class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[dict]
    timestamp: datetime
    request_id: str
```

### Error Categories

1. **Authentication Errors (401)**
   - INVALID_TOKEN
   - EXPIRED_TOKEN
   - MISSING_TOKEN

2. **Authorization Errors (403)**
   - INSUFFICIENT_PERMISSIONS
   - RESOURCE_ACCESS_DENIED

3. **Validation Errors (422)**
   - INVALID_INPUT
   - MISSING_REQUIRED_FIELD
   - INVALID_FILE_FORMAT

4. **Business Logic Errors (400)**
   - FIELD_NOT_FOUND
   - INFERENCE_FAILED
   - WEATHER_API_UNAVAILABLE

5. **Server Errors (500)**
   - DATABASE_ERROR
   - ML_MODEL_ERROR
   - STORAGE_ERROR

### Error Handling Strategy

- Use FastAPI exception handlers for consistent responses
- Log all errors with correlation IDs
- Return user-friendly messages
- Include retry hints for transient failures
- Sanitize error details in production

## Testing Strategy

### Unit Tests

**Backend:**
- Test services in isolation with mocked dependencies
- Test repositories with in-memory database
- Test utilities and validators
- Coverage target: >80%

**Frontend:**
- Test components with React Testing Library
- Test hooks and utilities
- Test API service functions with mocked responses
- Coverage target: >70%

**ML:**
- Test data loading and augmentation
- Test model inference with sample images
- Test TFLite conversion output
- Validate model metrics against baseline

### Integration Tests

- Test API endpoints with test database
- Test authentication flow end-to-end
- Test image upload and inference pipeline
- Test chatbot with knowledge base
- Test weather service with mocked API

### End-to-End Tests

- Test critical user flows (signup, login, disease detection)
- Test offline sync functionality
- Test admin dashboard operations
- Use Playwright or Cypress for web
- Use Detox for React Native

### Performance Tests

- Load test API endpoints (100+ concurrent users)
- Measure inference latency (target: <5s)
- Test database query performance
- Test image upload/download speeds
- Monitor memory usage and leaks

## Security Considerations

### Authentication & Authorization

- JWT tokens with 24-hour expiration
- Refresh token mechanism for mobile apps
- Role-based access control (RBAC)
- Password hashing with bcrypt (cost factor: 12)
- Rate limiting: 100 requests/minute per user

### Input Validation

- Pydantic models for all request bodies
- File type validation (JPEG, PNG only)
- File size limits (10MB max)
- SQL injection prevention via ORM
- XSS prevention via output encoding

### Data Protection

- HTTPS/TLS for all communications
- Encrypted database connections
- S3 bucket encryption at rest
- Environment variables for secrets
- No sensitive data in logs

### API Security

- CORS configuration for allowed origins
- CSRF protection for state-changing operations
- Request signing for critical operations
- API versioning for backward compatibility
- Rate limiting per endpoint

## Deployment Architecture

### Development Environment

```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/agri_dev
      - REDIS_URL=redis://redis:6379
    depends_on: [db, redis]
  
  db:
    image: postgres:14
    volumes: ["postgres_data:/var/lib/postgresql/data"]
  
  redis:
    image: redis:7-alpine
  
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports: ["9000:9000", "9001:9001"]
```

### Production Architecture (AWS)

**Compute:**
- ECS Fargate for backend containers
- Auto-scaling based on CPU/memory
- Application Load Balancer

**Database:**
- RDS PostgreSQL Multi-AZ
- Automated backups (7-day retention)
- Read replicas for analytics

**Storage:**
- S3 for images with CloudFront CDN
- Lifecycle policies for old data

**Caching:**
- ElastiCache Redis cluster

**Monitoring:**
- CloudWatch for logs and metrics
- SNS for alerts
- X-Ray for distributed tracing

**CI/CD Pipeline:**
1. Push to GitHub
2. GitHub Actions triggers
3. Run tests and linting
4. Build Docker images
5. Push to ECR
6. Deploy to ECS (staging)
7. Run smoke tests
8. Manual approval
9. Deploy to production
10. Health check validation

## Configuration Management

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://host:6379
REDIS_TTL=3600

# Storage
S3_BUCKET=agri-platform-images
S3_REGION=us-east-1
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx

# JWT
JWT_SECRET_KEY=xxx
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# External APIs
WEATHER_API_KEY=xxx
WEATHER_API_URL=https://api.weather.com

# ML
ML_MODEL_PATH=/app/models/disease_model.h5
TFLITE_MODEL_PATH=/app/models/disease_model.tflite
CONFIDENCE_THRESHOLD=0.7

# App
APP_ENV=production
LOG_LEVEL=INFO
CORS_ORIGINS=https://app.example.com,https://admin.example.com
RATE_LIMIT_PER_MINUTE=100
```

### Configuration Loading

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret_key: str
    s3_bucket: str
    weather_api_key: str
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

## Monitoring and Observability

### Logging Strategy

**Structured Logging Format:**
```json
{
  "timestamp": "2026-02-14T10:30:00Z",
  "level": "INFO",
  "service": "backend",
  "request_id": "abc-123",
  "user_id": "user-456",
  "endpoint": "/api/v1/infer/image",
  "method": "POST",
  "status_code": 200,
  "duration_ms": 1234,
  "message": "Image inference completed"
}
```

**Log Levels:**
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages for recoverable issues
- ERROR: Error messages for failures
- CRITICAL: Critical issues requiring immediate attention

### Metrics

**Application Metrics:**
- Request rate (requests/second)
- Error rate (errors/total requests)
- Response time (p50, p95, p99)
- Active users
- Inference count per hour

**Business Metrics:**
- Daily active users
- Images processed per day
- Average confidence scores
- Most common diseases detected
- Chatbot query volume

**Infrastructure Metrics:**
- CPU utilization
- Memory usage
- Database connections
- Cache hit rate
- Storage usage

### Health Checks

**Endpoint: GET /health**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-14T10:30:00Z",
  "version": "1.0.0",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "storage": "healthy",
    "ml_model": "healthy",
    "weather_api": "degraded"
  }
}
```

## Scalability Considerations

### Horizontal Scaling

- Stateless backend services
- Session data in Redis
- Load balancer distribution
- Database connection pooling
- Async processing for heavy tasks

### Caching Strategy

**Cache Layers:**
1. Browser cache (static assets)
2. CDN cache (images)
3. Application cache (Redis)
4. Database query cache

**Cache Keys:**
- Weather data: `weather:{lat}:{lon}` (TTL: 6 hours)
- User profile: `user:{user_id}` (TTL: 1 hour)
- Field data: `field:{field_id}` (TTL: 1 hour)
- ML predictions: `inference:{image_hash}` (TTL: 24 hours)

### Database Optimization

- Indexes on foreign keys and query fields
- Partitioning for large tables (by date)
- Read replicas for analytics queries
- Connection pooling (min: 5, max: 20)
- Query optimization with EXPLAIN ANALYZE

### Async Processing

**Use Cases:**
- Image processing and ML inference
- Email notifications
- Weather data polling
- Batch analytics calculations

**Implementation:**
- Celery with Redis broker
- Task queues for different priorities
- Retry logic with exponential backoff
- Dead letter queue for failed tasks

## Migration and Versioning

### API Versioning

- URL-based versioning: `/api/v1/`, `/api/v2/`
- Maintain backward compatibility for 2 versions
- Deprecation warnings in response headers
- Migration guides in documentation

### Database Migrations

- Alembic for schema migrations
- Version control for migration scripts
- Automated migrations in CI/CD
- Rollback procedures documented
- Zero-downtime migrations with blue-green deployment

## Future Enhancements

1. **Advanced ML Features**
   - Multi-disease detection in single image
   - Pest detection alongside diseases
   - Crop yield prediction models
   - Soil health analysis from images

2. **Platform Features**
   - Marketplace for agricultural products
   - Community forum for farmers
   - Video tutorials and courses
   - Integration with IoT sensors

3. **Technical Improvements**
   - GraphQL API option
   - WebSocket for real-time updates
   - Progressive Web App (PWA)
   - Federated learning for privacy-preserving model training
