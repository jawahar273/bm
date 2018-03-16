FROM python:3
MKDIR requirement
COPY requirement/base.txt ./requirement
COPY requirement/local.txt ./requirement
COPY requirements.txt ./

RUN pip pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver"]