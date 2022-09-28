FROM python:3.9.7
WORKDIR /project
COPY requirements.txt ./

#RUN apt-get update && apt-get install -y python3-opencv
#RUN apt-get install ffmpeg libsm6 libxext6  -y

#RUN pip3 install torch -i https://mirrors.aliyun.com/pypi/simple/


RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN pip3 uninstall opencv-python -y
RUN pip3 install opencv-python-headless -i https://mirrors.aliyun.com/pypi/simple/

COPY . .
CMD ["python", "server.py"]