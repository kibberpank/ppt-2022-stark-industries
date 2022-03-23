FROM python: 3.9

RUN mkdir /ppt-task-0
WORKDIR /ppt-task-0
COPY . . 
EXPOSE 80/udp

ENV host=127.0.0.1
ENV port=80

CMD [ "python", "/ppt-task-0/main.py"]
