FROM python:3.8   

ENV DockerHOME=/opt/clipcraftapp  

RUN mkdir -p $DockerHOME  && \
    python3 -m venv /opt/clipcraftapi/venv

WORKDIR $DockerHOME  

RUN pip install --upgrade pip  

COPY . $DockerHOME  

RUN pip install -r requirements.txt  

EXPOSE 8000  
 
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]