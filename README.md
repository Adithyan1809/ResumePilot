<div align="center">

# 🚀 ResumeAI

### AI-Powered Resume Tailoring & ATS Optimization

*Tailor your resume to any job description with AI. Score your ATS compatibility. Download optimized resumes in seconds.*

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Resume Upload** | Upload PDF or DOCX resumes with automatic parsing |
| 🎯 **ATS Scoring** | Multi-dimensional ATS compatibility scoring (0-100) |
| 🤖 **AI Tailoring** | Powered by Grok (xAI) — rewrites bullets, summaries, and skills |
| 📝 **Cover Letters** | AI-generated role-specific cover letters |
| 📊 **Gap Analysis** | Identifies missing keywords, weak verbs, and improvement areas |
| 🔄 **Side-by-Side** | Compare original vs. tailored resume in real-time |
| 📥 **Download** | Export as PDF or DOCX with multiple ATS-friendly templates |
| 📈 **Dashboard** | Track ATS scores, resume history, and improvements |
| 🔐 **Auth** | Secure JWT authentication with user accounts |

---

## 🏗️ Architecture

```
┌─────────────────┐     HTTP/REST      ┌─────────────────┐
│                 │ ◄──────────────── │                 │
│   Next.js 16    │                    │   FastAPI       │
│   Tailwind v4   │ ──────────────► │   Python 3.12   │
│   Port: 3000    │                    │   Port: 8000    │
└─────────────────┘                    └────────┬────────┘
                                                │
                                   ┌────────────┼────────────┐
                                   │            │            │
                              ┌────▼───┐  ┌────▼───┐  ┌────▼───┐
                              │ Grok   │  │ Postgre│  │ Local  │
                              │ xAI API│  │ SQL    │  │ Files  │
                              └────────┘  └────────┘  └────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 20+ and npm
- **Python** 3.12+
- **PostgreSQL** 16+ (or Docker)
- **Grok API Key** from [xAI Console](https://console.x.ai/)

### Option 1: Docker (Recommended)

```bash
# 1. Clone and configure
git clone <your-repo-url> ResumeBuilder
cd ResumeBuilder
cp .env.example .env
# Edit .env with your XAI_API_KEY

# 2. Build and run
docker-compose up --build

# 3. Open
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Setup database
# Make sure PostgreSQL is running, then:
cp .env.example .env
# Edit .env with your database URL and API keys

# Run server
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure API URL
# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Run dev server
npm run dev
```

#### Database Setup
```sql
-- Create database
CREATE DATABASE resumeai;
CREATE USER resumeai WITH PASSWORD 'resumeai_password';
GRANT ALL PRIVILEGES ON DATABASE resumeai TO resumeai;
```

The tables are created automatically on first run via SQLAlchemy.

---

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://...` |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | *Required* |
| `XAI_API_KEY` | Grok API key from xAI | *Required* |
| `XAI_BASE_URL` | Grok API base URL | `https://api.x.ai/v1` |
| `XAI_MODEL` | Grok model to use | `grok-3-mini` |
| `UPLOAD_DIR` | Directory for uploaded files | `./uploads` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |
| `NEXT_PUBLIC_API_URL` | Backend API URL for frontend | `http://localhost:8000/api/v1` |

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/signup` | Register new user |
| POST | `/api/v1/auth/login` | Login and get JWT token |
| GET | `/api/v1/auth/me` | Get current user profile |

### Resumes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/resume/upload` | Upload and parse resume |
| GET | `/api/v1/resume/list` | List user's resumes |
| GET | `/api/v1/resume/{id}` | Get resume details |
| DELETE | `/api/v1/resume/{id}` | Delete resume |

### Tailoring
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tailor/analyze` | Analyze resume vs job description |
| POST | `/api/v1/tailor/generate` | Generate tailored resume |
| POST | `/api/v1/tailor/cover-letter` | Generate cover letter |
| GET | `/api/v1/tailor/history` | Get tailoring history |
| GET | `/api/v1/tailor/{id}` | Get tailored resume |
| GET | `/api/v1/tailor/{id}/download` | Download PDF/DOCX |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |

---

## 📊 ATS Scoring Algorithm

The ATS score is calculated across 6 dimensions:

| Dimension | Weight | Method |
|-----------|--------|--------|
| **Keyword Match** | 30% | TF-IDF cosine similarity between JD and resume keywords |
| **Skills Alignment** | 25% | Exact + fuzzy matching of required vs present skills |
| **Semantic Similarity** | 15% | Sentence-transformer embedding cosine similarity |
| **Action Verb Quality** | 10% | Strong vs weak action verbs analysis |
| **Achievements** | 10% | Detection of quantified results (%, $, numbers) |
| **Formatting** | 10% | ATS-friendly structure checks |

**Score Ranges:**
- 🔴 0-40: Needs significant improvement
- 🟡 41-70: Moderate match, improvements recommended
- 🟢 71-100: Strong ATS compatibility

---

## 📁 Project Structure

```
ResumeBuilder/
├── frontend/                  # Next.js application
│   ├── src/
│   │   ├── app/               # Pages (App Router)
│   │   ├── components/        # React components
│   │   ├── contexts/          # Auth context
│   │   └── lib/               # API client, utilities
│   ├── Dockerfile
│   └── package.json
│
├── backend/                   # FastAPI application
│   ├── app/
│   │   ├── api/routes/        # API endpoints
│   │   ├── core/              # Config, security, database
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── prompts/           # AI prompt templates
│   │   └── utils/             # Utilities
│   ├── templates/             # Resume output templates
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🎨 Resume Templates

| Template | Style | Best For |
|----------|-------|----------|
| **Classic** | Traditional serif, conservative | Finance, Law, Academia |
| **Modern** | Clean sans-serif, accent color | Tech, Marketing, Design |
| **Executive** | Premium whitespace, bold headers | Senior Leadership, C-Suite |

All templates are ATS-friendly: single column, standard fonts, no tables for layout.

---

## 🛡️ Security

- Passwords hashed with bcrypt (12 rounds)
- JWT tokens with configurable expiration
- File upload validation (type + size)
- CORS configuration
- SQL injection prevention via SQLAlchemy ORM
- Input sanitization on all endpoints

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ using FastAPI, Next.js, and Grok AI**

</div>
