########## DEVELOPMENT ##########
FROM python:3.12-slim AS development
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; else pip install fastapi==0.111.0 uvicorn[standard]==0.30.1 sqlalchemy==2.0.0 "pydantic>=2.7,<3.0"; fi
COPY . .
## Sanitize any Python source files possibly copied with UTF-16/BOM
RUN python - <<'PY'
import pathlib
for path in pathlib.Path('.').rglob('*.py'):
	raw = path.read_bytes()
	changed = False
	if raw.startswith(b'\xef\xbb\xbf'):
		raw = raw[3:]; changed = True
	elif raw.startswith(b'\xff\xfe'):
		try:
			raw = raw[2:].decode('utf-16-le').encode('utf-8'); changed = True
		except Exception: pass
	elif raw.startswith(b'\xfe\xff'):
		try:
			raw = raw[2:].decode('utf-16-be').encode('utf-8'); changed = True
		except Exception: pass
	if b'\x00' in raw: # remove null bytes
		raw = raw.replace(b'\x00', b''); changed = True
	if changed:
		path.write_bytes(raw)
PY
EXPOSE 8000
CMD ["python","-m","app.start"]

# For staging
########## STAGING ##########
FROM python:3.12-slim AS staging
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY . .
RUN pip install fastapi==0.111.0 uvicorn[standard]==0.30.1 sqlalchemy==2.0.0 "pydantic>=2.7,<3.0"
EXPOSE 8000
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]

# For production
########## PRODUCTION ##########
FROM python:3.12-slim AS production
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY . .
RUN pip install fastapi==0.111.0 uvicorn[standard]==0.30.1 sqlalchemy==2.0.0 "pydantic>=2.7,<3.0"
EXPOSE 8000
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
