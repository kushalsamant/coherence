# ASK: Daily Research - Text-Based Research Tool

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Online SaaS research tool that generates high-quality Q&A content across any research topic or theme.**

## 💝 Support ASK: Daily Research

**Help us democratize research knowledge and make academic content accessible to everyone!**

🔬 **What we're building**: A revolutionary online research tool that transforms complex academic concepts into engaging, shareable Q&A content.

🎯 **Our mission**: Bridge the gap between academic research and public understanding by creating accessible, educational content.

### 🌟 Why Sponsor ASK?

- **📚 Educational Impact**: Every sponsorship helps create more educational content for students, researchers, and curious minds worldwide
- **🔬 Research Democratization**: Making complex research accessible through clear, well-structured Q&A pairs
- **💻 Open Source Excellence**: Supporting sustainable development of cutting-edge research tools
- **🌍 Global Knowledge Sharing**: Enabling researchers to share their work in accessible formats

### 🎁 Support Our Mission

**Every contribution, no matter the size, makes a difference!**

Your support enables us to:
- 🚀 Develop new research themes and content types
- 🔧 Improve content generation quality and reliability  
- 📱 Create mobile apps and additional platforms
- 🌐 Build a global research content community
- 🎓 Provide free educational resources to students

**[Become a GitHub Sponsor →](https://github.com/sponsors/kushalsamant)**

**Every contribution helps us make research more accessible and engaging for everyone!** 💙

---

*"The best way to predict the future is to create it." - Let's build the future of research communication together!*

## 🌟 Overview

ASK is an online SaaS research tool that automatically generates comprehensive question-answer pairs. Built with a focus on research methodology, sustainability science, engineering systems, and unlimited theme exploration, it creates structured Q&A content perfect for research and learning.

### ✨ Key Features

- **🌐 Online SaaS**: Cloud-based research tool accessible from anywhere
- **🤖 Template-Based Generation**: Multi-theme support with connected, chained-like experience
- **📊 Comprehensive Logging**: Detailed CSV tracking and volume management
- **🧠 Intelligent Content Generation**: Unlimited research theme exploration
- **🎯 Sequential Knowledge Building**: Questions and answers numbered systematically (ASK-01, ASK-02, etc.)
- **🔓 Unlimited Themes**: Explore any research topic - no restrictions on themes

## 🎨 What Makes ASK Special?

### **🧠 Intelligent Content Generation**
- **Unlimited Theme Support**: Explore any research topic or theme - no predefined limitations
- **Sequential Knowledge Building**: Questions and answers are numbered sequentially (ASK-01, ASK-02, etc.) for systematic learning
- **Sentence-Case Answers**: All content is professionally formatted for readability
- **Research Focus**: Every piece of content is specifically tailored to research and practice
- **Connected Q&A**: Questions reference previous content for a chained learning experience

### **⚡ Modern Technology Stack**
- **Frontend**: Next.js 16, React, TypeScript (hosted on Vercel)
- **Backend**: FastAPI, Python 3.8+ (hosted on Render)
- **Database**: PostgreSQL (via Render)
- **Caching**: Redis (via Render or Upstash)
- **Payments**: Razorpay (unified payment gateway)
- **AI**: Groq API (Llama 3.1 70B)
- **Storage**: CSV-based logging (with PostgreSQL for user/subscription data)
- **Authentication**: Google OAuth (NextAuth)

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+** (for frontend)
- **Internet connection** (for online SaaS operation)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kushalsamant/kushalsamant.github.io.git
cd kushalsamant.github.io/apps/ask
```

2. **Install backend dependencies**
```bash
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
```

4. **Configure environment**
```bash
# Environment variables are in ask.env.production at the repository root
# For local development, create .env.local files (not committed to git)
# The application automatically loads from the centralized location first
```

5. **Run the backend**
```bash
cd api
uvicorn main:app --reload
```

6. **Run the frontend** (in another terminal)
```bash
cd frontend
npm run dev
```

### 🎯 First Run
- **Content Generation**: Automatic generation of research Q&A pairs
- **Text Output**: High-quality Q&A pairs logged to `log.csv`
- **Web Interface**: Browse and manage content at `http://localhost:3000`

## 📋 Usage Modes

### 🎯 Text-Only Mode (Default)
```bash
python main_text_only.py
```
Generates Q&A pairs with multi-theme support and connected, chained-like experience.

### 📖 Help
```bash
python main_text_only.py --help
```
Shows all available modes and options.

## 🏗️ System Architecture

### Online SaaS Design
```
User Request
    ↓
FastAPI Backend
    ↓
Template-Based Generation
    ↓
CSV Logging
    ↓
Next.js Frontend Display
```

### Core Components

| Component | Purpose | Status |
|-|-|-|
| `main_text_only.py` | Main pipeline orchestrator | ✅ Active |
| `offline_question_generator.py` | Template-based question generation | ✅ Active |
| `offline_answer_generator.py` | Template-based answer generation | ✅ Active |
| `volume_manager.py` | Volume tracking | ✅ Active |
| `research_csv_manager.py` | CSV logging and data management | ✅ Active |
| `api/` | FastAPI backend server | ✅ Active |
| `frontend/` | Next.js web interface | ✅ Active |

## ⚙️ Configuration

### Environment Variables

**Standardized Infrastructure Stack:**
- **Vercel**: Frontend hosting
- **Render**: Backend hosting + PostgreSQL + Redis
- **Razorpay**: Payment processing
- **Groq**: AI inference
- **Google OAuth**: Authentication

**Required Environment Variables:**

> **⚠️ Configuration:** All production environment variables are in `ask.env.production` at the repository root

Key configuration options (in `ask.env.production`):

```env
# Groq AI Configuration
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-70b-versatile

# Database (PostgreSQL from Render)
DATABASE_URL=postgresql://user:password@host:port/database

# Redis (optional, for caching)
REDIS_URL=redis://localhost:6379/0
# Or use Upstash:
# UPSTASH_REDIS_REST_URL=https://...upstash.io
# UPSTASH_REDIS_REST_TOKEN=...

# Razorpay Payments
# Note: Code accepts both prefixed (ASK_RAZORPAY_*) and unprefixed (RAZORPAY_*)
# variables. Prefixed versions are preferred in .env files for organization.

# Prefixed versions (recommended)
ASK_RAZORPAY_KEY_ID=rzp_test_...
ASK_RAZORPAY_KEY_SECRET=...
ASK_RAZORPAY_WEBHOOK_SECRET=whsec_...
# Pricing amounts (shared across all projects: ASK, Sketch2BIM, Reframe)
ASK_RAZORPAY_WEEK_AMOUNT=129900
ASK_RAZORPAY_MONTH_AMOUNT=349900
ASK_RAZORPAY_YEAR_AMOUNT=2999900
# Plan IDs (shared across all projects - same plan IDs for all apps)
ASK_RAZORPAY_PLAN_WEEK=  # Set up later
ASK_RAZORPAY_PLAN_MONTH= # Set up later
ASK_RAZORPAY_PLAN_YEAR=  # Set up later

# Unprefixed versions (also work, for backward compatibility)
# RAZORPAY_KEY_ID=rzp_test_...
# RAZORPAY_KEY_SECRET=...
# RAZORPAY_WEBHOOK_SECRET=whsec_...
# RAZORPAY_WEEK_AMOUNT=129900
# RAZORPAY_MONTH_AMOUNT=349900
# RAZORPAY_YEAR_AMOUNT=2999900
# RAZORPAY_PLAN_WEEK=  # Set up later
# RAZORPAY_PLAN_MONTH= # Set up later
# RAZORPAY_PLAN_YEAR=  # Set up later

# Google OAuth
ASK_GOOGLE_CLIENT_ID=your_google_client_id
ASK_GOOGLE_SECRET=your_google_client_secret

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Logging
LOG_DIR=logs
LOG_CSV_FILE=log.csv
```

### Research Themes

**The tool supports unlimited research topics and themes.** You can explore any research area including:

- Research methodology
- Sustainability science
- Engineering systems
- Technology innovation
- Urban planning
- Architecture
- Marketing
- Sports research
- Environmental design
- Spatial design
- Digital technology
- And any other research topic you want to explore!

## 📊 Output Structure

### Generated Content

Each run creates:
- **Question**: Research question text
- **Answer**: Comprehensive answer text
- **CSV Entry**: Logged to `log.csv` with metadata

### File Organization

```
ask/
├── api/                    # FastAPI backend
├── frontend/               # Next.js frontend
├── logs/                   # Execution logs
└── log.csv                 # Q&A tracking database
```

### CSV Logging

The system maintains detailed logs in `log.csv`:

| Column | Description |
|-|-|
| `question_number` | Sequential identifier |
| `theme` | Research theme |
| `question` | Generated question |
| `answer` | Generated answer |
| `is_used` | Boolean flag |
| `created_timestamp` | Creation timestamp |

## 🔧 Advanced Features

### Volume Management

- **Automatic numbering**: Sequential question numbers (ASK-001, ASK-002, etc.)
- **Volume tracking**: Organizes content into manageable volumes
- **Duplicate prevention**: Prevents duplicate question generation

## 💡 Perfect For:

### **🏢 Research Professionals**
- **Research Inspiration**: Daily research questions and insights
- **Knowledge Building**: Systematic exploration of research concepts
- **Content Management**: Organize and track research Q&A pairs

### **🎓 Students & Educators**
- **Learning Tool**: Structured research content
- **Research Projects**: Ready-to-use research content
- **Educational Resources**: Professional-quality Q&A pairs

### **🔬 Researchers & Innovators**
- **Unlimited Theme Exploration**: Explore any research topic without restrictions
- **Content Generation**: Automated research question and answer creation
- **Knowledge Management**: Systematic organization of research content

### **💼 Content Creators**
- **Research Content**: Daily research content for any field
- **Professional Branding**: Consistent ASK branding and numbering
- **Flexible Topics**: Generate content for any research theme

## 🛠️ Development

### Project Structure

```
ask/
├── api/                          # FastAPI backend
│   ├── main.py                  # FastAPI app
│   ├── routes/                  # API endpoints
│   └── services/                # Business logic
├── frontend/                     # Next.js frontend
│   ├── app/                     # Next.js app directory
│   ├── components/              # React components
│   └── lib/                     # Utilities
├── main_text_only.py            # Main pipeline
├── offline_question_generator.py # Question generation
├── offline_answer_generator.py   # Answer generation
├── volume_manager.py            # Volume tracking
├── research_csv_manager.py      # CSV management
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Key Modules

- **`main_text_only.py`**: Pipeline orchestrator
- **`offline_question_generator.py`**: Template-based question generation
- **`offline_answer_generator.py`**: Template-based answer generation
- **`volume_manager.py`**: Volume tracking
- **`research_csv_manager.py`**: CSV logging and data management
- **`api/`**: FastAPI REST API server
- **`frontend/`**: Next.js web interface

### Dependencies

Core dependencies include:
- **FastAPI**: Web framework for REST API
- **Next.js**: React framework for frontend
- **python-dotenv**: Environment variable management
- **requests**: HTTP library for API calls

## 📈 Performance

### System Requirements

| Component | Minimum | Recommended |
|-|-|-|
| **CPU** | Multi-core | 4+ cores |
| **RAM** | 2GB | 4GB+ |
| **Storage** | 100MB | 500MB+ |

## 🔍 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
pip install -r requirements.txt --upgrade
```

**2. Frontend Build Errors**
```bash
cd frontend
npm install
npm run build
```

**3. API Connection Issues**
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `ask.env.production` or local `.env.local`
- Ensure CORS is configured correctly

### Log Files

- **`logs/execution.log`**: Detailed execution logs
- **`log.csv`**: Q&A content database

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
git clone https://github.com/kushalsamant/kushalsamant.github.io.git
cd kushalsamant.github.io/apps/ask
pip install -r requirements.txt
cd frontend && npm install
# Environment variables are in ask.env.production at the repository root
# For local development, create .env.local files (not committed to git)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Research Community**: For inspiration and feedback
- **FastAPI Team**: For the excellent web framework
- **Next.js Team**: For the React framework

## 📞 Support

- **Repository**: [Monorepo - apps/ask](https://github.com/kushalsamant/kushalsamant.github.io/tree/main/apps/ask)
- **Issues**: [GitHub Issues](https://github.com/kushalsamant/kushalsamant.github.io/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kushalsamant/kushalsamant.github.io/discussions)

---

**Made with ❤️ for the research community**

*Generate, explore, and share knowledge with ASK: Daily Research*
