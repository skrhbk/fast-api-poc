poetry init
poetry config virtualenvs.in-project true
poetry env use python
poetry shell


poetry add uvicorn fastapi fastapi-versioning pydantic pydantic-mongo pymongo python-multipart passlib[bcrypt] python-jose[cryptography]
poetry show
poetry show --tree


poetry install