# tp1-halabiski-gonzalez-boc-ho
## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install flask-cors
sudo apt install postgresql
pip install Flask-SQLAlchemy psycopg2
```

## Run

```bash
source venv/bin/activate
sudo systemctl start postgresql 
cd BACKEND/
flask run --debug
```
