# Basis for our Docker -> Linux Debian bullseye and Python 3.10
FROM python:3.10-slim-bullseye

#Loading of all modules listed in requirements.txt for later installation
COPY requirements.txt .

# Here other nessecary libraries will be installed, they are needed by some modules listed in the requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config && \
    apt-get clean
# Here the modules from the requirements will be installed 
RUN pip install --no-cache-dir -r requirements.txt

# Here the python source code and the parameters will be copied from the local building folder into the docker image
COPY src .
COPY params /params

# Here the commands will be listed which will be executed, when the docker starts -> "start Python", "execute main.py"
CMD [ "python", "./main.py" ]
