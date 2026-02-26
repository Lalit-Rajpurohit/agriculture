# Implementation Plan

- [ ] 1. Set up project structure and configuration
  - Create root directory structure with backend/, mobile/, web/, ml/, infrastructure/ folders
  - Initialize Git repository with .gitignore for Python, Node, and environment files
  - Create README.md with project overview and setup instructions
  - Create .env.example files for each service with required environment variables
  - _Requirements: 13.5_

- [ ] 2. Set up backend FastAPI project foundation
  - Initialize Python project with pyproject.toml and dependencies (fastapi, uvicorn, sqlalchemy, pydantic, python-jose, passlib, asyncpg, redis, boto3)
  - Create backend/app/main.py with FastAPI app initialization and CORS middleware
  - Create backend/app/config.py with Pydantic Settings for environment variable loading
  - Create backend/app/dependencies.py for dependency injection setup
  - _Requirements: 11.1, 13.5_

- [ ] 3. Implement database models and migrations
  - Create backend/app/models/base.py with SQLAlchemy Base and common fields (id, created_at, updated_at)
  - Create backend/app/models/user.py with User model (id, email, password_hash, role, timestamps)
  - Create backend/app/models/field.py with Field model (id, user_id FK, name, latitude, longitude, area_hectares, soil_type, crop_type, sowing_date)
  - Create backend/app/models/image_inference.py with ImageInference model (id, field_id FK, image_url, predictions JSON, confidence, disease_detected, inference_type)
  - Create backend/app/models/recommendation.py with Recommendation model (id, inference_id FK, treatment_type, description, products JSON, priority)
  - Create backend/app/models/chat_history.py with ChatHistory model (id, user_id FK, query, response, language, confidence)
  - Create backend/app/models/crop_record.py with CropRecord model (id, field_id FK, crop_type, sowing_date, harvest_date, yield_kg)
  - Initialize Alembic and create initial migration script for all models
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 4. Implement authentication and security
  - Create backend/app/utils/security.py with password hashing (bcrypt) and JWT token generation/verification functions
  - Create backend/app/schemas/auth.py with Pydantic models (SignupRequest, LoginRequest, TokenResponse)
  - Create backend/app/services/auth_service.py with signup, login, and token validation logic
  - Create backend/app/repositories/user_repository.py with async methods for user CRUD operations
  - Create backend/app/api/v1/endpoints/auth.py with POST /signup and POST /login endpoints
  - Create backend/app/middleware/auth_middleware.py for JWT token validation on protected routes
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 9.1_

- [ ] 5. Implement rate limiting and input validation
  - Create backend/app/middleware/rate_limit.py using Redis for rate limiting (100 requests/minute per user)
  - Create backend/app/utils/validators.py with input sanitization and validation functions
  - Add rate limiting middleware to FastAPI app with 429 response for exceeded limits
  - Add Pydantic validators for email, file types, and field constraints
  - _Requirements: 9.2, 9.3, 9.5_

- [ ] 6. Implement storage service for image uploads
  - Create backend/app/services/storage_service.py with S3 client initialization (boto3)
  - Implement upload_image method with file validation (JPEG/PNG, max 10MB), unique filename generation, and S3 upload
  - Implement get_image_url method to generate presigned URLs for image retrieval
  - Implement delete_image method for cleanup operations
  - Add MinIO configuration for local development environment
  - _Requirements: 9.5, 14.3_

- [ ] 7. Implement ML training pipeline for disease detection
  - Create ml/training/data_loader.py to load images from folder structure (disease_name/images) and create train/val/test splits
  - Create ml/training/augmentation.py with TensorFlow ImageDataGenerator for rotation, flip, brightness, zoom augmentations
  - Create ml/training/train_disease_model.py using transfer learning with MobileNetV3-Small base model
  - Implement model training with frozen base layers, custom classification head, Adam optimizer, and categorical crossentropy loss
  - Implement model evaluation with accuracy, precision, recall, F1-score, and confusion matrix generation
  - Save trained model as disease_model.h5 in ml/models/ directory
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 8. Implement TensorFlow Lite model conversion
  - Create ml/conversion/convert_to_tflite.py to load trained .h5 model
  - Apply post-training dynamic range quantization for model optimization
  - Convert model to TensorFlow Lite format and save as disease_model.tflite
  - Validate TFLite model output matches original model predictions
  - Verify model size is under 10MB target
  - _Requirements: 10.6, 10.7_

- [ ] 9. Implement ML inference service
  - Create backend/app/services/ml_service.py with TensorFlow model loading and caching
  - Implement predict_disease method that accepts image bytes, preprocesses to 224x224, runs inference, and returns top predictions with confidence scores
  - Implement get_recommendations method that maps disease predictions to treatment advice from a JSON knowledge base
  - Add confidence threshold filtering (minimum 70%) for predictions
  - Implement fallback error handling for model loading failures
  - _Requirements: 2.2, 2.4, 2.5_

- [ ] 10. Implement image inference API endpoint
  - Create backend/app/schemas/inference.py with Pydantic models (InferenceRequest, PredictionResult, InferenceResponse)
  - Create backend/app/repositories/inference_repository.py for storing inference results in database
  - Create backend/app/api/v1/endpoints/inference.py with POST /infer/image endpoint
  - Implement endpoint logic: validate image, upload to S3, run ML inference, store results, return predictions and recommendations
  - Add JWT authentication requirement and field_id association
  - Implement 5-second response time target with async processing
  - _Requirements: 2.1, 2.2, 2.4, 2.5, 2.7, 14.1_

- [ ] 11. Implement weather service integration
  - Create backend/app/services/weather_service.py with external weather API client (e.g., OpenWeatherMap)
  - Implement get_current_weather method accepting latitude/longitude and returning temperature, humidity, rainfall forecast, wind speed, UV index
  - Implement get_forecast method for 7-day weather predictions
  - Implement detect_extreme_weather method to identify alerts (heavy rain, frost, heat wave, hail)
  - Add Redis caching for weather data with 6-hour TTL
  - Implement fallback to cached data when API is unavailable with exponential backoff retry
  - _Requirements: 6.1, 6.4, 6.5_

- [ ] 12. Implement weather API endpoint and alerts
  - Create backend/app/api/v1/endpoints/weather.py with GET /weather endpoint accepting latitude/longitude
  - Implement weather polling background task that checks forecasts for all registered fields every 6 hours
  - Create alert generation logic for extreme weather conditions
  - Store alerts in database with associated field_id and user_id
  - _Requirements: 6.1, 6.2, 6.4_

- [ ] 13. Implement irrigation advisory service
  - Create backend/app/services/irrigation_service.py with crop water requirement calculations
  - Implement calculate_irrigation_advice method accepting soil_moisture, crop_type, field_size, and weather forecast
  - Use crop-specific evapotranspiration rates and soil moisture thresholds
  - Calculate next irrigation time based on weather forecast and current moisture
  - Calculate water volume in liters based on field area and crop requirements
  - Return reasoning explanation for recommendations
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 14. Implement irrigation advisory API endpoint
  - Create backend/app/schemas/irrigation.py with Pydantic models (IrrigationRequest, IrrigationResponse)
  - Create backend/app/api/v1/endpoints/irrigation.py with POST /irrigation/advise endpoint
  - Integrate weather service to fetch forecast data
  - Call irrigation service to calculate recommendations
  - Return next irrigation time, water volume, reasoning, and weather forecast
  - _Requirements: 3.1, 3.4, 3.5_

- [ ] 15. Implement chatbot knowledge base and retrieval
  - Create ml/data/knowledge_base/agriculture_qa.json with Q&A pairs categorized by topic (pest management, fertilizers, irrigation, crop selection)
  - Create backend/app/services/chatbot_service.py with sentence-transformers model loading (all-MiniLM-L6-v2)
  - Implement embed_knowledge_base method to generate embeddings for all Q&A pairs
  - Implement retrieve_relevant_context method using cosine similarity search for top-k relevant answers
  - Implement generate_response method using template-based response generation with retrieved context
  - Add safety disclaimers for critical agricultural decisions
  - _Requirements: 4.2, 4.3, 4.4_

- [ ] 16. Implement chatbot API endpoint with multilingual support
  - Create backend/app/schemas/chatbot.py with Pydantic models (ChatbotQuery, ChatbotResponse)
  - Create backend/app/repositories/chat_repository.py for storing chat history
  - Create backend/app/api/v1/endpoints/chatbot.py with POST /chatbot/query endpoint
  - Implement language detection and translation for Indian languages (Hindi, Tamil, Telugu, Kannada, Bengali)
  - Call chatbot service for retrieval and response generation
  - Store query, response, language, and confidence in chat history
  - Return response with confidence score, sources, and disclaimer
  - _Requirements: 4.1, 4.2, 4.4, 4.5, 4.6_

- [ ] 17. Implement field management API endpoints
  - Create backend/app/schemas/field.py with Pydantic models (FieldCreate, FieldUpdate, FieldResponse)
  - Create backend/app/repositories/field_repository.py with async CRUD methods for fields
  - Create backend/app/api/v1/endpoints/fields.py with GET /fields, POST /fields, PUT /fields/{id}, DELETE /fields/{id} endpoints
  - Implement field creation with validation for GPS coordinates, area, soil type, crop type, sowing date
  - Implement field listing with user_id filtering and days since sowing calculation
  - Implement field update with timestamp tracking
  - Implement field history retrieval showing associated images, predictions, and recommendations
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 18. Implement admin dashboard API endpoints
  - Create backend/app/api/v1/endpoints/admin.py with admin-only endpoints (role check middleware)
  - Implement GET /admin/metrics endpoint returning total users, active fields, images processed, prediction accuracy
  - Implement GET /admin/images endpoint with pagination, filtering by date range, crop type, disease type, confidence threshold
  - Implement GET /admin/predictions endpoint with image thumbnails, predictions, confidence scores
  - Implement PUT /admin/predictions/{id}/feedback endpoint for marking predictions as correct/incorrect
  - Calculate and return API response times, error rates, and ML model performance metrics
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 19. Implement logging and monitoring middleware
  - Create backend/app/utils/logger.py with structured JSON logging configuration
  - Create backend/app/middleware/logging_middleware.py to log all requests with method, path, status code, duration, user_id, request_id
  - Implement error logging with stack traces and context for debugging
  - Add correlation IDs to all requests for distributed tracing
  - _Requirements: 15.1, 15.2, 15.4_

- [ ] 20. Implement health check endpoint
  - Create backend/app/api/v1/endpoints/health.py with GET /health endpoint
  - Check database connectivity with test query
  - Check Redis connectivity with ping command
  - Check S3 storage availability with bucket access test
  - Check ML model loading status
  - Check weather API availability with test request
  - Return overall status (healthy/degraded/unhealthy) and individual component statuses
  - _Requirements: 11.5, 15.3_

- [ ] 21. Set up Docker configuration for backend
  - Create backend/Dockerfile with multi-stage build (builder stage for dependencies, runtime stage for app)
  - Use Python 3.10+ slim base image
  - Copy requirements and install dependencies in builder stage
  - Copy application code and ML models in runtime stage
  - Expose port 8000 and set CMD to run uvicorn server
  - Create docker-compose.yml for local development with backend, postgres, redis, minio services
  - _Requirements: 11.1, 11.2_

- [ ] 22. Initialize React Native mobile app project
  - Initialize Expo project with TypeScript template in mobile/ directory
  - Install dependencies: @react-navigation/native, @react-navigation/stack, axios, @react-native-async-storage/async-storage, expo-camera, expo-location, expo-notifications
  - Create mobile/src folder structure: screens/, components/, services/, models/, utils/, navigation/, assets/
  - Configure TypeScript with strict mode and path aliases
  - _Requirements: 8.1_

- [ ] 23. Implement mobile app navigation structure
  - Create mobile/src/navigation/AppNavigator.tsx with React Navigation stack navigator
  - Define routes: Auth (Login/Signup), Home, Camera, Fields, Chatbot, Profile screens
  - Implement authentication flow with conditional rendering based on token presence
  - Create bottom tab navigator for main app screens
  - _Requirements: 8.1_

- [ ] 24. Implement mobile API service and authentication
  - Create mobile/src/services/api.ts with Axios instance configured with base URL and interceptors
  - Implement request interceptor to add JWT token to headers
  - Implement response interceptor for error handling and token refresh
  - Create mobile/src/services/auth.ts with signup, login, logout, and token storage functions using AsyncStorage
  - Create mobile/src/models/User.ts and mobile/src/models/Auth.ts TypeScript interfaces
  - _Requirements: 1.1, 1.2, 8.1_

- [ ] 25. Implement mobile authentication screens
  - Create mobile/src/screens/AuthScreen.tsx with login and signup forms
  - Implement form validation for email and password fields
  - Call auth service methods on form submission
  - Store JWT token in AsyncStorage on successful authentication
  - Navigate to Home screen after login
  - Display error messages for failed authentication
  - _Requirements: 1.1, 1.2_

- [ ] 26. Implement mobile camera and image capture
  - Create mobile/src/screens/CameraScreen.tsx with expo-camera integration
  - Request camera permissions on screen mount
  - Implement capture button to take photo and save to local storage
  - Implement image picker option to select from gallery
  - Display captured image preview with crop type selection dropdown
  - Implement upload button to send image to inference API
  - _Requirements: 2.1_

- [ ] 27. Implement on-device TFLite inference for mobile
  - Install react-native-tensorflow-lite or expo-tensorflow-lite package
  - Copy disease_model.tflite to mobile/src/assets/models/ directory
  - Create mobile/src/services/tflite.ts with model loading and inference functions
  - Implement preprocessImage function to resize and normalize image to 224x224
  - Implement runInference function to execute TFLite model and return predictions
  - Implement offline detection logic to use TFLite when network is unavailable
  - _Requirements: 2.1, 2.2, 8.1, 8.2_

- [ ] 28. Implement mobile inference service and results display
  - Create mobile/src/services/inference.ts with uploadImage and getInferenceResults API methods
  - Create mobile/src/components/DiseaseCard.tsx to display prediction results with disease name, confidence, severity, and recommendations
  - Implement fallback logic: try on-device inference first, then server inference if confidence is low or offline mode fails
  - Display loading indicator during inference
  - Store inference results in AsyncStorage for offline viewing
  - _Requirements: 2.2, 2.3, 2.4, 2.5, 8.2, 8.3_

- [ ] 29. Implement mobile offline storage and sync queue
  - Create mobile/src/services/storage.ts with AsyncStorage wrapper functions for caching API responses
  - Implement queue system for failed API requests (images, field updates) using AsyncStorage
  - Create mobile/src/services/sync.ts with background sync logic
  - Implement network connectivity listener to trigger sync when online
  - Process queued requests sequentially and remove from queue on success
  - Display offline indicator in UI when network is unavailable
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 30. Implement mobile fields management screens
  - Create mobile/src/screens/FieldsScreen.tsx to display list of user's fields
  - Create mobile/src/components/FieldCard.tsx to show field name, crop type, area, days since sowing
  - Implement add field form with inputs for name, location (GPS), area, soil type, crop type, sowing date
  - Use expo-location to get current GPS coordinates
  - Call fields API to create, update, and retrieve fields
  - Display field history with associated images and recommendations
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 31. Implement mobile chatbot screen
  - Create mobile/src/screens/ChatbotScreen.tsx with chat interface
  - Create mobile/src/components/ChatMessage.tsx to display user and bot messages
  - Implement text input with send button
  - Call chatbot API with user query and display response
  - Support language selection dropdown for multilingual queries
  - Display confidence score and disclaimer with responses
  - Store chat history locally for offline viewing
  - _Requirements: 4.1, 4.2, 4.4, 4.6_

- [ ] 32. Implement mobile weather widget and alerts
  - Create mobile/src/components/WeatherWidget.tsx to display current weather for user's location
  - Call weather API with GPS coordinates to fetch temperature, humidity, rainfall forecast, wind speed
  - Implement push notification setup with expo-notifications
  - Register device token with backend for push notifications
  - Display weather alerts as notifications when received
  - Show alert details in app with recommended actions
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 33. Implement mobile home screen with dashboard
  - Create mobile/src/screens/HomeScreen.tsx with overview of recent activities
  - Display weather widget for current location
  - Show recent disease detections with thumbnails
  - Display quick action buttons for camera, fields, chatbot
  - Show notifications badge for unread alerts
  - Implement pull-to-refresh for data updates
  - _Requirements: 5.2, 6.4_

- [ ] 34. Initialize React web dashboard project
  - Initialize React project with TypeScript and Vite in web/ directory
  - Install dependencies: react-router-dom, @mui/material, @emotion/react, axios, recharts
  - Create web/src folder structure: pages/, components/, services/, hooks/, types/, utils/
  - Configure TypeScript and path aliases
  - Set up Material UI theme with custom colors
  - _Requirements: 7.1_

- [ ] 35. Implement web dashboard authentication and routing
  - Create web/src/services/api.ts with Axios instance and interceptors similar to mobile
  - Create web/src/pages/LoginPage.tsx with Material UI form components
  - Implement React Router with protected routes requiring authentication
  - Create web/src/components/Sidebar.tsx with navigation menu for Dashboard, Images, Users, Analytics pages
  - Store JWT token in localStorage and add to API requests
  - _Requirements: 1.1, 1.2, 7.1_

- [ ] 36. Implement web dashboard metrics page
  - Create web/src/pages/DashboardPage.tsx with grid layout for metrics cards
  - Create web/src/components/MetricsCard.tsx to display individual metrics (total users, active fields, images processed, prediction accuracy)
  - Call admin metrics API endpoint to fetch data
  - Display metrics with icons and trend indicators
  - Implement auto-refresh every 30 seconds for real-time updates
  - _Requirements: 7.1, 7.5_

- [ ] 37. Implement web dashboard images gallery page
  - Create web/src/pages/ImagesPage.tsx with image gallery and filtering controls
  - Create web/src/components/ImageGallery.tsx to display image thumbnails in grid layout
  - Implement filters for date range, crop type, disease type, confidence threshold using Material UI components
  - Implement pagination with page size selector
  - Call admin images API endpoint with filter parameters
  - Implement lightbox modal to view full-size images with prediction details
  - _Requirements: 7.2, 7.3_

- [ ] 38. Implement web dashboard prediction review functionality
  - Add feedback buttons (correct/incorrect) to image detail modal
  - Call admin prediction feedback API endpoint when feedback is submitted
  - Update UI to show feedback status
  - Display prediction confidence scores with color coding (green >80%, yellow 70-80%, red <70%)
  - Show treatment recommendations alongside predictions
  - _Requirements: 7.4_

- [ ] 39. Implement web dashboard analytics page with charts
  - Create web/src/pages/AnalyticsPage.tsx with data visualization charts
  - Use recharts to create line chart for daily image uploads over time
  - Create bar chart for disease distribution (count per disease type)
  - Create pie chart for prediction confidence distribution
  - Implement date range selector for filtering analytics data
  - Add export button to download data as CSV
  - _Requirements: 7.1, 7.5_

- [ ] 40. Implement web dashboard users management page
  - Create web/src/pages/UsersPage.tsx with data table of registered users
  - Create web/src/components/DataTable.tsx with Material UI Table components
  - Display user email, role, registration date, number of fields, last activity
  - Implement search and filter functionality
  - Implement pagination and sorting
  - Add user detail modal showing fields and activity history
  - _Requirements: 7.1_

- [ ] 41. Create Terraform infrastructure configuration
  - Create infrastructure/terraform/ directory with main.tf, variables.tf, outputs.tf
  - Define AWS provider configuration with region variable
  - Create VPC with public and private subnets across multiple availability zones
  - Define security groups for ALB, ECS tasks, RDS, ElastiCache with appropriate ingress/egress rules
  - Create RDS PostgreSQL instance with Multi-AZ, automated backups, and parameter group
  - Create ElastiCache Redis cluster with automatic failover
  - Create S3 bucket for image storage with versioning and encryption enabled
  - Create CloudFront distribution for S3 bucket with caching policies
  - _Requirements: 11.2, 11.3_

- [ ] 42. Create Terraform ECS and load balancer configuration
  - Define ECS cluster for running backend containers
  - Create Application Load Balancer with HTTPS listener and SSL certificate
  - Define ECS task definition for backend service with container image, environment variables, and resource limits
  - Create ECS service with auto-scaling policies based on CPU and memory utilization
  - Configure ALB target group and health check for ECS service
  - Define IAM roles and policies for ECS task execution and S3 access
  - _Requirements: 11.2, 11.3_

- [ ] 43. Create GitHub Actions CI/CD workflow
  - Create .github/workflows/backend-ci.yml for backend service
  - Implement workflow triggers on push to main branch and pull requests
  - Add job for running Python linting (flake8, black) and type checking (mypy)
  - Add job for running backend unit tests with pytest and coverage reporting
  - Add job for building Docker image and pushing to Amazon ECR
  - Add job for deploying to ECS staging environment with automatic deployment
  - Add job for deploying to ECS production environment with manual approval
  - Implement smoke tests job to validate deployment health
  - _Requirements: 11.4_

- [ ] 44. Create GitHub Actions workflow for mobile and web
  - Create .github/workflows/mobile-ci.yml for React Native app
  - Implement linting and type checking for TypeScript code
  - Add job for building Expo app and generating APK/IPA
  - Create .github/workflows/web-ci.yml for React dashboard
  - Implement linting, type checking, and build verification for web app
  - Add job for deploying web dashboard to S3 and invalidating CloudFront cache
  - _Requirements: 11.4_

- [ ] 45. Create comprehensive README documentation
  - Create root README.md with project overview, architecture diagram, and feature list
  - Document prerequisites (Node.js, Python, Docker, AWS CLI)
  - Write local development setup instructions for backend, mobile, and web
  - Document environment variable configuration with .env.example files
  - Write deployment instructions for staging and production environments
  - Add troubleshooting section for common issues
  - Include links to API documentation and architecture diagrams
  - _Requirements: 13.5_

- [ ] 46. Create API documentation and examples
  - Ensure FastAPI automatic documentation is enabled at /docs and /redoc endpoints
  - Create docs/api-examples.md with curl examples for all endpoints
  - Document authentication flow with example JWT token usage
  - Provide sample request/response JSON for each endpoint
  - Document error response formats and common error codes
  - Create Postman collection with pre-configured requests for all endpoints
  - _Requirements: 13.1, 13.2, 13.3, 13.4_

- [ ] 47. Create sample dataset structure and training data
  - Create ml/data/raw/ directory with sample disease images organized by disease name folders
  - Include at least 5 disease classes with 50+ images each (e.g., leaf_blight, powdery_mildew, rust, bacterial_spot, healthy)
  - Document dataset structure in ml/data/README.md
  - Create ml/data/knowledge_base/agriculture_qa.json with 50+ Q&A pairs across categories
  - Add data augmentation examples and expected training results
  - _Requirements: 10.1, 4.2_

- [ ] 48. Implement production-ready error handling and validation
  - Review all API endpoints and add comprehensive error handling with try-catch blocks
  - Ensure all Pydantic models have proper validation rules and error messages
  - Implement custom exception classes for business logic errors
  - Add global exception handler in FastAPI app to catch unhandled exceptions
  - Ensure all error responses follow consistent ErrorResponse schema
  - Add input sanitization for all user-provided data
  - _Requirements: 9.2, 13.4_

- [ ] 49. Implement database connection pooling and optimization
  - Configure SQLAlchemy engine with connection pool settings (min: 5, max: 20)
  - Add database indexes on foreign keys and frequently queried fields (user_id, field_id, created_at)
  - Implement database session management with proper cleanup in finally blocks
  - Add query optimization for complex joins and aggregations
  - Implement database health check in /health endpoint
  - _Requirements: 12.5, 14.4_

- [ ] 50. Final integration testing and deployment preparation
  - Run full integration tests for all API endpoints with test database
  - Test mobile app on iOS and Android devices/emulators
  - Test web dashboard on multiple browsers (Chrome, Firefox, Safari)
  - Verify offline functionality in mobile app
  - Test ML inference pipeline end-to-end with sample images
  - Verify Docker Compose setup works for local development
  - Run Terraform plan to validate infrastructure configuration
  - Perform security audit of environment variables and secrets management
  - _Requirements: 11.1, 11.2, 11.3, 11.4_
