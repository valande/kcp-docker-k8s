<a name="main"></a>

# __Instrucciones para desplegar en Kubernetes__

En esta sección se detallan los recursos utilizados para ejecutar la aplicación en la plataforma [Kubernetes](https://kubernetes.io/), así como las instrucciones para hacerlos funcionar de la manera correcta.  
Existen diferentes entornos posibles para correr Kubernetes, entre los cuales están [minikube](https://minikube.sigs.k8s.io/docs/start/) y [GKE](https://cloud.google.com/kubernetes-engine?hl=es), ambos utilizados para la demostración.


<br>

## __Recursos k8s__

El directorio `k8s` del proyecto contiene los diferentes recursos utilizados para desplegar la aplicación web en el entorno de contenedores descrito:
```
  k8s
  ├── config
  │   ├── app-config.yml
  │   ├── db-config.yml
  │   └── private.yml
  ├── deploys
  │   └── app.yml
  ├── hpa
  │   └── app-hpa.yml
  ├── network
  │   ├── http-ingress.yml
  │   └── nginx-controller.yml.txt
  ├── README.md
  ├── services
  │   ├── app-svc.yml
  │   ├── db-svc.yml
  │   └── headless-db-svc.yml
  └── sts
      └── db.yml
```

* config: Ficheros de configuración y datos sensibles como credenciales.
* deploys: Manifiesto para el deployment de la aplicación.
* hpa: Manifiesto para el autoescalado automático de pods.
* network: Manifiesto del Ingress junto a documento con el manifiesto de un ingress-controller.   
  Este último no se tendrá en cuenta para el despliegue, salvo que sea renombrado como fichero .yml o .yaml.
* services: Manifiestos para los servicios necesarios asociados al despliegue.
* sts: Manifiesto del statefulset utilizado para el backend.

Para modificar la configuración por defecto y adaptarla a tus necesidades, puedes editar los ficheros que están ubicados en el directorio config.  
* app-config.yml: Parámetros de configuración del microservicio.
* db-config.yml: Parámetros de configuración del backend
* private.yml: Datos de conexión con la base de datos del backend.  

Tanto el fichero `app-config.yml` como el `db-config.yml` establecen parámetros de configuración en texto claro, cuyos valores pueden ser modificados libremente, a partir de la sección `data:` de los mismos.  
Es altamente recomendable modificar las credenciales establecidas por defecto para la conexión a la base de datos, almacenadas en el fichero `private.yml`:

1. Crear un fichero de texto `connect.txt` con el siguiente contenido, indicando el usuario y contraseña que desees.  
   Revisa y comprueba que no hay espacios extra a la derecha de las definiciones, y no modifiques el nombre de las variables, solamente el valor de las mismas. El nombre de fichero utilizado es indiferente. 
```
 $ cat connect-data.txt
 POSTGRES_USER=usuario_conn
 POSTGRES_PASSWORD=password_conn
```
2. En el directorio `./k8s`, cambiando `SECRET_NAME` por el nombre que se desee dar al objeto en Kubernetes, ejecutar:
```
 $ cd ./k8s
 $ kubectl create secret generic SECRET_NAME --from-env-file=./connect-data.txt
 $ kubectl get secret -o yaml > ./config/private.yml
```

Como alternativa a lo anterior, puedes editar el fichero `private.yml` directamente, aunque se recomienda utilizar la manera descrita previamente.  
Para ello, tienes que especificar los datos de conexión en formato `base64`:
```
 $ echo "usuario_conn" | base64
 dXN1YXJpb19jb25uCg==
 $ echo "password_conn" | base64
 cGFzc3dvcmRfY29ubgo=
```
En este ejemplo, los token generados `dXN1YXJpb19jb25uCg==` y `cGFzc3dvcmRfY29ubgo=` son los valores que se deben indicar en el fichero `private.yml` modificado.

<br>

## __Desplegar en clúster de Minikube__

* Arrancar minikube y habilitar los plugins necesarios:
```
 $ minikube start
 $ minikube addons enable ingress
 $ minikube addons enable metrics-server
```

* Desplegar los componentes de la aplicación:
```
 $ cd /path/to/k8s
 $ kubectl apply -f config -f sts -f deploys -f services -f network -f hpa
```

* Cambia al namespace `practica`, done se generan todos los recursos de k8s.
```
 $ kubectl ns practica
```

* En otra terminal aparte, ejecutar (En Linux se pedirá la contraseña del usuario para obtener privilegios de administrador):
```
 $ minikube tunnel
```

* Obtener la dirección IP del servicio expuesto mediante el Ingress:
```
 $ kubectl get ingress http-ingress
```

* Añadir la siguiente entrada al fichero `/etc/hosts` de tu máquina, sustituyendo la dirección IP por la obtenida en el paso anterior:
```
  10.125.14.33  service.valande.io
```

* Visita la url que has añadido al fichero `/etc/hosts` con un navegador web o haz una petición con `curl` para comprobar el correcto funcionamiento.
```  
 $ curl http://service.valande.io
```

<br>

## Desplegar en un clúster GKE (Google Kubernetes Engine)

* Crear un clúster GKE mediante la consola de Google Cloud.
* Conectarse al clúster GKE

* Crear el namespace `practica` y situarse en el mismo.
```
 $ kubectl create ns practica
 $ kubectl ns practica
```

* Renombrar el fichero `ingres-controller.yml.txt` como `ingress-controller.yml`.

* Desplegar los componentes de la aplicación.
```
 $ cd /path/to/k8s
 $ kubectl apply -f config -f sts -f deploys -f services -f network -f hpa
```

* Obtener la dirección IP del servicio expuesto mediante el Ingress.  
  Puede consultarse en la sección de GKE `Ingress y servicios`, y es la correspondiente al servicio `ingress-nginx-controller`.

* Añadir la siguiente entrada al fichero `/etc/hosts` de tu máquina, sustituyendo la dirección IP por la obtenida en el paso anterior:
```
  13.45.82.24  service.valande.io
```

* Visita la url que has añadido al fichero `/etc/hosts` con un navegador web o haz una petición con `curl` para comprobar el correcto funcionamiento.
```  
 $ curl http://service.valande.io
```

<br>

### Índice

* [__Descripción__](../README.md#main)
* [__Funcionamiento__](../README.md#arch)
* [__Instalación y Configuración__](../README.md#setup)
* [__Instrucciones para despliegue en entorno local__](../README.md#rc_local)
* [__Instrucciones para despliegue en Kubernetes__](#main)
* [__Instrucciones para desplegar con Helm__](../charts/README.md#main)

<br>

[Volver arriba](#main)
