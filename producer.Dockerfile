FROM continuumio/miniconda3

ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml
# Pull the environment name out of the environment.yml
ENV ACTIVE_ENV $(head -1 /tmp/environment.yml | cut -d' ' -f2)
RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH
ENV EVENT_HUB_SAS_POLICY ""
ENV EVENT_HUB_SAS_KEY ""
ENV EVENT_HUB_ADDRESS ""

ADD ./producer /code
WORKDIR /code
ENTRYPOINT [ "/bin/bash", "-c" ]
CMD [ "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2) && exec python eventhub_producer.py"]
