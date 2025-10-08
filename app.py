from fastapi import FastAPI, Request, Form, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from chat.agent import get_chatbot_response
from db.query import (
    get_all_properties, get_property_by_id, search_properties, 
    add_property, update_property, delete_property
)
from web.maps_api import get_nearby_landmarks
from web.web_search import web_search
import json
import asyncio
from typing import List, Dict
import os

app = FastAPI(title="Real Estate AI Assistant", version="2.0")

# Mount static files
app.mount('/static', StaticFiles(directory='web'), name='static')

# Templates
templates = Jinja2Templates(directory="web")

# WebSocket connections for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove disconnected clients
                self.active_connections.remove(connection)

manager = ConnectionManager()

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    """Main homepage with property listings"""
    properties = get_all_properties()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "properties": properties,
        "total_properties": len(properties)
    })

@app.get('/property/{property_id}', response_class=HTMLResponse)
async def property_detail(request: Request, property_id: int):
    """Individual property detail page"""
    property_data = get_property_by_id(property_id)
    if not property_data:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Get nearby landmarks
    try:
        landmarks = get_nearby_landmarks(property_data['location'])
        property_data['landmarks'] = landmarks
    except:
        property_data['landmarks'] = []
    
    return templates.TemplateResponse("property_detail.html", {
        "request": request,
        "property": property_data
    })

@app.get('/chat', response_class=HTMLResponse)
async def chat_page(request: Request):
    """Chat interface page"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get('/admin', response_class=HTMLResponse)
async def admin_page(request: Request):
    """Admin panel for property management"""
    properties = get_all_properties()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "properties": properties
    })

# API Endpoints
@app.get('/api/properties')
async def get_properties():
    """Get all properties"""
    properties = get_all_properties()
    return JSONResponse({
        "success": True,
        "data": properties,
        "total": len(properties)
    })

@app.get('/api/properties/{property_id}')
async def get_property(property_id: int):
    """Get specific property by ID"""
    property_data = get_property_by_id(property_id)
    if not property_data:
        raise HTTPException(status_code=404, detail="Property not found")
    return JSONResponse({"success": True, "data": property_data})

@app.get('/api/properties/search/{query}')
async def search_properties_api(query: str):
    """Search properties"""
    properties = search_properties(query)
    return JSONResponse({
        "success": True,
        "data": properties,
        "query": query,
        "total": len(properties)
    })

@app.post('/api/properties')
async def create_property(request: Request):
    """Create new property"""
    try:
        data = await request.json()
        success = add_property(data)
        if success:
            # Broadcast update to all connected clients
            await manager.broadcast(json.dumps({
                "type": "property_added",
                "message": f"New property '{data['name']}' has been added"
            }))
            return JSONResponse({"success": True, "message": "Property added successfully"})
        else:
            raise HTTPException(status_code=400, detail="Failed to add property")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put('/api/properties/{property_id}')
async def update_property_api(property_id: int, request: Request):
    """Update existing property"""
    try:
        data = await request.json()
        success = update_property(property_id, data)
        if success:
            # Broadcast update to all connected clients
            await manager.broadcast(json.dumps({
                "type": "property_updated",
                "message": f"Property '{data['name']}' has been updated"
            }))
            return JSONResponse({"success": True, "message": "Property updated successfully"})
        else:
            raise HTTPException(status_code=400, detail="Failed to update property")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete('/api/properties/{property_id}')
async def delete_property_api(property_id: int):
    """Delete property"""
    success = delete_property(property_id)
    if success:
        # Broadcast update to all connected clients
        await manager.broadcast(json.dumps({
            "type": "property_deleted",
            "message": f"Property has been deleted"
        }))
        return JSONResponse({"success": True, "message": "Property deleted successfully"})
    else:
        raise HTTPException(status_code=400, detail="Failed to delete property")

@app.post('/api/chat')
async def chat_endpoint(request: Request):
    form = await request.form()
    message = form.get('message')
    property_id = form.get('property_id')
    # Only convert to int if property_id is a string of digits
    if isinstance(property_id, str) and property_id.isdigit():
        property_id = int(property_id)
    else:
        property_id = None
    response = get_chatbot_response(str(message), property_id=property_id)
    return JSONResponse({'success': True, 'response': response, 'user_message': message})

@app.get('/api/market-info/{location}')
async def get_market_info(location: str):
    """Get market information for a location"""
    try:
        market_info = web_search.search_property_market_info(location)
        return JSONResponse({
            "success": True,
            "data": market_info
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        })

@app.get('/api/amenities/{location}')
async def get_amenities(location: str):
    """Get nearby amenities for a location"""
    try:
        amenities_info = web_search.search_nearby_amenities(location)
        return JSONResponse({
            "success": True,
            "data": amenities_info
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        })

@app.get('/api/news')
async def get_news():
    """Get latest real estate news"""
    try:
        news_info = web_search.search_property_news()
        return JSONResponse({
            "success": True,
            "data": news_info
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        })

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 