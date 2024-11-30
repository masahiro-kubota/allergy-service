allergy service

```
$ xdg-open frontend/index.html
```
```
$ uv sync
$ . .venv/bin/activate
$ gunicorn backend.app:app --log-level debug
```

need to change remote address in index.html to local host