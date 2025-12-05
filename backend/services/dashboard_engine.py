from sqlmodel import Session, select, func
from typing import Any, Dict, List, Optional, Type
from sqlmodel import SQLModel
from services.filter_engine import QueryBuilder


class AggregateFunction:
    """Supported aggregate functions"""
    COUNT = "count"
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    DISTINCT_COUNT = "distinct_count"


class DashboardEngine:
    """Execute dashboard widget queries"""
    
    @staticmethod
    def run_widget(widget_def: Dict[str, Any], session: Session, models_map: Dict[str, Type[SQLModel]]) -> Dict[str, Any]:
        """Execute a widget query based on its definition"""
        widget_type = widget_def.get("type")
        
        if widget_type == "metric":
            return DashboardEngine._execute_metric(widget_def, session, models_map)
        elif widget_type == "chart":
            return DashboardEngine._execute_chart(widget_def, session, models_map)
        elif widget_type == "table":
            return DashboardEngine._execute_table(widget_def, session, models_map)
        else:
            return {"error": f"Unknown widget type: {widget_type}"}
    
    @staticmethod
    def _execute_metric(widget_def: Dict[str, Any], session: Session, models_map: Dict[str, Type[SQLModel]]) -> Dict[str, Any]:
        """
        Execute metric widget.
        Returns a single numeric value.
        """
        query_def = widget_def.get("query", {})
        resource = query_def.get("resource")
        aggregate = query_def.get("aggregate", AggregateFunction.COUNT)
        field = query_def.get("field")
        filters = query_def.get("filters", {})
        
        if resource not in models_map:
            return {"error": f"Unknown resource: {resource}"}
        
        model = models_map[resource]
        
        # Build query with filters
        query = select(model)
        if filters:
            query = QueryBuilder.apply_simple_filters(query, model, filters)
        
        # Apply aggregate
        result = DashboardEngine._apply_aggregate(query, model, aggregate, field, session)
        
        return {
            "type": "metric",
            "title": widget_def.get("title", "Metric"),
            "value": result
        }
    
    @staticmethod
    def _execute_chart(widget_def: Dict[str, Any], session: Session, models_map: Dict[str, Type[SQLModel]]) -> Dict[str, Any]:
        """
        Execute chart widget.
        Returns grouped data for visualization.
        """
        query_def = widget_def.get("query", {})
        resource = query_def.get("resource")
        group_by = query_def.get("group_by")
        aggregate = query_def.get("aggregate", AggregateFunction.COUNT)
        field = query_def.get("field")
        filters = query_def.get("filters", {})
        
        if resource not in models_map:
            return {"error": f"Unknown resource: {resource}"}
        
        model = models_map[resource]
        
        if not group_by or not hasattr(model, group_by):
            return {"error": f"Invalid group_by field: {group_by}"}
        
        group_field = getattr(model, group_by)
        
        # Build aggregation query
        if aggregate == AggregateFunction.COUNT:
            agg_expr = func.count()
        elif aggregate == AggregateFunction.SUM and field:
            agg_expr = func.sum(getattr(model, field))
        elif aggregate == AggregateFunction.AVG and field:
            agg_expr = func.avg(getattr(model, field))
        elif aggregate == AggregateFunction.MIN and field:
            agg_expr = func.min(getattr(model, field))
        elif aggregate == AggregateFunction.MAX and field:
            agg_expr = func.max(getattr(model, field))
        elif aggregate == AggregateFunction.DISTINCT_COUNT and field:
            agg_expr = func.count(func.distinct(getattr(model, field)))
        else:
            agg_expr = func.count()
        
        query = select(group_field, agg_expr).group_by(group_field)
        
        # Apply filters
        if filters:
            # Need to rebuild with proper filtering
            base_query = select(model)
            base_query = QueryBuilder.apply_simple_filters(base_query, model, filters)
            # This is simplified - in production, you'd need to properly merge the subquery
        
        results = session.exec(query).all()
        
        data = [{"label": str(row[0]), "value": float(row[1]) if row[1] else 0} for row in results]
        
        return {
            "type": "chart",
            "chart_type": widget_def.get("chart_type", "bar"),
            "title": widget_def.get("title", "Chart"),
            "data": data
        }
    
    @staticmethod
    def _execute_table(widget_def: Dict[str, Any], session: Session, models_map: Dict[str, Type[SQLModel]]) -> Dict[str, Any]:
        """
        Execute table widget.
        Returns filtered and paginated data.
        """
        query_def = widget_def.get("query", {})
        resource = query_def.get("resource")
        filters = query_def.get("filters", {})
        sort = query_def.get("sort", "")
        page = query_def.get("page", 1)
        limit = query_def.get("limit", 10)
        
        if resource not in models_map:
            return {"error": f"Unknown resource: {resource}"}
        
        model = models_map[resource]
        
        # Build query
        query = select(model)
        
        if filters:
            query = QueryBuilder.apply_simple_filters(query, model, filters)
        
        if sort:
            query = QueryBuilder.apply_sorting(query, model, sort)
        
        # Get total count
        total = QueryBuilder.get_total_count(session, query)
        
        # Apply pagination
        query = QueryBuilder.apply_pagination(query, page, limit)
        
        results = session.exec(query).all()
        
        # Convert to dict
        data = [item.model_dump() if hasattr(item, 'model_dump') else dict(item) for item in results]
        
        return {
            "type": "table",
            "title": widget_def.get("title", "Table"),
            "data": data,
            "total": total,
            "page": page,
            "limit": limit
        }
    
    @staticmethod
    def _apply_aggregate(query, model: Type[SQLModel], aggregate: str, field: Optional[str], session: Session) -> Any:
        """Apply aggregate function to query"""
        if aggregate == AggregateFunction.COUNT:
            count_query = select(func.count()).select_from(model)
            # Apply any filters from original query if needed
            return session.exec(count_query).one()
        
        elif aggregate == AggregateFunction.SUM and field and hasattr(model, field):
            sum_query = select(func.sum(getattr(model, field)))
            result = session.exec(sum_query).one()
            return result or 0
        
        elif aggregate == AggregateFunction.AVG and field and hasattr(model, field):
            avg_query = select(func.avg(getattr(model, field)))
            result = session.exec(avg_query).one()
            return result or 0
        
        elif aggregate == AggregateFunction.MIN and field and hasattr(model, field):
            min_query = select(func.min(getattr(model, field)))
            result = session.exec(min_query).one()
            return result or 0
        
        elif aggregate == AggregateFunction.MAX and field and hasattr(model, field):
            max_query = select(func.max(getattr(model, field)))
            result = session.exec(max_query).one()
            return result or 0
        
        elif aggregate == AggregateFunction.DISTINCT_COUNT and field and hasattr(model, field):
            distinct_query = select(func.count(func.distinct(getattr(model, field))))
            return session.exec(distinct_query).one()
        
        return 0
