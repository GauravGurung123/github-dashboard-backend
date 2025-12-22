```bash

python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver

```