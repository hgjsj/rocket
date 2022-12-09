FROM python:3.7.6
RUN pip install kubernetes
COPY src/k8s_operator.py /opt/
WORKDIR /opt
ENTRYPOINT ["python", "k8s_operator.py"]