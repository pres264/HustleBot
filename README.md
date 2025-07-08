
## Key Files Explained

### Backend Core
- `app.py` - Main Flask application with Twilio webhook endpoints  
- `models.py` - Database schema definitions (SQLite)  
- `config.py` - Configuration variables (add to `.gitignore`)  

### AI Components
- `nlp/matcher.py` - Job matching algorithm  
- `nlp/resume_parser.py` - Skills extraction from user inputs  

### Utilities
- `utils/scraper.py` - Web scraper for job listings  
- `utils/bias_filter.py` - CV anonymization logic  
- `utils/twilio_handler.py` - WhatsApp message processor  

### Testing
- `tests/` - Unit and integration tests  
- `data/` - Sample data for development/testing  

### Deployment
- `Procfile` - Specifies how to run the app on Render/Heroku  
- `.github/workflows` - CI/CD pipeline configuration  


