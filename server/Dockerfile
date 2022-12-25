FROM python:3.10

WORKDIR /src/app

RUN python3 -m venv venv

RUN . venv/bin/activate

COPY . .

RUN find . -type d -name __pycache__ -exec rm -r {} \+

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]