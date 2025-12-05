from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import create_db_and_tables
from routers import apps, schema_builder, dynamic_data, pages, forms, dashboards, api_endpoints, menus

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {
        "message": "PYCRUD - Dynamic CRUD Builder API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Meta-CRUD Builder routers
app.include_router(apps.router, prefix=settings.API_V1_STR)
app.include_router(schema_builder.router, prefix=settings.API_V1_STR)
app.include_router(dynamic_data.router, prefix=settings.API_V1_STR)

# App Component routers
app.include_router(pages.router, prefix=settings.API_V1_STR)
app.include_router(forms.router, prefix=settings.API_V1_STR)
app.include_router(dashboards.router, prefix=settings.API_V1_STR)
app.include_router(api_endpoints.router, prefix=settings.API_V1_STR)
app.include_router(menus.router, prefix=settings.API_V1_STR)
