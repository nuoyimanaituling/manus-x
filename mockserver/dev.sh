#!/bin/bash

# Start uvicorn server with hot reload
exec uvicorn main:app --host 0.0.0.0 --port 8090 --reload 