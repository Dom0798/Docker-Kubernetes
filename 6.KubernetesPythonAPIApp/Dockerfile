FROM continuumio/miniconda3

WORKDIR /app
COPY environment.yml /app
RUN conda env create -f /app/environment.yml
# to run commands inside env
SHELL ["conda", "run", "-n", "DummyEnv", "/bin/bash", "-c"]

RUN echo "Make sure dependencies worked:"
RUN python -c 'import flask'

# to optimize, copy everything else after the env (so if code changed, just use cached env)
COPY . /app

# expose a port
EXPOSE ${PORT}

# code to run when container starts, flag to get stdout and stderr (CMD or ENTRYPOINT)
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "DummyEnv", "python", "api.py"]