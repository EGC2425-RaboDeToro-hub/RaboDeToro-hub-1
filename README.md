<div align="center">
  <img src="https://github.com/user-attachments/assets/2780ac75-1f64-48db-b317-0b2e3006e1d5" alt="image" width="600"/>
</div>

## 🌍 **Language/Idioma**

**English** | **Español**  
--- | ---  
[English](#rabo-de-toro---english) | [Español](#rabo-de-toro---spanish)


# 🔗 Rabo De toro- Spanish
## 💡Sobre Nosotros

Aplicación de modelos formato UVL integrada con fakenodo y flamapy siguiendo los Principios de Ciencia Abierta, que permite a los usuarios acceder a conjuntos de datos publicos con buscadores de alta calidad y con comunidades para poder buscar los datos del tipo que mas le interesen<br> - Desarrollado por EGC2425-RaboDeToro-Hub-1.

## 👥 Miembros del proyecto

| Miembros |
| ------------- |
| [Mesa Pérez, Virginia](https://github.com/virmesper)|
| [Moreno Moguel, Juan Antonio](https://github.com/JuanAntonioMorenoMoguel)|
| [Morgado Prudencio, Jose María](https://github.com/josemorgado)|
| [Reyes Apresa, Mario](https://github.com/marioreyesapresa)|
| [Sanchez Gómez, Paula](https://github.com/paulasanchezg)|
| [Suarez Linares, Paula María](https://github.com/pausualin)|

## 🏁 Objetivos del proyecto

A lo largo de este proyecto se han realizado diversas integraciones a la aplicacion que le aportan mayor valor y mayor usabilidad y accesibilidad, ademas, se han desarrollado tecnicas y procesos que facilitan la agregacion de cambios al proyecto y a la gestion del mismo.

Algunas de las nuevas integraciones son los "Work Items":

### WI realizados:

- **Improve Search:** <span style="color:yellow;">(Medium)</span> Consiste en añadir nuevos filtros a la sección de explore en uvlhub. Los filtros añadidos han sido de rango de fecha y de tamaño de datasets. 



- **View user profile:** <span style="color:red;">(Low)</span>Este WorkItem nos permite visualizar los datasets subidos por un usuario al pinchar sobre su nombre. Esto permite una mayor navegabilidad sobre la página.


- **Remember my password:** <span style="color:red;">(Low)</span> Permite a los usuarios recuperar y cambiar su contraseña en caso de que la hayan olvidado a través de un correo electrónico que se envia.


- **Download All Datasets:** <span style="color:yellow;">(Medium)</span> Nos permite descargar todos los datasets con todos los modelos y en todos los formatos al pulsar un botón.


- **Advanced filtering:** <span style="color:green;">(High)</span> ESte es un filtro avanzado que nos permite filtrar por número de características y número de productos para obtener datasets deacuerdo a mis necesidades.


- **Create Communities:** <span style="color:green;">(High)</span> Permite crear una comunidad que dara mejor accesibilidad a los usuarios que esten dentro de la comunidad, permitiendoles acceder rapidamente a los datasets de los otros usuarios de la comunidad.


- **Fakenodo:** Redirigimos las llamadas a zenodo a fakenodo para evitar sobresaturar la red.


## 💻 Tecnologias usadas:
- **Lenguaje**:Python(Flask)
- **Frontend**: HTML, CSS, JavaScript
- **Base de datos**: MySQL/MariaDB
- **Automatización y CI/CD**: Github Actions, Render
- **Pruebas Automatizadas**: Selenium, Pytest
- **Virtualización**: Docker,Vagrant

## 🚀Instalación:
Sigue estos pasos para configurar el proyecto después de clonar el repositorio:

**1. Clona el repositorio**
```
git clone https://github.com/EGC2425-RaboDeToro-hub/RaboDeToro-hub-1.git
cd RaboDeToro-hub-1
```
**2. Ejecuta el script de instalación**

Usa el script proporcionado para configurar el entorno, la base de datos y las dependencias:

```
chmod +x setup.sh
./setup.sh
```

## 🧪 Pruebas:

Para ejecutar las pruebas en el proyecto ejecuta el siguiente comando:

**Usando rosemary**

```
rosemary test //para pruebas unitarias y de integración
rosemary selenium //para pruebas de interfaz
```

**Usando pytest**

```
pytest app/modules
```

### Cambios realizados
- **Script de construccion:** A partir de ahora podra preparar todo el entorno del proyecto con un simple comando: ./setup.sh. Este script se encargara de realizar todo lo que usted podria deberia de haber hecho siguiendo el manual de instalacion

- **Gestion de logs y sesiones flask:** Para evitar la inclusion en el codigo de logs indeseados se ha modificado el codigo para que estos sean eliminados cada vez que se arranca el proyecto, ademas de excluirlos del repositorio, lo mismo se ha realizado con las sesiones flask

- **Arreglo de lint:** Se han arreglado todos los errores de lint que aparecian al usar flake8

## 🌐 Enlace de despliegue del proyecto:
- **Render:**  [ https://rabodetoro-hub-1.onrender.com](https://rabodetoro-hub-1.onrender.com)

## 📖 Wiki del proyecto

 - **Wiki:** [https://github.com/EGC2425-RaboDeToro-hub/RaboDeToro-hub-1/wiki](https://github.com/EGC2425-RaboDeToro-hub/RaboDeToro-hub-1/wiki)







# 🔗 Rabo De toro- English
## 💡 About Us
UVL format models application integrated with fakenodo and flamapy following Open Science Principles, allowing users to access public datasets with high-quality search engines and communities to search for the type of data they are most interested in - Developed by EGC2425-RaboDeToro-Hub-1.

## 👥 Project Members

| Members |
| ------------- |
| [Mesa Pérez, Virginia](https://github.com/virmesper)|
| [Moreno Moguel, Juan Antonio](https://github.com/JuanAntonioMorenoMoguel)|
| [Morgado Prudencio, Jose María](https://github.com/josemorgado)|
| [Reyes Apresa, Mario](https://github.com/marioreyesapresa)|
| [Sanchez Gómez, Paula](https://github.com/paulasanchezg)|
| [Suarez Linares, Paula María](https://github.com/pausualin)|

## 🏁 Project Goals

Throughout this project, various integrations have been made to the application that provide greater value, usability, and accessibility. Additionally, techniques and processes have been developed to facilitate the addition of changes to the project and its management.

Some of the new integrations are the "Work Items":

### Completed Work Items:

- **Improve Search:** <span style="color:yellow;">(Medium)</span> Adding new filters to the "Explore" section in uvlhub. The added filters include date range and dataset size.

- **View user profile:** <span style="color:red;">(Low)</span> This WorkItem allows us to visualize the datasets uploaded by a user by clicking on their name. This improves the site's navigation.

- **Remember my password:** <span style="color:red;">(Low)</span> Allows users to recover and change their password in case they have forgotten it through an email that is sent to them.

- **Download All Datasets:** <span style="color:yellow;">(Medium)</span> Allows us to download all datasets with all models and in all formats at the click of a button.

- **Advanced filtering:** <span style="color:green;">(High)</span> This is an advanced filter that lets us filter by the number of features and number of products to obtain datasets according to our needs.

- **Create Communities:** <span style="color:green;">(High)</span> Allows creating a community that provides better accessibility to users within the community, enabling them to quickly access datasets from other users in the community.

- **Fakenodo:** Redirecting Zenodo calls to Fakenodo to avoid network overload.

## 💻 Technologies Used:
- **Language**:Python(Flask)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL/MariaDB
- **Automation and CI/CD**: Github Actions, Render
- **Automated Testing**: Selenium, Pytest
- **Virtualization**: Docker,Vagrant

## Installation:
Follow these steps to set up the project after cloning the repository:

**1. Clone the repository**
```
git clone https://github.com/EGC2425-RaboDeToro-hub/RaboDeToro-hub-1.git
cd RaboDeToro-hub-1
```
**2. Run the setup script**

Use the provided script to configure the environment, database, and dependencies:

```
chmod +x setup.sh
./setup.sh
```
## 🧪 Tests:

To run the tests in the project, execute the following command:

**Using rosemary**

```
rosemary test //para pruebas unitarias y de integración
rosemary selenium //para pruebas de interfaz
```

**Using pytest**

```
pytest app/modules
```

### Changes Made
- **Build Script:** From now on, you can prepare the entire project environment with a single command: ./setup.sh. This script will handle everything you would have done by following the installation manual.

- **Log and Flask Session Management:** To avoid the inclusion of unwanted logs in the code, the code has been modified to delete them every time the project starts, and they have been excluded from the repository. The same has been done with Flask sessions.

- **Lint Fixes:** All lint errors that appeared when using flake8 have been fixed.


## 🌐 Project Deployment Link:
- **Render:**  [ https://rabodetoro-hub-1.onrender.com](https://rabodetoro-hub-1.onrender.com)

## 📖 Project Wiki

 - **Wiki:** [https://github.com/EGC2425-RaboDeToro-hub/RaboDeToro-hub-1/wiki](https://github.com/EGC2425-RaboDeToro-hub/RaboDeToro-hub-1/wiki)


