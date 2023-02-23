<a name="main"></a>

# __Instrucciones para desplegar con Helm__
Para desplegar la aplicación con la ayuda de Helm se han definido una serie de plantillas, a partir de los recursos de k8s existentes, así como un fichero `values.yaml` con los parámetros que configurables de la misma para los despliegues.  

```
  charts/
  ├── contkube
  │   ├── charts
  │   ├── Chart.yaml
  │   ├── templates
  │   │   ├── app-config.yml
  │   │   ├── app-hpa.yml
  │   │   ├── app-svc.yml
  │   │   ├── app.yml
  │   │   ├── db-config.yml
  │   │   ├── db-svc.yml
  │   │   ├── db.yml
  │   │   ├── headless-db-svc.yml
  │   │   ├── _helpers.tpl
  │   │   ├── ingress.yml
  │   │   ├── NOTES.txt
  │   │   └── private.yml
  │   └── values.yaml
  └── README.md
```

Es requisito necesario disponer de un clúster de Kubernetes, ya sea con minikube, en GKE, o de alguna otra manera que se desee.  
Para instalar la aplicación con Helm basta con ejecutar lo siguiente en línea de comandos, desde el directorio `charts` del proyecto:

```
 $ helm install mi_release contkube
```

<br>

## __NOTA para instalación en un clúster GKE__
Si se desea exponer la aplicación al exterior, se debe copiar previamente el fichero `nginx-controller.yml` al directorio `templates` del chart.

<br>

## __values.yaml__
Todos aquellos parámetros definidos en el fichero `values.yaml` son, hasta cierto punto, configurables, siempre que con ellos se establezca una configuración razonable de la aplicación y sus componentes. Por defecto están todos habilitados.  
A continuación se detallan algunos de ellos:

```
namespace: practica
...

images.microservice: valande/microservice
images.database: valande/backend
replicaCount: 3
...

volumeMount.enabled: true
volumeMount.path: /var/lib/postgresql/data
volumeMount.size: 4Gi
...

```

Para modificar esta configuración por defecto existen dos maneras de hacerlo:

* Mediante un fichero adicional `my-values.yaml`, en el que estarán definidos los valores deseados a sobreescribir respecto a la configuración por defecto.
```
 $ helm install RELEASE_NAME contkube -f /path/to/my-values.yaml 
```

* Mediante flags `--set` indicando las propiedades a modificar. Ejemplo:
```
 $ helm install RELEASE_NAME contkube --set replicaCount=3,volumeMount.enabled=false
```

<br>

### __Ejemplos__
Solamente es necesaria una de las dos opciones mostradas en cada caso de ejemplo.

* Deshabilitar ingress:
```
 $ helm install RELEASE_NAME contkube --set ingress.enabled=false
```
```
 $ cat my-values.yaml
 ...
 ingress:
  enabled: false
 ...
```

* Exponer aplicación o la base de datos, mediante LoadBalancer:
```
 $ helm install RELEASE_NAME contkube --set service.[microservice|database].type=LoadBalancer, 
```
```
 $ cat my-values.yaml
 ...
 service:
  microservice:
    type: LoadBalancer
  database:
    type: ClusterIP
 ...
```

* Cambiar el `namespace`:
```
 $ helm install RELEASE_NAME contkube --set namespace=otrovalor
```
```
 $ cat my-values.yaml
 ...
 namespace: otrovalor
 ...
```

* Modificar el número mínimo de réplicas del autoescalado:
```
 $ helm install RELEASE_NAME contkube --set autoscaling.minReplicas=2
```
```
 $ cat my-values.yaml
 ...
 autoscaling:
  ...

  minReplicas: 2
 ...
```

<br>

### Índice

* [__Descripción__](../README.md#main)
* [__Funcionamiento__](../README.md#arch)
* [__Instalación y Configuración__](../README.md#setup)
* [__Instrucciones para despliegue en entorno local__](../README.md#rc_local)
* [__Instrucciones para despliegue en Kubernetes__](../k8s/README.md#main)
* [__Instrucciones para desplegar con Helm__](#main)

<br>

[Volver arriba](#main)