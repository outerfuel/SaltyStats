# start by pulling the python image
FROM python:slim-bullseye

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

COPY ./SaltyStats /app

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

CMD [ "/bin/sh", "./entrypoint.sh" ]