FROM python:3.8-slim

WORKDIR /app

COPY . /app

# if server is connected to internet, it should be uncommented
# RUN pip install -r requirements.txt

# if server is deployed in China Mainland, it should be uncommented
RUN pip install --index-url https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5004"]