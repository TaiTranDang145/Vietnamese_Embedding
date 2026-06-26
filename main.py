import uvicorn
from src.api.routes import app
from src.utils.helpers import load_config

def main():
    config = load_config()
    app_config = config.get("app", {})
    host = app_config.get("host", "127.0.0.1")
    port = app_config.get("port", 8080)
    debug = app_config.get("debug", False)
    
    print(f"Starting Vietnamese Embedding Service on {host}:{port} (debug={debug})...")
    uvicorn.run("src.api.routes:app", host=host, port=port, reload=debug)

if __name__ == "__main__":
    main()
