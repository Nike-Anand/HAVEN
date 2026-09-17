"""Run the HAVEN API locally.

Usage:
    python run.py            # starts uvicorn on http://127.0.0.1:8000
    python run.py --port 9000
"""
import argparse
import uvicorn

import app.db as db

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run HAVEN API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    db.init_db()
    print(f"HAVEN API starting on http://{args.host}:{args.port}  (docs: /docs)")
    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)