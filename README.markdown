# Guía de Instalación y Ejecución del Proyecto

**Universidad Valle del Momboy**  
**Estudiantes:** Zeuddy Segovia, Endelkys Matos  
**Asignatura:** Lenguaje y Compiladores  
**Profesora:** Katiuska Morillo  

Esta guía explica cómo configurar el entorno para ejecutar el proyecto utilizando ANTLR 4.9.2 en Ubuntu.

## Descripción
ANTLR (ANother Tool for Language Recognition) es un generador de analizadores léxicos y sintácticos. Permite traducir gramáticas a código ejecutable (en Python, Java, etc.). Este proyecto utiliza ANTLR v4.9.2 con Python3.

## Requisitos Previos
- Sistema operativo Ubuntu (20.04 o superior recomendado).
- Acceso a terminal y permisos de administrador (`sudo`).

## Instalación en Ubuntu

### 1. Instalar Java JDK
ANTLR requiere Java para su ejecución:

sudo apt update
sudo apt install default-jdk

## Instalar Python3 y pip 
sudo apt install python3 python3-pip

##  Instalar ANTLR 4.9.2 
Descargar el archivo JAR y configurar el entorno:

curl -O https://www.antlr.org/download/antlr-4.9.2-complete.jar
sudo mv antlr-4.9.2-complete.jar /usr/local/lib/

Agregar al archivo .bashrc (o .zshrc si usas Zsh):

echo 'export CLASSPATH=".:/usr/local/lib/antlr-4.9.2-complete.jar:$CLASSPATH"' >> ~/.bashrc
echo 'alias antlr4="java -jar /usr/local/lib/antlr-4.9.2-complete.jar"' >> ~/.bashrc
source ~/.bashrc

## Configurar Entorno Virtual

Se recomienda trabajar en un etorno virtual 

python3 -m venv venv
source venv/bin/activate 

### Instalar el runtime de ANTLR para Python:

pip install antlr4-python3-runtime==4.9.2 


## Ejecutar el Proyecto
Generar el parser a partir de la gramática Anny.g

antlr4 -Dlanguage=Python3 -listener Anny.g

Ejecutar el transpilador con un archivo de entrada:
python3 main.py example.anny 


## Windows

## Pasos Requeridos

1. **Instalar Java JDK 8+**  
   Descargar desde [Oracle](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).  
   Ejecutar el instalador y seguir los pasos (usar ubicación predeterminada).  
   ![Paso 1](images/primera.png)

---

2. **Descargar ANTLR 4.9.2**  
   Obtener `antlr-4.9.2-complete.jar` desde [ANTLR.org](http://www.antlr.org/download.html).  
   Guardar en `C:\Javalib`.  
   ![Paso 2](images/segunda.png)

---

3. **Configurar Variables de Entorno**  
   - Ir a **Panel de Control > Cuentas de Usuario > Variables de entorno**.  
   - Agregar al `PATH`:  
     ```
     C:\Javalib\antlr-4.9.2-complete.jar  
     C:\Program Files\Java\jdk1.8.0_121\bin
     ```  
   ![Paso 3](./images/Primera.png)  
   ![Paso 4](./images/segunda.png)

---

4. **Crear Comandos ANTLR**  
   En `C:\Windows\System32`, crear:  
   - **antlr4.bat**:  
    
     java -jar C:\Javalib\antlr-4.9.2-complete.jar %*
     ```  
   - **grun.bat**:  

     java org.antlr.v4.gui.TestRig %*
     ```  
   ![Paso 5](./images/quinta.png)

---

5. **Probar Instalación**  
   antlr4   # Debe mostrar "ANTLR Parser Generator 4.9.2"
   grun     # Debe mostrar opciones de TestRig

6. **Generar Parser y Ejecutar Proyecto**
antlr4 -Dlanguage=Python3 -listener Anny.g  
python main.py ejemplo.anny