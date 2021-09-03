# PFE
# Documentation

first clone project https://github.com/ouadhi/DjangoGraphDB.git

## GraphDB
Download [GraphDB Free](https://www.ontotext.com/products/graphdb/graphdb-free/)
Create  repository with ID =3

import repository Data from BC1.4.rj

## Run in local machine 
in project graph-db  connection set base url to localhost 

install requirement.txt
```bash
pip install -r requirement.txt
```

to run server use :  
 ```bash
python manage.py runserver 0.0.0.0:8000
```

## Use Docker 

pull image from [dockerHub](https://hub.docker.com/repository/docker/ouadhi/pfe)
 ```bash
docker push ouadhi/pfe:tagname
```

run  image 
 ```bash
docker run   --name pfe -d -p 8000:8000 pfe:latest  
```
