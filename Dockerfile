FROM python:latest

COPY ./filecense.py /bin/filecense

ENTRYPOINT [ filecense ]
