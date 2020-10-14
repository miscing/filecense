FROM python:latest

COPY ./filecense.py /home/

ENTRYPOINT [ "python", "/home/filecense.py" ]
