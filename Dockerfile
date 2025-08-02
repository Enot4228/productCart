FROM python:3.13
WORKDIR /usr/local/productCart

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY run.py ./
COPY initializeDb.py ./
COPY app ./app
COPY runApp.sh ./

EXPOSE 6080

CMD ["sh", "runApp.sh"]