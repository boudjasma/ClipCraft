FROM python:3.8   

ENV DockerHOME=/opt/clipcraftapp  

RUN mkdir -p $DockerHOME  && \
    python3 -m venv /opt/clipcraftapi/venv

WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN pip install --upgrade pip  

COPY . $DockerHOME  

RUN pip install -r requirements.txt  

EXPOSE 8000  
 
CMD python manage.py runserver  