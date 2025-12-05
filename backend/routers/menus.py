"""
Menus Router - Manage navigation menu configurations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from core.database import get_session
from models.schema_builder import MenuConfig, MenuConfigCreate, MenuConfigUpdate, MenuConfigRead, App

router = APIRouter(prefix="/apps/{app_id}/menus", tags=["menus"])


@router.get("", response_model=List[MenuConfigRead])
def list_menus(
    app_id: int,
    session: Session = Depends(get_session)
):
    """List all menu items for an app"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    statement = select(MenuConfig).where(MenuConfig.app_id == app_id).order_by(MenuConfig.order)
    menus = session.exec(statement).all()
    return menus


@router.post("", response_model=MenuConfigRead, status_code=201)
def create_menu(
    app_id: int,
    menu: MenuConfigCreate,
    session: Session = Depends(get_session)
):
    """Create a new menu item"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    db_menu = MenuConfig(**menu.model_dump(), app_id=app_id)
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu


@router.get("/{menu_id}", response_model=MenuConfigRead)
def get_menu(
    app_id: int,
    menu_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific menu item"""
    menu = session.get(MenuConfig, menu_id)
    if not menu or menu.app_id != app_id:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu


@router.patch("/{menu_id}", response_model=MenuConfigRead)
def update_menu(
    app_id: int,
    menu_id: int,
    menu_update: MenuConfigUpdate,
    session: Session = Depends(get_session)
):
    """Update a menu item"""
    menu = session.get(MenuConfig, menu_id)
    if not menu or menu.app_id != app_id:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    update_data = menu_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(menu, key, value)
    
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu


@router.delete("/{menu_id}", status_code=204)
def delete_menu(
    app_id: int,
    menu_id: int,
    session: Session = Depends(get_session)
):
    """Delete a menu item"""
    menu = session.get(MenuConfig, menu_id)
    if not menu or menu.app_id != app_id:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    session.delete(menu)
    session.commit()
    return None


@router.get("/tree", response_model=List[dict])
def get_menu_tree(
    app_id: int,
    session: Session = Depends(get_session)
):
    """Get hierarchical menu tree structure"""
    app = session.get(App, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    statement = select(MenuConfig).where(MenuConfig.app_id == app_id).order_by(MenuConfig.order)
    all_menus = session.exec(statement).all()
    
    # Build tree structure
    menu_dict = {menu.id: {**menu.model_dump(), "children": []} for menu in all_menus}
    root_menus = []
    
    for menu in all_menus:
        if menu.parent_id and menu.parent_id in menu_dict:
            menu_dict[menu.parent_id]["children"].append(menu_dict[menu.id])
        else:
            root_menus.append(menu_dict[menu.id])
    
    return root_menus
