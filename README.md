<a name="main"></a>
# __Práctica Pablo Cazallas - Contenedores__

`contkube` es una demo de aplicación web, desarrollada en Python con las librerías `Flask` y `psycopg` y conectada a un backend con base de datos `Postgres`.  
Permite mantener un ranking de jugadores de un torneo basado en puntos, por victorias (+3) y empates (+1). 

<br>

# __Índice de contenidos__
* [__Descripción__](#main)
* [__Funcionamiento__](#arch)
* [__Instalación y Configuración__](#setup)
* [__Instrucciones para despliegue en entorno local__](#rc_local)
* [__Instrucciones para despliegue en Kubernetes__](./k8s/README.md)
* [__Instrucciones para desplegar con Helm__](./charts/README.md#main)

<br>

<a name="arch"></a>
# __Funcionamiento__
Todos los endpoints muestran la lista de clasificados, una vez han realizado la acción correspondiente.  
Puedes visitar las urls mediante navegador web, o puedes usar el comando `curl` para el mismo cometido.

```
 $ curl http://<url>/<action>/player
```

Para l agestión del torneo, se dispone los siguientes endpoints:

* `http://<url>/add/<player>` añade el jugador <player> al torneo, con 0 puntos iniciales.
* `http://<url>/drop/<player>` elimina al jugador <player> del torneo, si existe.
* `http://<url>/win/<player>` +3 puntos para el jugador <player> (victoria), si existe.
* `http://<url>/draw/<player>` +1 punto para el jugador <player> (empate), si existe.
* `http://<url>/restart` reinicia las puntuaciones.
* `http://<url>/reset` borra todos los datos (reinicia el sistema al completo).
* `http://<url>` muestra la clasificación (por defecto).

*`<url>`* puede referirse a una dirección IP o un nombre de dominio, y también podría incorporar una especificación de puerto.  
Esto dependerá del tipo de despliegue realizado y la configuración correspondiente al mismo.  
Algunos ejemplos:
```
 http://mi.sitio.com/add/julian
 http://mi.sitio.com:8080/win/julian
 http://192.168.192.168:5000/
 http://192.168.192.168/drop/lucas
 http://mi.sitio2.com/restart
```

<br>

<a name="setup"></a>
# __Instalación y Configuración__

## Utiliza imágenes ya disponibles (recomendado)
Puedes descargar y utilizar las imágenes ya creadas, disponibles en el [hub de docker](https://docs.docker.com/docker-hub/).  
Este paso no será necesario en caso de utilizar [docker compose](https://docs.docker.com/compose/) para el despliegue.
```
 $ docker pull valande/microservice
 $ docker pull valande/backend
```

<br>

## Construye tus propias imágenes
En el directorio `docker` puedes ver los [archivos utilizados](https://docs.docker.com/engine/reference/builder/) para crear las imágenes en las que se basa la aplicación.   
Puedes modificar estos archivos para personalizarlas a tu gusto y [construirlas](https://docs.docker.com/engine/reference/commandline/build/) en tu entorno local:

```
 $ cd /path/to/project
 $ docker build -t tag-microservice -f ./docker/microservice-dockerfile microservice
 $ docker build -t tag-backend -f ./docker/backend-dockerfile dbinit
```

* NOTA:   
  Si utilizas [docker compose](https://docs.docker.com/compose/) para el despliegue de la aplicación, necesitarás revisar el fichero `.env` y modificar los valores de los parámetros `APP_IMAGE` (microservicio) y `DB_IMAGE` (backend), para que hagan uso de las imágenes construídas.  

<br>

## Configuración y personalización
Para ejecutar la aplicación con una configuración personalizada, se recomienda editar cuidadosamente el fichero `.env`, ubicado en el directorio raíz del proyecto.  
Se trata de un fichero en el que se definen las diferentes variables de entorno utilizadas dentro de los contenedores docker:
```
 $ cat .env
 APP_IMAGE="valande/microservice"               # Imagen del microservicio
 APP_PORT=5000                                  # Puerto del microservicio interno a docker (interno)
 APP_TUNNEL_PORT=8000                           # Puerto externo a docker (acceso desde el host)
 FLASK_APP=valapp.py                            # Nombre de la aplicación Flask
 FLASK_DEBUG=true                               # Modo depuración true/false de la aplicación Flask
 FLASK_RUN_HOST=0.0.0.0                         # Direccionamiento IP con acceso permitido al microservicio
 DB_IMAGE="valande/backend"                     # Imagen del backend
 DB_SERVICE=svc-database                        # DNS del servicio de backend
 DB_PORT=5432                                   # Puerto del backend interno a docker (interno)
 DB_TUNNEL_PORT=7777                            # Puerto externo a docker (acceso desde el host)
 DB_NAME=flask_db                               # Nombre de la base de datos 
 DB_USERNAME=dbuser                             # Usuario de conexión a la base de datos
 DB_PASSWORD=dbpass                             # Password de conexión a la base de datos
 DB_PGDATA=/var/lib/postgresql/data/pgdata      # Directorio de datos de la base de datos
 DB_VOLUME_DIR=/var/lib/postgresql/data         # Volumen de docker para el contenedor del backend
```

* NOTAS:   
  Este fichero es consumido únicamente por docker compose.  
  Si realizas un despliegue manual, tendrás que modificar estos valores editando los ficheros Dockerfile descritos previamente en *Construye tus propias imágenes*.  
  Se recomienda encarecidamente modificar el valor del parámetro `DB_PASSWORD` en todos los casos.

<br>

<a name="rc_local"></a>
# __Instrucciones para despliegue en entorno local__

## Despliegue automático (recomendado)
Para desplegar la aplicación basta con ejecutar el siguiente comando en el directorio raíz:
```
 $ cd /path/to/project
 $ docker compose up -d
```

Si previamente deseas construir las imágenes, añade el flag `--build` al comando:
```
 $ docker compose up -d --build
```

El flag `-d` indica a docker compose que debe ejecutarse en segundo plano y no mostrar salida por consola de comandos.  
Cuando el comando `docker compose` termine, ya deberías poder acceder a la url `http://localhost:8000` de manera que se muestre la aplicación web.  

### *Troubleshooting*
Si la web no responde, ya sea mediante `curl` o por medio de un navegador web, probablemente hay algún problema con el despliegue:
* De configuración: 
    * Revisar los parámetros establecidos en el fichero *.env*.
* De imágenes: 
    * En el caso de haberse utilizado el flag `--build`, revisar los ficheros *Dockerfile*.
    * Revisar la lista de imágenes disponibles en local, con `docker image ls`.

<br>

## Despliegue manual e interactivo

* __IMPORTANTE: Se desaconseja desplegar la aplicación de esta manera, salvo depuración o testeo de la misma.__

Esta manera es la más propensa a cometer errores, además de ser la más costosa de realizar, teniendo que recordar muchos comandos y parámetros.  
Si aún así estás interesado, puedes arrancar contenedores completamente independientes y con una configuración personalizada haciendo uso de [docker run](https://docs.docker.com/engine/reference/run/).

```
 $ docker run --name backend -p 7777:5432 valande/backend
 $ docker run --name microservicio -p 8000:5000 valande/microservice 
```

<br>

[Volver arriba](#main)