FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV USING_DOCKER 1


RUN apt-get update
RUN apt-get install -y libgraphviz-dev graphviz

# The next line enables to build NumberJack
RUN apt-get install -y python-dev swig libxml2-dev zlib1g-dev libgmp-dev

# Numberjack is very slow to install,
# It has its own Docker file, line so changes in other lines don't reinstall it.
RUN pip install Numberjack

# Install pm4py
RUN git clone --single-branch --branch bpmnIntegration2 --depth 1 https://github.com/pm4py/pm4py-source.git
WORKDIR /pm4py-source/
RUN pip install -r requirements_stable.txt
RUN python setup.py build
RUN python setup.py install

# Install thesis dependencies
COPY ./src/requirements.txt /thesis/src/requirements.txt
WORKDIR /thesis/src
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy thesis source
COPY ./src /thesis

# Test pm4py installation
# WORKDIR /thesis/tests/
# RUN python pm4py_test.py
# RUN python pm4py_bpmn_example.py

# Run processing problems
WORKDIR /thesis/
RUN python main.py
