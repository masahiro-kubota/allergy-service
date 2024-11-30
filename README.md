allergy service

```
$ xdg-open frontend/index.html
```
```
$ uv sync
$ . .venv/bin/activate
$ gunicorn backend.app:app --log-level debug
```

```
#.env
# end point of the backend
BASE_URL=xxxxxxxxxx
PYTHON_VERSION=3.12.7
```