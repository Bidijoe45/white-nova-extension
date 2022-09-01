# Extensión white nova

Se ha creado esta pequeña extensión de navegador para que los estudiantes de 42 Madrid puedan consultar su estado y el de otros estudiantes desde la comodidad de la intranet.

Consiste en una interfaz integrada a la página de perfil que contiene toda la información relevante a un click de distancia, con una estética afín al resto de la intra.

<img width="643" alt="imagen" src="https://user-images.githubusercontent.com/10995165/186650112-31ef14bd-c76a-4d1b-b2ed-6fb1e9ca2774.png">
<img width="640" alt="imagen" src="https://user-images.githubusercontent.com/10995165/186650160-3c5351ad-df19-476b-bc78-d4fca91e4a6d.png">


### Instalación

- **Chrome:** se puede descargar de la [store de chrome](https://chrome.google.com/webstore/detail/intra42nova/fnehnflgpiaemngoknikolkcgcigabhc)
- **Firefox:** se puede descargar de las releases de github [aquí](https://github.com/Bidijoe45/white-nova-extension/releases/latest/download/intra42whitenova-firefox.xpi)

### Por qué se ha creado la extensión
Para calcular si se cumplen los requistos de Whitenova hay que hacer una serie de llamadas a la API de 42 que son muy costosas en cuanto a tiempo de respuesta.

Para solucionar este problema se ha implementado una base de datos que es alimentada por un proceso "sincronizador" que se encarga de hacer llamadas a la API de 42 periódicamente.

Al guardar todos estos datos las consultas y los cálculos son instantáneos.

### Qué información se guarda

Los datos generados se guardan en una base de datos. Se guardan tu ID de usuario, tu login, y la fecha en la que un usuario con extensión te buscó por última vez. Si no quieres que se guarden tus datos contacta a @apavel en Slack.

Estos datos se extraen de la API de 42.

### Contribuciones

Este repositorio se ha creado con una continua evolución en mente. Cualquier persona que quiera contribuir o proponer nuevas ideas es más que bienvenida. Podéis crear una pull request o contactar con nosotros a través de Slack.

### Colaboradores

[@alvrodri](https://github.com/alvrodri)
[@apavel](https://github.com/Bidijoe45)
[@mmartin-](https://github.com/Mariomm-marti)
[@npinto-g](https://github.com/bororama)
[@ycarro](https://github.com/m00nbyt3)


___🔥 made with ❤ for students by students___
