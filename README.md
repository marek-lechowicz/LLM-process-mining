If you want to generate a BPMN/Petri Net diagram of a given problem
put the problem description files (.txt with matrices and .task_names) 
inside the src/probelms directory.
Repository contains problem examples inside sample_problems directory.

To generate the process description use the notebook:
gpt_process_generation.ipynb

NOTE: inside provide a valid OpenAI API key

To build project run in project dir:
$ docker build --tag=tpaszun/thesis:latest .

To run the containter and get container id:
docker run --rm -d -t papaszun/thesis bash

To copy solutions from the container
$ docker cp <containerId>:/thesis/solutions solutions

There is also an option to connect to docker container via VSCode, 
which allows direct operations inside the container - simmilar workflow
like in case of a local environment.