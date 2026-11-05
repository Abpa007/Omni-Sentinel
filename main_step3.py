import uvicorn

if __name__ == "__main__":
    print("🚀 [Step 3] Starting Omni-Sentinel FastAPI & WebSocket Telemetry Gateway...")
    print("📡 Endpoints available at: http://127.0.0.1:8000")
    print("🔌 WebSocket stream active at: ws://127.0.0.1:8000/ws/telemetry")
    
    uvicorn.run("engine.streaming_engine:app", host="127.0.0.1", port=8000, reload=True)