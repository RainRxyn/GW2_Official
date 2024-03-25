# Use an official Python runtime as a parent image
FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
# COPY migrations migrations
COPY controllers controllers
COPY iframe_figures iframe_figures
COPY model model
COPY view view
COPY static static
COPY expenses.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP expenses.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]