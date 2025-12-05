from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session
from typing import Dict, Any
import json
from pathlib import Path
from core.database import get_session
from services.dashboard_engine import DashboardEngine
from models.project import Project
from models.user import User
from models.tag import Tag

router = APIRouter(prefix="/dashboards", tags=["dashboards"])

# Models map for dashboard engine
MODELS_MAP = {
    "project": Project,
    "user": User,
    "tag": Tag,
}


def load_dashboard_schema():
    """Load dashboard schema from JSON file"""
    schema_path = Path(__file__).parent.parent / "dashboards" / "schema.json"
    with open(schema_path, "r") as f:
        return json.load(f)


@router.get("/")
def list_dashboards():
    """List all available dashboards"""
    schema = load_dashboard_schema()
    dashboards = schema.get("dashboards", [])
    
    return {
        "data": [
            {
                "id": d.get("id"),
                "name": d.get("name"),
                "title": d.get("title"),
                "description": d.get("description"),
            }
            for d in dashboards
        ]
    }


@router.get("/{dashboard_id}")
def get_dashboard(dashboard_id: str):
    """Get dashboard definition"""
    schema = load_dashboard_schema()
    dashboards = schema.get("dashboards", [])
    
    dashboard = next((d for d in dashboards if d.get("id") == dashboard_id), None)
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    return dashboard


@router.post("/run")
def run_dashboard(
    dashboard_def: Dict[str, Any] = Body(...),
    session: Session = Depends(get_session)
):
    """
    Execute all widgets in a dashboard.
    
    Example payload:
    {
        "widgets": [
            {
                "type": "metric",
                "title": "Total Projects",
                "query": {
                    "resource": "project",
                    "aggregate": "count"
                }
            }
        ]
    }
    """
    widgets = dashboard_def.get("widgets", [])
    results = []
    
    for widget in widgets:
        try:
            result = DashboardEngine.run_widget(widget, session, MODELS_MAP)
            results.append(result)
        except Exception as e:
            results.append({
                "error": str(e),
                "widget": widget.get("title", "Unknown")
            })
    
    return {"results": results}


@router.post("/widget")
def run_widget(
    widget_def: Dict[str, Any] = Body(...),
    session: Session = Depends(get_session)
):
    """
    Execute a single widget query.
    
    Example payload:
    {
        "type": "chart",
        "chart_type": "bar",
        "title": "Projects by Status",
        "query": {
            "resource": "project",
            "group_by": "status",
            "aggregate": "count"
        }
    }
    """
    try:
        result = DashboardEngine.run_widget(widget_def, session, MODELS_MAP)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{dashboard_id}/execute")
def execute_dashboard(dashboard_id: str, session: Session = Depends(get_session)):
    """Execute a predefined dashboard by ID"""
    schema = load_dashboard_schema()
    dashboards = schema.get("dashboards", [])
    
    dashboard = next((d for d in dashboards if d.get("id") == dashboard_id), None)
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    widgets = dashboard.get("widgets", [])
    results = []
    
    for widget in widgets:
        try:
            result = DashboardEngine.run_widget(widget, session, MODELS_MAP)
            results.append(result)
        except Exception as e:
            results.append({
                "error": str(e),
                "widget": widget.get("title", "Unknown")
            })
    
    return {
        "dashboard": {
            "id": dashboard.get("id"),
            "name": dashboard.get("name"),
            "title": dashboard.get("title"),
        },
        "results": results
    }
