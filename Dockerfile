FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV USING_DOCKER 1


RUN apt-get update
RUN apt-get install -y libgraphviz-dev graphviz

# The next line enables to build NumberJack
RUN apt-get install -y python-dev-is-python3 swig libxml2-dev zlib1g-dev libgmp-dev

# Numberjack is very slow to install,
# It has its own Docker file, line so changes in other lines don't reinstall it.
RUN pip install Numberjack

# Install pm4py
# clone branch with BPMN implementation - it may require changes when branch is merged to master
RUN git clone https://github.com/pm4py/pm4py-source.git
WORKDIR /pm4py-source/
RUN pip install -r requirements.txt
RUN python setup.py build
RUN python setup.py install

# Install thesis dependencies
COPY ./src/requirements.txt /thesis/src/requirements.txt
WORKDIR /thesis/src
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy thesis source
COPY ./src /thesis

# Run processing problems
WORKDIR /thesis/
RUN python main.py
