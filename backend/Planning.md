### Authentication & User Management
- POST auth/register
- POST auth/login
- POST auth/refresh
- GET user/profile
- PUT user/profile
- DELETE user/account

### Calendar Integration
- POST calendar/connect/google
- POST calendar/connect/callback
- GET calendar/integrations
- DELETE calendar/integrations/{id}
- POST calendar/sync
- GET calendar/events

### Preferences Management
- GET /api/weather/current
- GET /api/weather/forecast
- POST /api/weather/refresh
- GET /api/schedule/suggestions
- POST /api/schedule/generate
- GET /api/schedule/suggestions/{date}
- POST /api/schedule/book/{suggestion_id}

### Ride Planning and Tracking
- GET /api/rides/planned
- POST /api/rides/plan
- PUT /api/rides/{id}
- DELETE /api/rides/{id}
- POST /api/rides/{id}/complete
- GET /api/rides/history
- GET /api/rides/stats