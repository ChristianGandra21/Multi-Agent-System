# Multi-Agent Autonomous Research System

A production-grade research and analysis platform that orchestrates multiple AI agents (Research, Data Analysis, Code Execution, and Writing) to generate executive-level reports with real-time data visualization.

## Technical Differentiators

### Multi-Agent Orchestration Architecture

Implements LangGraph for complex workflow orchestration, enabling cyclic agent interactions and autonomous decision-making. Each agent operates independently while maintaining state consistency across the execution pipeline.

### Enterprise-Grade Async Processing

Built on FastAPI with Celery and Redis for distributed task queuing. Handles long-running research operations without blocking the main application thread, enabling concurrent multi-user workloads.

### Container-Native Infrastructure

Fully containerized microservices architecture using Docker Compose. Zero-configuration deployment with isolated services for API, worker processes, database, and cache layer.

### Real-Time Status Streaming

React-based frontend with TypeScript implements polling-based status updates, providing live feedback on agent execution progress and task completion.

### Dynamic Code Execution

Integrated Python code interpreter that generates and executes data visualization scripts on-demand, converting matplotlib charts to base64-encoded images for client-side rendering.

## System Architecture

The system implements a four-stage agent pipeline:

**Research Agent**: Executes web searches via Tavily API, collecting relevant sources from trusted domains and filtering for content quality.

**Data Extraction Agent**: Analyzes collected research to identify and extract structured data points, metrics, and quantitative information suitable for visualization.

**Code Execution Agent**: Generates Python visualization scripts using matplotlib and pandas, executes them in a sandboxed environment, and returns base64-encoded chart images.

**Writer Agent**: Synthesizes all gathered information into structured markdown reports with executive summaries, key findings, and supporting data analysis.

## Technology Stack

**Backend**

- Python 3.10+ with FastAPI 0.109.0
- LangChain 0.3.15 + LangGraph 0.2.55
- Groq API (Llama 3.3 70B)
- Celery 5.3.4 for distributed task processing
- PostgreSQL 13 with SQLAlchemy ORM
- Redis 5.0 for message broker

**Frontend**

- React 18 with TypeScript
- Tailwind CSS for styling
- Axios for HTTP client
- Lucide React for iconography

**Infrastructure**

- Docker & Docker Compose
- Multi-stage builds for optimization
- Network isolation between services

**AI & Data Processing**

- LangChain for LLM orchestration
- Tavily API for web research
- Matplotlib + Pandas + NumPy for data visualization

## Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Groq API key ([Get here](https://console.groq.com))
- Tavily API key ([Get here](https://tavily.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/seu-usuario/Multi-Agent-System.git
cd Multi-Agent-System

# Create environment configuration
cat > .env << EOF
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
DATABASE_URL=postgresql://postgres:postgres@db:5432/research_db
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
EOF

# Launch the entire infrastructure
docker-compose up --build
```

**Access Points**:

- Frontend Application: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- API Base URL: http://localhost:8000

### Usage

1. Navigate to http://localhost:3000
2. Enter a research query (e.g., "analyze renewable energy adoption trends in 2026")
3. Monitor real-time agent execution status
4. View generated report with data visualizations

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── agents/          # Agent node implementations
│   │   │   ├── research_node.py
│   │   │   ├── data_node.py
│   │   │   ├── code_node.py
│   │   │   ├── writer_node.py
│   │   │   ├── graph.py     # LangGraph workflow definition
│   │   │   └── llm_config.py
│   │   ├── main.py          # FastAPI application
│   │   ├── worker.py        # Celery task definitions
│   │   ├── models.py        # SQLAlchemy models
│   │   └── schemas.py       # Pydantic schemas
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   └── App.tsx          # Main application
│   └── package.json
├── docker-compose.yml       # Service orchestration
├── Dockerfile              # Backend container
└── README.md
```

## API Endpoints

### POST /research

Initiates a new research task.

**Request Body**:

```json
{
  "query": "your research query"
}
```

**Response**:

```json
{
  "id": 1,
  "query": "your research query",
  "status": "pending",
  "created_at": "2026-01-08T12:00:00"
}
```

### GET /research/{id}

Retrieves research task status and results.

**Response** (completed):

```json
{
  "id": 1,
  "status": "completed",
  "final_report": "# Executive Summary...",
  "research_data": [...],
  "analysis_data": {...},
  "code_outputs": {
    "chart_base64": "iVBORw0KGgoAAAANS..."
  },
  "completed_at": "2026-01-08T12:05:00"
}
```

## Performance Characteristics

- Average research completion time: 30-60 seconds
- Concurrent task capacity: 10+ simultaneous research operations
- Database connection pooling for optimized query performance
- Redis-based result caching for completed tasks

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Local Development (without Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Celery worker
celery -A app.celery_app worker --loglevel=info

# Frontend
cd frontend
npm install
npm start
```

## Known Limitations

- Groq API dependency resolver may install incompatible version (0.9.0 instead of 0.37.1). Workaround: `docker exec research_celery_worker pip install --upgrade groq==0.37.1`
- Chart generation depends on availability of numeric data in research results
- Tavily API rate limits apply based on subscription tier

## Future Enhancements

- Implement WebSocket connections for true real-time updates
- Add support for multi-document report generation
- Integrate vector database for semantic search across historical reports
- Implement agent memory for contextual follow-up queries
- Add export functionality (PDF, DOCX formats)


## Author

[Your Name](https://github.com/ChristianGandra21)

**LinkedIn**: [linkedin.com/in/your-profile](https://linkedin.com/in/christian-gandra)
