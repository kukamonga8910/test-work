FROM ubuntu:22.04
RUN apt update && apt install python3 python3-pip -y
RUN pip3 install flask
RUN pip3 install requests 
COPY mail-test.py /home/
EXPOSE 5555/tcp
CMD ["python3", "/home/mail-test.py"]
