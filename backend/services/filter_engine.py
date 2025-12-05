from sqlmodel import Session, select, or_, and_, col
from typing import Any, Dict, List, Optional, Type
from sqlmodel import SQLModel
from datetime import datetime, date


class FilterOperator:
    """Filter comparison operators"""
    EQ = "eq"
    NEQ = "neq"
    LT = "lt"
    LTE = "lte"
    GT = "gt"
    GTE = "gte"
    LIKE = "like"
    ILIKE = "ilike"
    IN = "in"
    NIN = "nin"
    BETWEEN = "between"


class QueryBuilder:
    """Advanced query builder with filtering, sorting, and pagination"""
    
    @staticmethod
    def apply_simple_filters(query, model: Type[SQLModel], filters: Dict[str, Any]):
        """
        Apply simple key-value filters with operators.
        Example: name__eq=John, age__gte=18, status__in=active,pending
        """
        for filter_key, filter_value in filters.items():
            if "__" in filter_key:
                field_name, operator = filter_key.rsplit("__", 1)
            else:
                field_name = filter_key
                operator = FilterOperator.EQ
            
            # Check if it's a relationship filter (e.g., owner.full_name__ilike)
            if "." in field_name:
                query = QueryBuilder._apply_relation_filter(
                    query, model, field_name, operator, filter_value
                )
            else:
                query = QueryBuilder._apply_field_filter(
                    query, model, field_name, operator, filter_value
                )
        
        return query
    
    @staticmethod
    def _apply_field_filter(query, model: Type[SQLModel], field_name: str, operator: str, value: Any):
        """Apply filter to a direct field"""
        if not hasattr(model, field_name):
            return query
        
        field = getattr(model, field_name)
        
        if operator == FilterOperator.EQ:
            query = query.where(field == value)
        elif operator == FilterOperator.NEQ:
            query = query.where(field != value)
        elif operator == FilterOperator.LT:
            query = query.where(field < value)
        elif operator == FilterOperator.LTE:
            query = query.where(field <= value)
        elif operator == FilterOperator.GT:
            query = query.where(field > value)
        elif operator == FilterOperator.GTE:
            query = query.where(field >= value)
        elif operator == FilterOperator.LIKE:
            query = query.where(field.like(f"%{value}%"))
        elif operator == FilterOperator.ILIKE:
            query = query.where(field.ilike(f"%{value}%"))
        elif operator == FilterOperator.IN:
            if isinstance(value, str):
                value = value.split(",")
            query = query.where(field.in_(value))
        elif operator == FilterOperator.NIN:
            if isinstance(value, str):
                value = value.split(",")
            query = query.where(~field.in_(value))
        elif operator == FilterOperator.BETWEEN:
            if isinstance(value, str):
                values = value.split(",")
                if len(values) == 2:
                    query = query.where(field.between(values[0], values[1]))
        
        return query
    
    @staticmethod
    def _apply_relation_filter(query, model: Type[SQLModel], field_path: str, operator: str, value: Any):
        """
        Apply filter to a related field.
        Example: owner.full_name__ilike=John
        """
        parts = field_path.split(".", 1)
        if len(parts) != 2:
            return query
        
        relation_name, relation_field = parts
        
        if not hasattr(model, relation_name):
            return query
        
        relation_model = getattr(model, relation_name).property.mapper.class_
        
        # Join the relation
        query = query.join(relation_model)
        
        # Apply filter on the related field
        if hasattr(relation_model, relation_field):
            field = getattr(relation_model, relation_field)
            
            if operator == FilterOperator.EQ:
                query = query.where(field == value)
            elif operator == FilterOperator.ILIKE:
                query = query.where(field.ilike(f"%{value}%"))
            elif operator == FilterOperator.IN:
                if isinstance(value, str):
                    value = value.split(",")
                query = query.where(field.in_(value))
        
        return query
    
    @staticmethod
    def apply_json_filters(query, model: Type[SQLModel], filter_json: Dict[str, Any]):
        """
        Apply complex JSON filters with AND/OR logic.
        Example:
        {
            "logic": "and",
            "filters": [
                {"field": "status", "op": "eq", "value": "active"},
                {
                    "logic": "or",
                    "filters": [
                        {"field": "priority", "op": "gte", "value": 3},
                        {"field": "name", "op": "ilike", "value": "critical"}
                    ]
                }
            ]
        }
        """
        logic = filter_json.get("logic", "and")
        filters = filter_json.get("filters", [])
        
        if not filters:
            return query
        
        conditions = []
        
        for f in filters:
            if "logic" in f:
                # Nested logic group
                nested_query = select(model)
                nested_query = QueryBuilder.apply_json_filters(nested_query, model, f)
                # Extract the where clause
                if nested_query.whereclause is not None:
                    conditions.append(nested_query.whereclause)
            else:
                # Simple filter
                field_name = f.get("field")
                operator = f.get("op", "eq")
                value = f.get("value")
                
                if hasattr(model, field_name):
                    field = getattr(model, field_name)
                    condition = QueryBuilder._get_condition(field, operator, value)
                    if condition is not None:
                        conditions.append(condition)
        
        if conditions:
            if logic == "or":
                query = query.where(or_(*conditions))
            else:  # and
                query = query.where(and_(*conditions))
        
        return query
    
    @staticmethod
    def _get_condition(field, operator: str, value: Any):
        """Get SQLAlchemy condition for a field and operator"""
        if operator == FilterOperator.EQ:
            return field == value
        elif operator == FilterOperator.NEQ:
            return field != value
        elif operator == FilterOperator.LT:
            return field < value
        elif operator == FilterOperator.LTE:
            return field <= value
        elif operator == FilterOperator.GT:
            return field > value
        elif operator == FilterOperator.GTE:
            return field >= value
        elif operator == FilterOperator.LIKE:
            return field.like(f"%{value}%")
        elif operator == FilterOperator.ILIKE:
            return field.ilike(f"%{value}%")
        elif operator == FilterOperator.IN:
            if isinstance(value, str):
                value = value.split(",")
            return field.in_(value)
        elif operator == FilterOperator.NIN:
            if isinstance(value, str):
                value = value.split(",")
            return ~field.in_(value)
        elif operator == FilterOperator.BETWEEN:
            if isinstance(value, str):
                values = value.split(",")
                if len(values) == 2:
                    return field.between(values[0], values[1])
        return None
    
    @staticmethod
    def apply_sorting(query, model: Type[SQLModel], sort: str):
        """
        Apply sorting to query.
        Example: name:asc,priority:desc
        """
        if not sort:
            return query
        
        sort_items = sort.split(",")
        for item in sort_items:
            if ":" in item:
                field_name, direction = item.split(":", 1)
                field_name = field_name.strip()
                direction = direction.strip().lower()
                
                if hasattr(model, field_name):
                    field = getattr(model, field_name)
                    if direction == "desc":
                        query = query.order_by(field.desc())
                    else:
                        query = query.order_by(field.asc())
        
        return query
    
    @staticmethod
    def apply_pagination(query, page: int = 1, limit: int = 20):
        """
        Apply pagination to query.
        """
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        return query
    
    @staticmethod
    def get_total_count(session: Session, query) -> int:
        """Get total count for pagination"""
        from sqlalchemy import func, select as sa_select
        
        # Create a count query from the existing query
        count_query = select(func.count()).select_from(query.subquery())
        total = session.exec(count_query).one()
        return total
