# AnxinBao Insurance AI Agent Service
AnxinBao is an online insurance mall with an AI insurance advisor. It supports users to browse insurance products, view insurance plans, consult insurance clauses and claim guidance.
This repository is the backend agent-service based on FastAPI.

## System Architecture
The whole system consists of two parts:
- **frontend**: React + Ant Design insurance mall UI, ready-made, no need to develop
- **agent-service (this project)**: Python FastAPI backend
  - Traditional insurance business: user authentication, product query, premium calculation, order & policy management, claim records
  - AI Agent & RAG: intent recognition, insurance recommendation, clause QA, claim consultation, streaming LLM reply

## Tech Stack
| Layer | Technology |
| ---- | ---- |
| Web Framework | FastAPI |
| AI Orchestration | LangGraph (state graph) + LangChain (LLM / tools / messages) |
| LLM | DeepSeek (OpenAI compatible interface) |
| Vector Database | Milvus 2.6 |
| Relational Database | PostgreSQL 16 |
| Frontend | React + Ant Design |
| Package Manager | uv |
| Deployment | Docker Compose |

## Infrastructure Ports
| Service | Port | Description |
| ---- | ---- | ---- |
| PostgreSQL | 5432 | Business data & conversation history, default DB: `insurance`, user: `insurance` / `insurance123` |
| Milvus | 19530 | Vector storage & retrieval |
| etcd | 2379 | Milvus metadata storage |
| MinIO | 9000/9001 | Milvus object storage |
| Attu | 3000 | Milvus web management UI |

## Project Structure
agent-service/
├── app/
│   ├── core/                # Core config, logging
│   │   ├── config.py        # pydantic-settings env management
│   │   └── logging.py       # Structlog configuration
│   ├── common/              # Common base model & mixin
│   │   └── models.py        # SQLAlchemy Base, created_at / updated_at mixin
│   ├── infra/               # Infrastructure
│   │   └── database.py      # Async SQLAlchemy engine, session pool, lifespan handler
│   ├── modules/             # Business modules
│   │   └── product/         # Insurance product module
│   │       ├── models.py    # SQLAlchemy ORM model
│   │       ├── schemas.py   # Pydantic request & response schema
│   │       ├── repository.py# DB access layer
│   │       ├── service.py   # Business logic layer
│   │       └── router.py    # FastAPI route definition
│   └── main.py              # FastAPI entry & lifespan
├── .env                     # Environment variables
├── pyproject.toml           # uv dependencies
└── notebooks/               # Test notebooks

```

## Environment Preparation
### 1. Start Infrastructure
```shell
# Enter deploy directory
cd deploy
# Start all services
docker compose up -d
```

After startup, verify all services are `Healthy`.

- PostgreSQL connection: `insurance` / `insurance123`
- Milvus Attu web: [http://192.168.150.101:3000](http://192.168.150.101:3000)

### 2. Frontend Startup

```
cd frontend
npm install
npm run dev
```

Frontend access: [http://localhost:5173](http://localhost:5173)

### 3. Backend Dependency Install

```
uv sync
```

### 4. Environment Configuration

Copy `.env` and fill your DeepSeek key:

```
# App
APP_NAME=AnxinBao
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8001

# Log
LOGGING_LEVEL=INFO

# PostgreSQL
DB_HOST=192.168.150.101
DB_PORT=5432
DB_NAME=insurance
DB_USER=insurance
DB_PASSWORD=insurance123

# LLM
DEEPSEEK_API_KEY=your_deepseek_api_key
CHAT_MODEL=deepseek-v4-flash
```

### 5. Run Backend Service

```
uv run python -m app.main
```

FastAPI docs: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

## API List

### Product APIs

1. Get product list
`GET /api/v1/products`
Query params:

- `category` (optional): filter product type, e.g. `medical`, `critical_illness`, `life`, `accident`

2. Get candidate products for AI recommendation
`GET /api/v1/products/candidates`
Query params:

- `categories` (required, multiple): product categories
- `premium_min` (optional): filter products whose min_premium is lower than this value
- `limit_per_category` (optional, default=5): max items per category

## Development Specification

Adopt layered architecture: `Router → Service → Repository`

- Router: HTTP layer, parameter validation, dependency injection
- Service: business logic, data assembly
- Repository: pure database access, no business logic
- Schema: API request/response serialization
- Model: SQLAlchemy ORM mapping for database table

## License

MIT
