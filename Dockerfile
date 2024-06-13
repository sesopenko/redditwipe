FROM python:3.10

# run this before copying requirements for cache efficiency
RUN pip install --upgrade pip
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py ./

CMD [ "python", "./main.py" ]