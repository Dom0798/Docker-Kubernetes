# use miniconda for env
FROM continuumio/miniconda3

# set virtual root dir
COPY . /app
RUN conda env create -f /app/environment.yml
# to run commands inside env
SHELL ["conda", "run", "-n", "DummyEnv", "/bin/bash", "-c"]

# test if dependencies imported
#RUN pip install numpy
#RUN pip install pandas
RUN echo "Make sure dependencies worked:"
RUN python -c 'import flask'

# set virtual working dir
WORKDIR /app/DummyPythonApp

# expose a port
EXPOSE 5000

# code to run when container starts, flag to get stdout and stderr (CMD or ENTRYPOINT)
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "DummyEnv", "python", "api.py"]