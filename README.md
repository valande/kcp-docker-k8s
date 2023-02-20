<a name="main"></a>
# __Práctica Pablo Cazallas - Contenedores, más que VMs__

`contkube` es una aplicación web desarrollada en Python con las librerías `Flask` y `psycopg` y conectada a un backend con base de datos `Postgres`. 
Permite mantener un torneo de jugadores basado en puntos por victoria y empate, sin límite de participantes.

# Índice de contenidos

* [__Descripción__](#main)
* [__Funcionamiento__](#arch)
* [__Instalación y Configuración__](#setup)
* [__Instrucciones para ejecutar en entorno local__](#rc_local)
* [__Instrucciones para desplegar en Kubernetes__](./k8s/README.md)
* [__Instrucciones para desplegar con Helm__](./charts/README.md#main)


<a name="arch"></a>
# Funcionamiento

Para crear o actualizar el torneo, hazlo de la siguiente manera:

* `http(s)://<url>/add/<player>` añade el jugador <player> al torneo, con 0 puntos iniciales.
* `http(s)://<url>/drop/<player>` elimina al jugador <player> del torneo.
* `http(s)://<url>/win/<player>` +3 puntos para el jugador <player> (victoria).
* `http(s)://<url>/draw/<player>` +1 punto para el jugador <player> (empate).
* `http(s)://<url>/restart` reinicia las puntuaciones.
* `http(s)://<url>/reset` borra todos los datos (reinicia el sistema al completo).
* `http(s)://<url>` muestra la clasificación (por defecto).

Puedes visitar una url mediante navegador web, o usar `curl` para llamar a los endpoints.
```
curl http(s)://<url>/<action>/player
```


<a name="setup"></a>
# Instalación y Configuración

TODO



<a name="rc_local"></a>
# Instrucciones para ejecutar en entorno local

TODO



