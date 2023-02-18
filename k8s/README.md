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