# import the fastapi image with python version 3.12
FROM python:3.12-alpine

RUN addgroup api_user
RUN adduser -D -h /api_user -u 1000 -G api_user api_user

RUN apk update

WORKDIR /api_user/code

# copy the necessary files to the docker
COPY main.py /api_user/code/main.py
COPY pytest.ini /api_user/code/pytest.ini
COPY ./requirements.txt /api_user/code/requirements.txt
COPY ./db /api_user/code/db
COPY ./run.sh /api_user/code/run.sh

RUN chown -R api_user:api_user /api_user

USER api_user

RUN pip install --upgrade pip
# install the necessary python package
RUN pip install --no-cache-dir --upgrade -r /api_user/code/requirements.txt

ENV PATH="/api_user/.local/bin/:${PATH}"

# run the server
CMD ["./run.sh"]
