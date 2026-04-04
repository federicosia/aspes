# Aspes

## Project structure
src/  
├── domain/  
│   ├── model/          # Aggregati, Entity — zero dipendenze  
│   ├── value_objects/  # Dataclass immutabili  
│   ├── events/         # Domain events  
│   ├── ports/          # Interfacce astratte dei repository (ABC)  
│   └── service/        # Use cases, orchestrazione  
│
├── adapters/  
│   ├── persistence/    # ORM models con Base (usati da Alembic)  
│   ├── repositories/   # Implementazioni concrete dei port  
│   ├── mappers/        # Traduzione ORM ↔ Domain  
│   ├── unit_of_work/   # Gestione sessione e commit  
│   └── migrations/     # Alembic versions  
│
├── entrypoints/  
│   ├── routers/        # FastAPI routes  
│   ├── schemas/        # Pydantic request/response  
│   └── dependencies/   # Dependency injection FastAPI  
│
├── db/  
│   ├── session.py      # engine, SessionFactory  
│   └── base.py         # DeclarativeBase  
│
├── config/             # Settings, env vars  
├── tests/  
└── main.py             # App init, lifespan hook  