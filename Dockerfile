FROM alpine:latest

# dependencies
RUN apk add python3

WORKDIR /home/filecense
# TODO copy and install files in fist
# COPY . .

# switch to a empty directory in which to license files
RUN mkdir /project
WORKDIR /project
ENTRYPOINT [ "python3", "/home/filecense/filecense.py", "-f" , "-v" ]
