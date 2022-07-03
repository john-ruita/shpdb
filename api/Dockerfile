FROM osgeo/gdal:ubuntu-small-latest as dev

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["manage.py", "run", "-h", "0.0.0.0"]