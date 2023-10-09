FROM ubuntu:22.04
RUN apt update && apt install python3 python3-pip -y; pip3 install flask; pip3 install requests 
COPY mail-test.py /home/
EXPOSE 5555/tcp
CMD ["python3", "/home/mail-test.py"]
