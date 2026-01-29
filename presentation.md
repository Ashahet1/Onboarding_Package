---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
header: 'Onboarding Package Generator'
footer: 'GitHub Documentation → AI-Powered PDF'
---

<!-- _class: lead -->

# **Onboarding Package Generator**

### Turn Messy GitHub Docs into Clean Onboarding Handbooks

*Automated Documentation Generation with AI*

---

## **The Problem** 🤔

- GitHub repositories have scattered documentation
- Markdown files spread across multiple directories
- New developers struggle to understand where to start
- Reading documentation directly on GitHub is not ideal for onboarding
- No unified, readable format for comprehensive learning

---

## **The Solution** ✨

**Onboarding Package Generator** automatically:

1. 📥 Pulls all Markdown files from any GitHub repository
2. 🖼️ Extracts and includes images from documentation
3. 🤖 Summarizes content using OpenAI GPT
4. 📄 Generates a polished, professional PDF handbook
5. 🚀 Provides a user-friendly web interface

---

## **Key Features** 🎯

- **Automated Documentation Fetching** - Direct GitHub API integration
- **AI-Powered Summarization** - Smart content synthesis with OpenAI
- **Image Support** - Preserves diagrams and visual content
- **Professional PDF Output** - Using IronPDF for high-quality rendering
- **Interactive Web Interface** - Built with Streamlit
- **Customizable Metadata** - Author and company information

---

## **Technology Stack** 🛠️

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit (Python) |
| AI Engine | OpenAI GPT API |
| PDF Generation | .NET Core + IronPDF |
| API Framework | ASP.NET Core Web API |
| Language | Python 3.x, C# |
| Repository Access | GitHub API |

---

## **Architecture Overview** 🏗️

```
┌─────────────────┐
│   User Input    │
│  (GitHub URL)   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Streamlit UI   │
│   (Python)      │
└────────┬────────┘
         │
         v
┌─────────────────┐      ┌──────────────┐
│ Repository      │─────▶│   GitHub     │
│ Fetcher         │      │     API      │
└────────┬────────┘      └──────────────┘
         │
         v
┌─────────────────┐      ┌──────────────┐
│   AI           │─────▶│   OpenAI     │
│ Summarizer      │      │     API      │
└────────┬────────┘      └──────────────┘
         │
         v
┌─────────────────┐
│    HTML         │
│   Builder       │
└────────┬────────┘
         │
         v
┌─────────────────┐      ┌──────────────┐
│  .NET PDF API   │─────▶│   IronPDF    │
└────────┬────────┘      └──────────────┘
         │
         v
┌─────────────────┐
│  PDF Download   │
└─────────────────┘
```

---

## **How It Works** 🔄

### Step 1: Fetch Documentation
- User enters GitHub repository URL
- System fetches all Markdown files
- Images are downloaded and stored
- Content is organized by file path

---

## **How It Works** 🔄

### Step 2: AI Summarization
- Each Markdown file is analyzed
- OpenAI GPT generates concise summaries
- Key concepts are extracted
- Technical details are preserved

---

## **How It Works** 🔄

### Step 3: Document Generation
- Summaries compiled into HTML structure
- Images embedded with proper references
- Professional styling applied
- Metadata (author, company) added

---

## **How It Works** 🔄

### Step 4: PDF Creation
- HTML sent to .NET API
- IronPDF renders high-quality PDF
- Document optimized for reading
- Ready for download and distribution

---

## **Project Structure** 📁

```
Onboarding_Package/
├── streamlit_app/         # Main web application
│   ├── app.py            # Streamlit interface
│   ├── repo_fetcher.py   # GitHub API integration
│   ├── ai_summarizer.py  # OpenAI integration
│   └── html_builder.py   # HTML generation
│
├── dotnet_pdf_api/        # PDF generation service
│   ├── Program.cs        # API entry point
│   ├── PdfController.cs  # REST endpoints
│   └── PdfService.cs     # IronPDF logic
│
└── onboard/              # Documentation assets
```

---

## **User Workflow** 👤

1. **Start the Application**
   - Launch Streamlit web interface
   - Ensure .NET API is running

2. **Enter Repository Information**
   - Paste GitHub repository URL
   - Add author name and company

3. **Generate Documentation**
   - Click "Fetch Documentation"
   - Click "Summarize with AI"
   - Click "Generate PDF"

4. **Download and Share**
   - Download the generated PDF
   - Distribute to new team members

---

## **Sample Output** 📊

### What You Get:

✅ Professional cover page with repo information
✅ Table of contents with all documentation
✅ AI-generated summaries for each file
✅ Embedded images and diagrams
✅ Clean, readable formatting
✅ Ready-to-print PDF format

---

## **Benefits** 💪

**For New Developers:**
- Single document to read from start to finish
- Clear, summarized information
- No jumping between multiple files
- Printable reference material

**For Teams:**
- Consistent onboarding experience
- Automated documentation updates
- Time-saving automated process
- Professional brand presentation

---

## **Configuration** ⚙️

### Required Environment Variables:

```bash
# .env file
OPENAI_API_KEY=your_api_key_here
```

### API Endpoints:

```
.NET PDF API: http://localhost:5165
Streamlit App: http://localhost:8501
```

---

## **Technical Highlights** 🌟

- **Scalable Architecture** - Microservices-based design
- **API-First Approach** - RESTful communication
- **Modern UI** - Reactive Streamlit components
- **Error Handling** - Comprehensive exception management
- **Session Management** - Stateful user experience
- **Type Safety** - Strong typing in C# backend

---

## **Use Cases** 💼

1. **Developer Onboarding** - New hire documentation
2. **Open Source Projects** - Community onboarding guides
3. **Internal Tools** - Team knowledge bases
4. **Training Materials** - Educational resources
5. **Client Handoffs** - Project documentation delivery
6. **Archive Creation** - Repository snapshots

---

## **Future Enhancements** 🚀

- 📱 Multi-language support
- 🎨 Custom themes and branding
- 📊 Analytics and metrics
- 🔄 Scheduled automatic updates
- 📧 Email distribution
- 🌐 Deploy as SaaS platform
- 🔐 Enterprise authentication

---

## **Getting Started** 🏁

### Prerequisites:
- Python 3.8+
- .NET 6.0+
- OpenAI API key

### Quick Start:
```bash
# Clone repository
git clone https://github.com/Ashahet1/Onboarding_Package

# Install Python dependencies
cd streamlit_app
pip install -r requirements.txt

# Start .NET API
cd ../dotnet_pdf_api
dotnet run

# Launch Streamlit
cd ../streamlit_app
streamlit run app.py
```

---

## **Demo Time** 🎬

### Live Demonstration

Let's see the Onboarding Package Generator in action!

---

<!-- _class: lead -->

# **Questions?**

### Thank you for your attention!

📧 Contact: contact@example.com
🔗 GitHub: https://github.com/Ashahet1/Onboarding_Package
📚 Documentation: See README.md

---

<!-- _class: lead -->

# **Let's Transform Documentation!**

### From Scattered Markdown to Polished Handbook

*Making onboarding easier, one repository at a time*

