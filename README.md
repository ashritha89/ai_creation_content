# AI Content Creator SaaS

A production-ready SaaS application for AI-powered content creation built with Python and Streamlit.

## 🚀 Features

### Core Features
- **JWT Authentication**: Secure token-based authentication with access and refresh tokens
- **Secure Authentication**: Bcrypt password hashing, email validation, secure sessions
- **Freemium Model**: Free preview for non-users, full access for authenticated users
- **Content Generation**: AI-powered content creation with customizable parameters
- **Content Evaluation**: Quality scoring and analysis
- **Content Repurposing**: Convert content into multiple formats
- **History Management**: User-specific content history with full isolation

### SaaS Architecture
- **Modular Design**: Separated concerns (auth, database, content, utils)
- **Database**: SQLite for MVP (easily migratable to PostgreSQL)
- **User Isolation**: Complete data separation between users
- **Scalable**: Ready for subscription plans, usage limits, and payments

## 📁 Project Structure

```
ai_content_creator/
├── app/
│   ├── __init__.py
│   ├── auth/                    # Authentication module
│   │   ├── __init__.py
│   │   └── auth_manager.py     # Password hashing, validation, login/signup
│   ├── database/                # Database module
│   │   ├── __init__.py
│   │   ├── models.py           # Database schema and initialization
│   │   ├── user_db.py          # User database operations
│   │   └── history_db.py       # Content history operations
│   ├── content/                 # Content generation module
│   │   ├── __init__.py
│   │   ├── content_generator.py    # AI content generation
│   │   ├── content_evaluator.py    # Quality evaluation
│   │   └── content_repurposer.py   # Content repurposing
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── validators.py        # Input validation
│       └── download.py          # Download utilities
├── app.py                       # Main Streamlit application
├── requirements.txt             # Python dependencies
├── .env                        # Environment variables (create this)
└── saas_app.db                 # SQLite database (auto-created)
```

## 🛠️ Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET=your-super-secret-jwt-key-change-this
```

Alternatively, copy `.env.example` to `.env` and fill in the values:

```powershell
copy .env.example .env
# then edit .env to add your real secrets
```

**Important**: Generate a strong JWT secret:
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 3. Run the Application

```bash
streamlit run app.py
```

Or use the helper scripts:
- **Windows PowerShell**: `.\run_app.ps1`
- **Windows CMD**: `.\run_app.bat`

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Content History Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `title`: Content title
- `prompt`: User's original prompt
- `output`: Generated content
- `content_type`: Type of content
- `tone`: Tone used
- `timestamp`: Creation timestamp

### User Preferences Table (Future)
- User-specific default settings

### Usage Tracking Table (Future)
- Track user actions for subscription/limits

## 🔐 Security Features

1. **JWT Authentication**: Token-based authentication with automatic refresh
2. **Password Hashing**: Bcrypt with salt
3. **Input Validation**: Email format, password strength
4. **SQL Injection Protection**: Parameterized queries
5. **User Isolation**: Database-level user filtering
6. **Environment Variables**: API keys and secrets stored securely
7. **Token Expiration**: Access tokens (24h) and refresh tokens (7 days)

## 💰 Freemium Model

### Non-Authenticated Users
- ✅ Can enter prompts
- ✅ See preview (first 2-3 lines)
- ❌ Cannot view full content
- ❌ Cannot download
- ❌ Cannot access quality scores
- ❌ Cannot repurpose content
- ❌ Cannot access history

### Authenticated Users
- ✅ All preview features
- ✅ View full generated content
- ✅ Download content
- ✅ Quality scoring
- ✅ Content repurposing
- ✅ Full history access
- ✅ User-specific data isolation

## 🚀 Scaling to Production

### Database Migration (PostgreSQL)

1. Install PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

2. Update `app/database/models.py`:
   - Replace SQLite connection with PostgreSQL
   - Update connection string
   - Adjust SQL syntax if needed

### Adding Subscription Plans

1. Add `subscription_plans` table:
   - `id`, `name`, `price`, `features`, `limits`
2. Add `user_subscriptions` table:
   - `user_id`, `plan_id`, `start_date`, `end_date`, `status`
3. Implement usage tracking:
   - Check limits before generation
   - Track usage in `usage_tracking` table

### Adding Payment Integration

1. Integrate Stripe/PayPal SDK
2. Add payment endpoints
3. Update subscription status after payment
4. Implement webhook handlers

### Admin Dashboard

1. Create admin authentication
2. Add admin routes:
   - User management
   - Usage analytics
   - Content moderation
   - System settings

## 📊 Future Enhancements

- [ ] Subscription plans (Free, Pro, Enterprise)
- [ ] Usage limits per plan
- [ ] Payment gateway integration
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] Content templates
- [ ] Team collaboration
- [ ] API access
- [ ] Analytics dashboard

## 🔧 Development

### Running Tests

```bash
# Add tests directory and run
pytest tests/
```

### Database Reset

Delete `saas_app.db` to reset the database. It will be recreated on next run.

## 📝 License

This is a production-ready SaaS application template.

## 🤝 Contributing

This is a private SaaS application. For questions or issues, contact the development team.

