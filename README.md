# entregable-1-cicd

Primer entregable del curso de CI/CD: introducción a Git, GitHub y la automatización con GitHub Actions.

## Integrantes

**Texto de nombres usado en `AUTOR` y en el saludo del workflow:** `José Miguel Blanco Vélez`

| Nombre completo | Usuario de GitHub | Rol |
|---|---|---|
| José Miguel Blanco Vélez | [drase-lab](https://github.com/drase-lab) | Propietario del repositorio |

Modalidad: individual.

## Contenido del repositorio

- [`.github/workflows/mi_workflow.yml`](.github/workflows/mi_workflow.yml): workflow de GitHub Actions que imprime un saludo personalizado y la fecha/hora del runner, configura Python 3.13 y ejecuta el script.
- [`mi_script.py`](mi_script.py): script de Python que imprime el autor, el sistema operativo del runner y la fecha/hora.

## Ejecución exitosa del workflow

Enlace a una ejecución exitosa de `mi_workflow.yml` (job `imprimir_info`), con el autor correcto en los logs:

👉 https://github.com/drase-lab/entregable-1-cicd/actions/runs/42415990663

Salida obtenida en los logs:

```
Hola, soy José Miguel Blanco Vélez y este es mi primer workflow!
La fecha y hora actual es: Sat Nov  7 21:28:11 UTC 2026
Autor: José Miguel Blanco Vélez
Sistema Operativo: Linux 7.0.0-1019-azure
Fecha y hora desde Python: 2026-11-07 21:28:11.667288
```

También se probó la ejecución manual con **Run workflow** (evento `workflow_dispatch`) sobre la rama `main`.

## Respuestas a las preguntas

### 1. ¿Qué eventos configuraste para disparar tu workflow y por qué?

Configuré dos eventos:

- **`push` a la rama `main`**: el workflow se ejecuta automáticamente cada vez que subo cambios a la rama principal. Así verifico de inmediato que el código integrado en `main` sigue funcionando, que es la idea central de la integración continua. Lo limité a `main` con `branches` para no ejecutar el workflow en cada rama de trabajo.
- **`workflow_dispatch`**: permite ejecutar el workflow manualmente desde la pestaña Actions (botón *Run workflow*), sin tener que hacer un commit. Es útil para volver a probarlo, depurarlo o ejecutarlo bajo demanda.

### 2. ¿Qué sistema operativo utiliza el runner `ubuntu-latest` y por qué puede ejecutar tu workflow aunque tu computadora sea Windows o macOS? ¿Qué relación tiene el runner con el shell de los pasos `run`?

`ubuntu-latest` es una máquina virtual con **Ubuntu Linux** (la versión LTS más reciente que GitHub tenga marcada como `latest`), alojada y administrada por GitHub. En los logs, el script de Python lo confirma: `Sistema Operativo: Linux`.

Funciona aunque mi computadora sea Windows o macOS porque el workflow **no se ejecuta en mi computadora**: al hacer `push`, GitHub crea una máquina virtual nueva en sus servidores, clona el repositorio en ella y ejecuta ahí todos los pasos. Mi equipo solo sirve para editar el código y subir los cambios.

El runner determina el **shell por defecto** de los pasos `run`: en Ubuntu y macOS es **Bash**, y en Windows es **PowerShell**. Por eso un comando como `$(date)` funciona en Bash pero no necesariamente en PowerShell. En este workflow fijé `shell: bash` en el paso del saludo para dejarlo explícito. Además, `$(date)` devuelve la fecha y hora del runner (en UTC), no la hora local de mi computadora.

### 3. Tres acciones del Marketplace de GitHub Actions (no mencionadas en el material)

1. **`actions/cache`**: guarda en caché dependencias o archivos generados (por ejemplo `~/.cache/pip` o `node_modules`) entre ejecuciones, usando una clave como el hash de `requirements.txt`. Sirve para acelerar los workflows, porque evita descargar e instalar todo desde cero en cada ejecución.
2. **`docker/build-push-action`**: construye una imagen de Docker a partir de un `Dockerfile` y puede publicarla en un registro (Docker Hub, GitHub Container Registry, etc.). Sirve para empaquetar una aplicación como contenedor y prepararla para desplegarla.
3. **`codecov/codecov-action`**: sube los reportes de cobertura de las pruebas a Codecov. Sirve para medir qué porcentaje del código cubren las pruebas y ver cómo cambia esa cobertura en cada commit o Pull Request.
4. *(Extra)* **`actions/setup-node`**: instala una versión específica de Node.js en el runner, y opcionalmente cachea las dependencias de npm/yarn/pnpm. Sirve para compilar y probar proyectos de JavaScript/TypeScript.

### 4. ¿Qué es un secreto en GitHub Actions y para qué se usa? ¿Cómo lo usarías en tu workflow?

Un **secreto** es un valor sensible (un token de API, una contraseña, una clave de acceso a la nube) que se guarda cifrado en la configuración del repositorio, organización o entorno, **fuera del código**. Se usa para que el workflow pueda autenticarse con servicios externos sin escribir esas credenciales en el YAML ni en el código, que en un repositorio público cualquiera podría ver. GitHub intenta ocultar sus valores en los logs (los reemplaza por `***`), pero no se deben imprimir.

Para usarlo en mi workflow:

1. Crearía el secreto en **Settings > Secrets and variables > Actions > New repository secret**, por ejemplo `API_TOKEN`.
2. Lo pasaría al paso que lo necesita como variable de entorno:

```yaml
      - name: Ejecutar script Python
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
        run: python mi_script.py
```

3. En el script lo leería con `os.environ["API_TOKEN"]`, sin imprimirlo nunca.

Este entregable no necesita secretos, pero los usaría, por ejemplo, para publicar una imagen en Docker Hub o desplegar a un servidor o servicio en la nube.

### 5. Reflexión: uso de GitHub Actions en mi flujo de trabajo diario

**José Miguel Blanco Vélez:** GitHub Actions me parece útil para quitarme tareas repetitivas en las que es fácil olvidar un paso. Automatizaría principalmente dos cosas:

- **Pruebas y revisión de estilo en cada `push` y Pull Request**: ejecutaría las pruebas automatizadas (por ejemplo con `pytest`) y un linter como `flake8` o `ruff`. Así detectaría los errores en el momento en que los introduzco, y no días después cuando ya cuesta más saber qué cambio los causó. Además, nadie podría integrar a `main` código que rompe las pruebas.
- **Tareas programadas con `schedule`**: por ejemplo, un workflow semanal que revise si hay dependencias desactualizadas o con vulnerabilidades, o que genere un reporte automáticamente. Son tareas que se olvidan si dependen de que alguien se acuerde, y con `cron` se ejecutan solas.

Más adelante también automatizaría el **despliegue**: cuando los cambios pasen las pruebas en `main`, construir la aplicación y publicarla en un entorno de pruebas. Primero lo haría con aprobación manual (entrega continua), y cuando el pipeline sea confiable, podría pasar a despliegue continuo.
