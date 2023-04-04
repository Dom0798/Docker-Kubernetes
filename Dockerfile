# This example can be run with:
# docker build docker build -t pythonapp .
# docker run -d -p 5000:5000 --rm -v data_python:/app/DummyPythonApp/data -v "C:\Path\to\DummyPythonApp:/app/DummyPythonApp" --name papp pythonapp:latest

# use miniconda for env
FROM continuumio/miniconda3

# set virtual root dir
WORKDIR /app
COPY environment.yml /app
RUN conda env create -f /app/environment.yml
# to run commands inside env
SHELL ["conda", "run", "-n", "DummyEnv", "/bin/bash", "-c"]

# test if dependencies imported
#RUN pip install numpy
#RUN pip install pandas
RUN echo "Make sure dependencies worked:"
RUN python -c 'import flask'

# to optimize, copy everything else after the env (so if code changed, just use cached env)
COPY . /app
# set virtual working dir
WORKDIR /app/DummyPythonApp

# expose a port
EXPOSE 5000

# save txts in anonymous volumes
# VOLUME [ "/app/DummyPythonApp/data" ]

# code to run when container starts, flag to get stdout and stderr (CMD or ENTRYPOINT)
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "DummyEnv", "python", "api.py"]