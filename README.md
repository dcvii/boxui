# Wagtail Karma Blog

A minimal Wagtail CMS application with Vue.js frontend, implementing a karma system for comments with full end-to-end testing using Cypress.

## Features

- **Wagtail CMS**: Blog article pages with rich text content
- **Comment System**: Users can add comments to articles
- **Karma System**: Upvote/downvote comments with real-time score updates
- **Vue 3 + TypeScript**: Interactive karma popover component
- **API Integration**: RESTful API for karma interactions
- **Comprehensive Testing**: Django unit tests and Cypress E2E tests
- **Modern Frontend**: Vite build system with hot reload

## Project Structure

```
wagtail-karma-blog/
├── home/                 # Wagtail starter app with ArticlePage model
├── comments/             # Django app for Comment + CommentInteraction models
├── frontend/             # Vite + Vue 3 + TypeScript project
│   ├── src/
│   │   ├── KarmaPopover.vue    # Main Vue component
│   │   └── main.ts             # Vue app initialization
│   ├── package.json
│   └── vite.config.ts
├── cypress/              # End-to-end tests
│   ├── e2e/
│   │   └── karma_spec.cy.ts    # Karma system tests
│   └── support/
├── templates/            # Django templates
│   └── home/
│       └── article_page.html   # Article page template
├── static/               # Static files (Vue build output)
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies and scripts
├── cypress.config.ts     # Cypress configuration
└── README.md
```

## Requirements

- **Python**: 3.12+
- **Node.js**: 20+
- **Database**: SQLite (included)
- **OS**: macOS (tested), Linux, Windows

## Installation

### 1. Backend Setup (Django/Wagtail)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 2. Frontend Setup (Vue.js)

```bash
# Install Node.js dependencies for both root and frontend
npm install
npm run install:frontend

# Build the Vue.js frontend
npm run build:frontend
```

### 3. Create Sample Data

```bash
# Start Django shell
python manage.py shell

# Create sample data
from django.contrib.auth.models import User
from home.models import ArticlePage
from comments.models import Comment
from wagtail.models import Page

# Get root page
root = Page.objects.get(id=1)

# Create an article page
article = ArticlePage(
    title="Welcome to Karma Blog",
    body="<p>This is a sample article. Hover over the karma scores below to interact with comments!</p>"
)
root.add_child(instance=article)

# Create a test user
user = User.objects.create_user('demo', 'demo@example.com', 'demo123')

# Add some comments
Comment.objects.create(
    page=article,
    user=user,
    text="This is a great article! Thanks for sharing."
)

Comment.objects.create(
    page=article,
    user=user,
    text="I have some questions about this topic. Could you elaborate more?"
)
```

## Running the Application

### Development Mode

```bash
# Terminal 1: Start Django development server
python manage.py runserver

# Terminal 2: Start Vue.js development server (optional, for frontend development)
npm run dev:frontend

# Access the application at http://localhost:8000
```

### Production Build
```bash
# Build frontend for production
npm run build:frontend

# Start Django server
python manage.py runserver
```

## Testing

### Django Unit Tests

```bash
# Run all Django tests
python manage.py test

# Run tests with pytest (alternative)
pytest

# Run specific app tests
python manage.py test comments
```

### Cypress E2E Tests

```bash
# Install Cypress (if not already installed)
npm install

# Run Cypress tests headlessly
npm run test:e2e

# Open Cypress interactive runner
npm run cypress:open

# Run all tests
npm run test:all
```

### Test Coverage

The project includes comprehensive tests:

- **Model Tests**: Comment and CommentInteraction models
- **API Tests**: Karma interaction endpoints
- **E2E Tests**: Complete user workflows including:
  - Comment karma display
  - Upvote/downvote functionality
  - Authentication requirements
  - Real-time updates
  - Vote toggling

## API Endpoints

### Karma Interaction

**POST** `/api/karma/`

```json
{
  "comment_id": 1,
  "reaction": 1  // 1 for upvote, -1 for downvote
}
```

**Response:**
```json
{
  "success": true,
  "karma_score": 5,
  "user_reaction": 1
}
```

### Get Comment Karma

**GET** `/api/karma/{comment_id}/`

**Response:**
```json
{
  "karma_score": 5,
  "user_reaction": 1
}
```

## Usage

### Admin Interface

1. Access the Wagtail admin at `http://localhost:8000/admin/`
2. Login with your superuser credentials
3. Create new article pages under "Pages"
4. Manage comments through Django admin at `http://localhost:8000/django-admin/`

### User Interaction

1. Visit an article page
2. Hover over comment karma scores to see the voting popover
3. Click 👍 to upvote or 👎 to downvote
4. Scores update in real-time
5. Click the same button again to toggle off your vote

### Development Workflow

1. **Backend Changes**: Modify Django models, views, or templates
2. **Frontend Changes**: Edit Vue components in `frontend/src/`
3. **Rebuild**: Run `npm run build:frontend` to compile Vue changes
4. **Test**: Run tests to ensure everything works

## Key Features Explained

### Karma System

- Each comment has a karma score (sum of all interactions)
- Users can upvote (+1) or downvote (-1) comments
- One vote per user per comment (enforced at database level)
- Clicking the same vote button toggles it off
- Real-time score updates without page refresh

### Vue.js Integration

- **KarmaPopover Component**: Appears on hover over karma displays
- **Real-time Updates**: Uses fetch API to communicate with Django
- **TypeScript Support**: Full type safety for better development experience
- **Reactive State**: Vue's reactivity system manages UI state

### Security & Authentication

- CSRF protection for all API calls
- Login required for voting
- Input validation and error handling
- Secure user session management

## Customization

### Adding New Fields

1. **Comment Model**: Add fields to `comments/models.py`
2. **Migration**: Run `python manage.py makemigrations && python manage.py migrate`
3. **Admin**: Update `comments/admin.py` to display new fields
4. **Frontend**: Modify Vue components if needed

### Styling

1. **Template Styles**: Edit CSS in `templates/home/article_page.html`
2. **Vue Components**: Modify styles in `frontend/src/KarmaPopover.vue`
3. **Global Styles**: Add styles to Django static files

### API Extensions

1. **New Endpoints**: Add views to `comments/views.py`
2. **URL Routing**: Update `comments/urls.py`
3. **Frontend**: Update `frontend/src/main.ts` for new API calls

## Environment Variables

Create a `.env` file for environment-specific settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

## Docker Support (Optional)

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=True
```

## Troubleshooting

### Common Issues

1. **Vue components not loading**: Run `npm run build:frontend`
2. **CSRF errors**: Ensure CSRF tokens are included in API calls
3. **Database errors**: Run `python manage.py migrate`
4. **Static files not found**: Run `python manage.py collectstatic`

### Debug Mode

Enable Django debug mode by setting `DEBUG=True` in `settings.py` for detailed error messages.

### Logging

Check Django logs for API errors and Vue browser console for frontend issues.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review test files for usage examples
3. Examine the source code for implementation details
