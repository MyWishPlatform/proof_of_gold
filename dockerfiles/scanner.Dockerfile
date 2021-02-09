FROM python:3.7.2

WORKDIR /code

ENV PYTHONUNBUFFERED=1

COPY scanner_requirements.txt /code/scanner_requirements.txt
RUN pip install -r scanner_requirements.txt

COPY . /code
CMD ["python", "scanner/networks/networks_scan_entrypoint.py"]

