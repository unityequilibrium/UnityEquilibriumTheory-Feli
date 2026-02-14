@echo off
cd /d %~dp0
docker-compose run --rm uet_kb uet_kb --db-url postgres://postgres:postgres@postgres:5432/uet_kb start-mcp-server
