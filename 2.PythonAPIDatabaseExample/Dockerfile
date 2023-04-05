# This example can be run with:
# docker build -t apiapp .
# docker run -d -p 5000:5000 --rm --env-file .env -v "C:\Docker+Kubernetes\Docker-Kubernetes\2.PythonAPIDatabaseExample:/app" --name apiapp apiapp:latest

# use miniconda for env
FROM continuumio/miniconda3

# set virtual root dir
WORKDIR /app
COPY environment.yml /app
RUN conda env create -f /app/environment.yml
# to run commands inside env
SHELL ["conda", "run", "-n", "DummyEnv", "/bin/bash", "-c"]

# test if dependencies imported
RUN echo "Make sure dependencies worked:"
RUN python -c 'import flask'

# to optimize, copy everything else after the env (so if code changed, just use cached env)
COPY . /app

# expose a port
EXPOSE ${PORT}

# save txts in anonymous volumes
# VOLUME [ "/app/DummyPythonApp/data" ]

# code to run when container starts, flag to get stdout and stderr (CMD or ENTRYPOINT)
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "DummyEnv", "python", "api.py"]