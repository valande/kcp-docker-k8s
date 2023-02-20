<a name="main"></a>
# __Instrucciones para desplegar en Kubernetes__
## TO DO:

* Describe los recursos creados y documenta lo que sea configurable

  Microservicio (Deployment + Service)
  Backend (StatefulSet + Service + Headless)
  Configuración de microservicio (ConfigMap)
  Configuración de backend (ConfigMap)



* Incluye instrucciones de despliegue en kubernetes y cómo probar
  la aplicación y el correcto funcionamiento


  minikube tunnel

  
  kubectl create secret generic secrets --from-env-file secrets.txt
  kubectl create configmap config --from-env-file config.txt


  kubectl apply -f .

  kubectl logs database-0
  kubectl logs microsvc-...


  Abrir navegador y visitar <ip>:<port>
  kubectl describe svc -o wide

  ...

# Índice de contenidos

* [__Descripción__](../README.md#main)
* [__Funcionamiento__](../README.md#arch)
* [__Instalación y Configuración__](../README.md#setup)
* [__Instrucciones para despliegue en entorno local__](../README.md#rc_local)
* [__Instrucciones para despliegue en Kubernetes__](#main)
* [__Instrucciones para desplegar con Helm__](../charts/README.md#main)
