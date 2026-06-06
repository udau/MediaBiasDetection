# Project Documentation: News Aggregator Application

## 1. Identify the Software Project, Create Business Case, Arrive at a Problem Statement

### Software Project Identification
The project is a **News Aggregator Application**. It collects, curates, and presents news articles from various online sources (e.g., Fox News) into a single, unified platform. It utilizes a modern frontend (React/TypeScript) and a robust backend (Python) with data stored in DynamoDB, enhanced by machine learning models (Hugging Face) for intelligent content processing.

### Business Case
In today's fast-paced world, users are overwhelmed by the sheer volume of news scattered across multiple platforms. A central aggregator saves time and provides a consolidated view of current events. Value-add services, such as AI-driven sentiment analysis and summaries, elevate the platform above traditional news tracking, opening pathways for user retention and potential premium subscriptions or ad-based revenue.

### Problem Statement
Users struggle to keep up with news from diverse sources, often facing information overload and fragmented user experiences across different websites. There is a critical need for a centralized platform that automatically pulls, categorizes, and presents the latest news in an easy-to-digest format with built-in AI insights.

---

## 2. Analyze Stakeholder and User Description and Identify the appropriate Process Model

### Stakeholders
- **End Users / Readers:** Individuals seeking timely news updates from various sources in one place.
- **Content Providers (Implicit):** News websites from which data is aggregated (via public interfaces/RSS).
- **System Administrators / Moderators:** Personnel managing the platform, monitoring scraper health, and ensuring system uptime.
- **Developers / Engineering Team:** Responsible for building and maintaining the backend, scrapers, and front-end interface.

### User Description
- **Casual Readers:** Looking for quick headlines and overarching trends without reading full articles.
- **Researchers / Power Users:** Need detailed articles, sentiment analysis insights, and specific categorizations via AI.

### Recommended Process Model: Agile (Scrum)
Given the evolving nature of web structures (which affect BeautifulSoup scraping) and iterative enhancements in AI prompt responses, an **Agile (Scrum)** process model is ideal. It allows for iterative development, frequent testing, and the flexibility to adapt to changing source websites or API limits without halting the entire project.

---

## 3. Identify the Requirements, System Requirements, Functional Requirements, Non-Functional Requirements

### System Requirements
**Hardware/Infrastructure:**
- App Server: Minimum 2 Core CPU, 4GB RAM for backend APIs and scraping tasks.
- Storage/Database: Cloud-based NoSQL Database (Amazon DynamoDB).
**Software:**
- Frontend: React UI Framework, TypeScript, Tailwind/Vanilla CSS.
- Backend: Python (e.g., running `main.py`).
- Machine Learning: Hugging Face Transformers (`model.py`).

### Functional Requirements
- **FR1 (Data Aggregation):** The system shall scrape news articles from targeted sources (e.g., Fox News) at regular intervals parsing HTML elements.
- **FR2 (Content Storage):** The system shall store extracted news data (title, link, content, origin source) into AWS DynamoDB.
- **FR3 (AI Integration):** The system shall feature a button that, when clicked, triggers a backend Hugging Face model process to analyze the article heading and display the output directly on the page.
- **FR4 (User Interface):** The system shall display aggregated news in a responsive, modern web interface.

### Non-Functional Requirements
- **NFR1 (Performance):** Scrapers must run asynchronously or as background tasks so they do not block API endpoints for users serving the data.
- **NFR2 (Scalability):** The backend database (DynamoDB) and the Python services must scale dynamically to handle scraping workload spikes (e.g., breaking news events).
- **NFR3 (Resilience):** If a target site changes its DOM and breaks the scraper, the system should log the error without crashing the rest of the application or the user-facing feed.

---

## 4. Prepare Project Plan based on scope, Find Job roles and responsibilities, Calculate Project effort based on resources

### Project Plan and Scope
**Scope Check:** Building robust web scrapers, configuring a NoSQL DB schema, developing the Python backend logic, integrating the HF AI model, and building an interactive React frontend.

### Job Roles and Responsibilities
- **Frontend Developer:** Develop UI in React, bind API data, design the "AI Insight" interactive elements.
- **Backend Developer (Python):** Write `scraper.py`, `main.py` API endpoints, configure boto3 integrations for DB management.
- **Machine Learning Engineer:** Implement `model.py`, select the appropriate Hugging Face NLP model, tune output formatting.
- **QA / Test Engineer:** Identify breakages in the scraper, design user test workflows.

### Project Effort (Estimated)
- Team Size: 3-4 Developers
- Duration: ~10 Weeks
- Total Core Effort: 1200 Person-Hours (Accounting for coding, QA, and deployment configuration)

---

## 5. Prepare the Work Breakdown Structure based on timelines, Risk Identification and Plan

### Work Breakdown Structure (WBS)
- **Phase 1: Foundation (Weeks 1-2)**
  - Requirement finalization, initial architecture setups.
- **Phase 2: Data Acquisition & DB (Weeks 3-5)**
  - Beautiful Soup scraping module (`scraper.py`).
  - DynamoDB creation (Partitions/Sort Keys definition).
- **Phase 3: AI & API Integration (Weeks 6-7)**
  - Integrate Hugging Face via `model.py`.
  - Expose API endpoints fetching from DynamoDB and processing ML requests.
- **Phase 4: Frontend Development (Weeks 8-9)**
  - Setup React, establish API bindings (e.g., `api.ts`), implement responsive design (`index.css`).
- **Phase 5: Testing, Polish & Deployment (Week 10)**

### Risk Identification and Mitigation Plan
- **Risk:** Target website layout changes breaking web scrapers.
  - *Mitigation:* Employ flexible CSS selectors. Have an automated alert testing tool pinging the scraper.
- **Risk:** High Latency when querying the Hugging Face AI model.
  - *Mitigation:* Display loading skeletons in the UI (`App.tsx`), ensuring asynchronous requests prevent UI freezes.

---

## 6. Designing a System Architecture, Use Case Diagram, ER Diagram (Database)

### System Architecture
The application runs on an N-Tier architecture integrating modern Cloud primitives:
1. **Client Tier:** React (+ Vite/TypeScript).
2. **API/Business Tier:** Python Backend connecting scraping, user requests, and model inference.
3. **Data Tier:** AWS DynamoDB.

![System Architecture Diagram](documents/archetecture.pdf)

### Use Case Diagram
- **Actor:** Reader vs Application Admin
- **Use Cases for Reader:** Browse Articles, Trigger AI Tool on Heading, Search/Filter.

![Use Case Diagram](use case diagram.jpg)

### ER Diagram (Database)
As DynamoDB is NoSQL, the "ER" is modeled around access patterns.
- **Article Entity:** `Article_ID` (Partition Key), `Source`, `Headline`, `URL`, `Timestamp` (Sort Key).

*Note: Schema relies on Table Partitions/Sort keys mapped to Article_ID and Timestamp parameters as documented above.*

---

## 7. DFD Diagram (Process) (Up to Level 1), Class Diagram (Applied for OOPS based Project)

### Data Flow Diagram (DFD)
**Level 0 Context:** Reader -> [News Aggregator System] -> Web News Sources
**Level 1 Detailed:**
1. Process 1.0: Scheduled Scraper extracts HTML.
2. Process 2.0: Cleaner formats to JSON, stores to DB.
3. Process 3.0: UI queries backend, rendering results.
4. Process 4.0: Reader triggers AI interaction, fetching NLP results layer.

![Data Flow Diagram Level 0](documents/Level0dfd_media bias.jpg)
![Data Flow Diagram Level 1](documents/dfd1.jpg)

### Class Diagram
Backend Python pseudo-classes:
- `WebScraper(source_url, parser)`
- `DBClient(credentials, table_name)`
- `NLPModel(model_name)` -> processes heading string.

![Class Diagram](documents/Class Diagram.svg)

---

## 8. Create Interaction Diagrams, State chart and Activity Diagrams

### Interaction Diagram
How the frontend (`App.tsx`) communicates with `main.py` which communicates with `model.py` to deliver an AI summarization feature on a specific news element.

![Interaction Diagram](documents/interaction_diagram_media_bias.svg)

### State Chart Diagram
States of an "Article" Object:
`Found in DOM` -> `Parsed Elements` -> `DB Uploaded` -> `Displayed on Client` -> `AI Analyzed (if requested)`.

![State Machine Diagram](documents/State_machine.svg)

### Activity Diagram
Sequential flow of the Python `scraper.py`: Start -> Fetch HTTP Res -> BS4 Parse -> Loop Elements -> Clean text -> Insert -> End.

![Activity Diagram](documents/activity_diagram_media_bias.svg)

---

## 9. Design State and Sequence Diagram, Deployment Diagram

### Sequence Diagram
**Scenario: User requests AI insights for a news headline.**
1. User clicks "Analyze" button on article card.
2. Frontend sends `POST` request to Backend `/api/analyze_heading` with payload.
3. Backend passes heading to `model.py`.
4. HuggingFace model returns sentiment/summary.
5. Backend responds with Result JSON.
6. Frontend updates state and reveals result natively inside the card.

![Sequence Diagram](documents/Sequence_diagram.png)

### Deployment Diagram
Visualizing the AWS setup: User connects via HTTP/HTTPS -> React Build (stored on CDN/S3) -> API Gateway -> Python Backend Container -> connects to DynamoDB and Hugging Face endpoint.

![Deployment Diagram](documents/deployment_diagram_media_bias.svg)

---

## 10. Sample Frontend Design (UI/UX)
The UI applies modern aesthetic rules:
- Clean whitespace, easily legible sans-serif fonts.
- Interactive news cards displaying the image, headline, and source tag.
- A prominent integrated button (e.g., "Ask AI") per card yielding a dropdown or modal containing the Hugging Face model response.

![Frontend UI Mockup](documents/pictures/Screenshot 2026-04-13 123109.png)

---

## 11. Sample code implementation

### Scraper Extraction (Python/BeautifulSoup)
```python
import requests
from bs4 import BeautifulSoup

def scrape_fox_news():
    url = "https://www.foxnews.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = []
    
    for item in soup.select("article"):
        heading = item.find("h2")
        link = item.find("a")
        if heading and link:
            articles.append({
                "heading": heading.text.strip(),
                "url": link.get("href")
            })
    return articles
```

### Hugging Face AI Invocation (`model.py`)
```python
from transformers import pipeline

nlp_pipeline = pipeline("sentiment-analysis") # or summarization

def analyze_heading(heading_text: str):
    # Sends article heading to backend model and returns structured insight
    result = nlp_pipeline(heading_text)
    return result[0]
```

### DB Operations Integration (DynamoDB wrapper)
```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('NewsArticles')

def save_article_to_db(article_data):
    table.put_item(Item={
        'ArticleId': article_data['url'], # using url as unique key
        'Title': article_data['heading'],
        'Source': 'FoxNews'
    })
```

---

## 12. Create a Master Test Plan, Test Case Design

### Master Test Plan
**Objectives:** Verify frontend performance, UI responsiveness, accuracy of Beautiful Soup tag extraction, DB read/write confirmation, and proper async handling of Hugging Face inferences.

### Test Case Design
| Test ID | Feature Set | Description | Expected Value |
|---|---|---|---|
| TC-01 | Scraper System | Execute scraper script against mock HTML | Returns perfectly parsed list of dictionary objects |
| TC-02 | DynamoDB Integration | Write sample parsed json to DB | Item appears successfully in AWS Table Console |
| TC-03 | Hugging Face AI | Inject text "Stock Market Crashes" into `model.py` | Returns predicted negative sentiment confidence score |
| TC-04 | User Interface | Click 'Analyze' button on React Client | Button changes to loading state until API returns |

---

## 13. Manual Testing
Manual evaluation ensures real-world alignment beyond simple unit tests:
1. **Resilience Testing:** Disconnect Wi-Fi during the "Analyze AI" sequence to observe if the frontend cleanly handles API timeout errors rather than crashing.
2. **Visual Inspection:** Verify responsive CSS adjustments down to 320px mobile viewport sizes. Confirm news source labeling text is distinct from headings.
3. **End-to-end Flow:** Boot the Python backend locally, verify DynamoDB environment variables from `.env`, load `App.tsx`, and visually confirm new web records appear instantly.

---

## 14. Analysis of Costing, Efforts and Resources

### Resource Requirements
- AWS Account initialization (DynamoDB usage generally stays in the Free Tier for early startup volume).
- Developer laptops with minimum environment specs (Node.js, Python 3.9+, Git).

### Operational Costing Projection (Monthly scale)
- Database (DynamoDB): ~$20 
- API Server Hosting (EC2 / App Runner or similar): ~$50
- Frontend Distribution (Vercel/Netlify): Free-$20
- Total running system overhead is highly optimal, maintaining under **$100/mo** until major traffic scaling is necessary.

### Cost vs. Benefit Structure
The effort required to set up the robust initial architecture saves long-term labor. Constructing manual news aggregation takes hours daily. This system automates fetching and categorizes content using AI, driving massive operational efficiency and creating immediate user value.
