FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code

ENTRYPOINT [ "bash", "entrypoint.sh" ]
CMD sleep 5 && python3 src/every_day_check.py