<div align="center">

# 🚀 ResumePilot (V4)

### The AI Employability Operating System & Recruiter-Grade Narrative Platform

*A complete career transition engine. Upload your master resume once, and ResumePilot acts as a deterministic evidence-based resume optimizer, a recruiter simulation engine, and an ATS compatibility evaluator.*

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Grok AI](https://img.shields.io/badge/xAI-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.ai/)

</div>

---

## 🌟 The V4 Evolution

ResumePilot has evolved from a generic AI text generator into a **premium AI-powered Career Intelligence Platform**. 

**Our Core Product Philosophy:** We optimize *REAL evidence* — never hallucinated expertise. The system strictly preserves authenticity, rejects validation failures, and avoids injecting generic corporate buzzwords.

| Module | Description |
|---------|-------------|
| 🧠 **Account-Based Evidence Storage** | Upload your master resume once. The system extracts your entire career into a rich JSON profile. All future tailoring pulls deterministically from this single source of truth. |
| 🎯 **Smart Tailoring Engine** | Paste a JD or job URL. ResumePilot maps your *real* evidence to the role, generating a highly targeted resume that passes ATS and impresses recruiters. |
| 📊 **Career Intelligence** | Real-time market demand graphs, career progression maps, role transition history, and skill gap analysis (You vs. Market). |
| 🎙️ **Interview Simulator** | Generates role-calibrated technical, behavioral, and system design questions based strictly on your master profile evidence and targeted company. |
| 🌐 **Personal Branding Engine** | Auto-generates optimized LinkedIn headlines, GitHub readmes, Portfolio copy, and Twitter strategies using your authentic experience. |

---

## 🏗️ Architecture

ResumePilot is powered by a massively parallel orchestration pipeline comprising over **65 specialized micro-engines**.

```text
┌─────────────────┐     REST / JSON    ┌─────────────────┐
│                 │ ◄──────────────── │                 │
│   Next.js 16    │                   │   FastAPI       │
│   Tailwind v4   │ ──────────────►   │   Python 3.12   │
│   Glass UI/UX   │                   │   65+ AI Engines│
└─────────────────┘                   └────────┬────────┘
                                               │
                                  ┌────────────┼────────────┐
                                  │            │            │
                             ┌────▼───┐   ┌────▼───┐   ┌────▼───┐
                             │ Grok   │   │ Postgre│   │ Vector │
                             │ xAI API│   │ SQL DB │   │ Stores │
                             └────────┘   └────────┘   └────────┘
```

### The 6-Stage V4 Orchestration Pipeline
1. **JD Ingestion:** Parses the job description and extracts required skills, domain focus, and seniority.
2. **Deterministic Evidence Retrieval:** Pulls the candidate's Master JSON Profile.
3. **Semantic Alignment & Gap Analysis:** Identifies what the candidate has vs. what the role needs. Generates a "Skill Gap Report".
4. **Targeted Document Assembly:** Reorders skills, re-weights project significance, and synthesizes a narrative summary.
5. **Truth-Preserving Quality Gates:** Enforces strict anti-hallucination checks to ensure no fake technologies or inflated metrics are added.
6. **Multidimensional Simulation:** Simulates ATS parsing, runs semantic vector similarity, and generates a "Recruiter glance scan heatmap".

*Note: Phase 5 (The Recruiter-Grade Narrative & Humanization System) is actively in development.*

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 20+ and npm
- **Python** 3.12+
- **PostgreSQL** 16+ (or use Docker)
- **Grok API Key** from [xAI Console](https://console.x.ai/)

### Local Development

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Setup database
cp .env.example .env
# Edit .env with your database URL and xAI API keys

# Run server
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure API URL
# Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Run dev server
npm run dev
```

---

## 🛡️ Strict Anti-Hallucination Guardrails

ResumePilot implements strict safeguards:
- **No Invented Technologies:** If a technology isn't in your Master Profile, it won't be on the tailored resume.
- **No Fabricated Projects:** The system re-weighs existing projects based on JD relevance but never invents new ones.
- **Metric Realism:** Enforces authentic internship/junior-level phrasing and strips out exaggerated "enterprise-scale" claims.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ using FastAPI, Next.js, and Grok AI**

</div>
