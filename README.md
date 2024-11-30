allergy service

need to change remote address in frontend/scripts/app.js to local host
```
# frontend
$ cd frontend
$ python3 -m http.server 5000
```

```
# backend
$ uv sync
$ . .venv/bin/activate
$ gunicorn backend.app:app --workers 4 --log-level debug --bind 127.0.0.1:8000
```

