FROM python:3
RUN mkdir work/
COPY requirements.txt work/
WORKDIR /work/
RUN pip install -r requirements.txt
ADD . /work/
