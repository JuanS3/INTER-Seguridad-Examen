# Examen Práctico: Evaluación de Seguridad para Sistema de Gestión de Casos Legales

Bufete Jurídico Internacional S.A. (BJI) ha implementado recientemente una nueva plataforma digital para la gestión de casos legales. Esta plataforma almacena información altamente sensible relacionada con casos jurídicos confidenciales, datos de clientes y estrategias legales.

Conscientes de la importancia de la seguridad informática, BJI ha decidido realizar una evaluación independiente de la robustez de su plataforma antes de cargar todos sus datos históricos. Para ello, ha contratado a su equipo como consultores externos especializados en seguridad informática.

## Objetivo del examen

Realizar una evaluación de seguridad del sistema de gestión de casos jurídicos de BJI, con énfasis en la identificación y explotación de vulnerabilidades de inyección SQL que podrían comprometer la confidencialidad, integridad o disponibilidad de la información almacenada.

## Infraestructura disponible

Para este examen, se le proporcionará acceso a una versión de prueba de la plataforma, desplegada en un entorno aislado que replica las características del sistema en producción. La aplicación ha sido desarrollada utilizando FastAPI como framework backend y una base de datos SQL para el almacenamiento de la información.

### Actividades a realizar

1. **Reconocimiento inicial**: Identificar los componentes de la aplicación y puntos de entrada, especialmente aquellos que puedan ser vulnerables a inyecciones SQL.

2. **Exploración de vulnerabilidades de inyección SQL**: Utilizar técnicas de inyección SQL para:
   * Eludir el sistema de autenticación y obtener acceso no autorizado
   * Extraer información de la base de datos subyacente
   * Identificar tablas y columnas relevantes

3. **Explotación del sistema**: Una vez conseguido el acceso mediante inyección SQL, explorar la estructura de la base de datos para:
   * Localizar el endpoint específico que contiene la información de usuarios
   * Extraer la lista completa de usuarios y contraseñas almacenadas en el sistema

4. **Documentación**: Preparar un informe detallado que incluya:
   * Las vulnerabilidades de inyección SQL identificadas
   * Las consultas SQL específicas utilizadas para la explotación
   * Los pasos seguidos para localizar y extraer las credenciales de usuario
   * Recomendaciones específicas para mitigar estas vulnerabilidades

### Consideraciones importantes

* El éxito en este examen depende de su capacidad para identificar y explotar correctamente vulnerabilidades de inyección SQL.
* Es necesario documentar meticulosamente cada consulta SQL utilizada y su propósito.
* Se evaluará tanto el éxito en la obtención de las credenciales como la metodología empleada.
* El informe final debe incluir capturas de pantalla que demuestren el acceso exitoso y la extracción de la información de usuarios.

## Entregables

* Informe técnico detallando las vulnerabilidades de inyección SQL encontradas, metodología de explotación y evidencias.
* Colección de consultas SQL utilizadas para la explotación (debidamente comentadas).
* Archivo con las credenciales extraídas (usuario y contraseña) de todos los usuarios del sistema.

## Criterios de evaluación

Su trabajo será evaluado considerando:

* **Efectividad**: Capacidad para explotar exitosamente las vulnerabilidades de inyección SQL.
* **Metodología**: Enfoque sistemático durante el proceso de explotación.
* **Exhaustividad**: Capacidad para extraer la información completa de usuarios y contraseñas.
* **Análisis de impacto**: Valoración realista de las consecuencias potenciales de estas vulnerabilidades.
* **Claridad del informe**: Capacidad para comunicar eficazmente los hallazgos técnicos y las técnicas utilizadas.

## Consejos adicionales

* Considere explorar diferentes tipos de inyecciones SQL (unión, error-based, blind, etc.).
* Preste atención a cómo están almacenadas las contraseñas (texto plano, hash, etc.).
* Intente determinar si existen usuarios con diferentes niveles de privilegio.

## Recursos técnicos adicionales

### Configuración del entorno de pruebas

Para comenzar con el examen, deberá configurar el entorno de pruebas siguiendo estos pasos:

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/JuanS3/INTER-Seguridad-Examen.git
   cd INTER-Seguridad-Examen
   ```

2. **Crear un entorno virtual de Python**:

   ```bash
   python -m venv venv

   # En Windows
   nv\Scripts\activate

   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar las dependencias necesarias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Iniciar la aplicación**:

   ```bash
   python app.py
   ```

5. **Acceder a la aplicación**:

   Una vez iniciada, la aplicación estará disponible en <http://127.0.0.1:8000>

Asegúrese de mantener la aplicación en ejecución durante toda la evaluación. La base de datos ya viene preconfigurada con datos de prueba que simulan un entorno de producción.
