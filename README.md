# Onboarding Package

A documentation transformation tool that converts scattered GitHub repository docs into a cohesive, readable onboarding handbook for new team members.

---

## What This Project Does

We've all been there: you join a new team and get pointed to a repository with dozens of markdown files, outdated wikis, and scattered documentation that makes no sense in any particular order. This project solves that problem.

The Onboarding Package takes your messy documentation and transforms it into something people actually want to read. It pulls markdown files from any GitHub repository, uses AI to summarize and organize the content, and generates a polished PDF handbook that tells a coherent story from start to finish.

Think of it as a translator between "developer documentation chaos" and "actually useful onboarding material."

---

## How It Works

The system combines several technologies to make this happen:

1. **Content Extraction** - Connects to your GitHub repository and pulls all markdown documentation
2. **AI Processing** - Uses OpenAI to summarize, organize, and create logical flow between documents
3. **Interactive Preview** - Provides a Streamlit web interface to review and adjust the output
4. **PDF Generation** - A .NET backend with IronPDF creates the final, professionally formatted document

---

## Tech Stack

**Frontend and Processing**
- Python for core logic and GitHub integration
- Streamlit for the web-based user interface
- OpenAI API for intelligent content summarization

**Backend and Output**
- .NET for the PDF generation service
- IronPDF for creating high-quality PDF documents

---

## Getting Started

### Prerequisites

Before you begin, make sure you have the following installed on your machine:

- Python 3.8 or higher
- .NET 6.0 SDK or higher
- An OpenAI API key
- A GitHub personal access token (for private repositories)

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/Ashahet1/Onboarding_Package.git
cd Onboarding_Package
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Set up your environment variables by creating a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token
```

Build the .NET PDF service:

```bash
cd pdf-service
dotnet restore
dotnet build
```

---

## Usage

Start the Streamlit application:

```bash
streamlit run app.py
```

From there, you can:

1. Enter the GitHub repository URL you want to process
2. Configure which files and folders to include
3. Preview the AI-generated summaries
4. Adjust the organization and flow of content
5. Generate your final PDF handbook

---

## Why We Built This

Onboarding shouldn't feel like archaeology. New developers deserve documentation that respects their time and actually helps them get productive. This tool exists because we got tired of watching talented people struggle through their first weeks simply because the docs were a mess.

Good documentation is a form of respect for the people who come after you. This tool makes it easier to deliver on that.

---

## Contributing

Contributions are welcome. If you've got ideas for improvements or have found a bug, feel free to open an issue or submit a pull request.

Please keep code changes focused and include clear descriptions of what you're trying to accomplish. We value readable code and thoughtful solutions over clever tricks.

---

## License

This project is open source. See the LICENSE file for details.
