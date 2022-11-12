FROM python:3.10

# copy source code to image
COPY . /app
WORKDIR /app

# install system dependencies for the project
RUN pip install pipenv

# install from Pipfile
RUN pipenv install
RUN mkdir logs

RUN wget https://chromedriver.storage.googleapis.com/108.0.5359.22/chromedriver_linux64.zip && \
    unzip unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver

#CMD ["pipenv", "run", "python", "main.py"]
