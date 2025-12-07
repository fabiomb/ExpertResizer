# ExpertResizer - Redimensionador Profesional de Imágenes

Herramienta profesional para redimensionar imágenes en lote manteniendo proporciones y optimizando calidad.

![ExpertResizer](https://github.com/fabiomb/ExpertResizer/blob/main/docs/resizer.png)

## 🚀 Características

- ✅ **Selección de carpetas**: Origen y destino separados para no sobreescribir originales
- ✅ **Lista de archivos**: Visualiza dimensiones y tamaño de cada imagen
- ✅ **Selección múltiple**: Elige qué archivos procesar
- ✅ **Redimensionamiento proporcional**: Ajusta automáticamente ancho/alto manteniendo la proporción
- ✅ **Múltiples algoritmos**: LANCZOS, BICUBIC, BILINEAR, NEAREST, BOX, HAMMING
- ✅ **Formatos soportados**: JPG, PNG, WebP
- ✅ **Control de calidad**: Ajusta compresión para cada formato
- ✅ **Proceso batch**: Procesa múltiples imágenes automáticamente
- ✅ **Log detallado**: Seguimiento completo del proceso

## 📋 Requisitos

- Python 3.8 o superior
- Windows (probado en Windows 10/11)

## 🔧 Instalación para Desarrollo

1. Clona o descarga este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:

```bash
python main.py
```

## 📦 Crear Ejecutable Standalone

Para generar el archivo `.exe` independiente:

```bash
build.bat
```

El ejecutable se generará en la carpeta `dist\ExpertResizer.exe` y podrá ejecutarse sin necesidad de tener Python instalado.

## 📖 Uso

1. **Selecciona la carpeta origen**: Carpeta que contiene las imágenes a procesar
2. **Selecciona la carpeta destino**: Donde se guardarán las imágenes procesadas
3. **Carga los archivos**: Click en "Cargar Archivos" para listar las imágenes
4. **Configura opciones**:
   - Ancho/Alto máximo en píxeles
   - Método de redimensionamiento (LANCZOS recomendado para mejor calidad)
   - Calidad para JPG y WebP (1-100)
   - Compresión para PNG (0-9)
5. **Selecciona imágenes**: Click en el checkbox o usa los botones de selección
6. **Procesa**: Click en "PROCESAR IMÁGENES"

## 🎨 Métodos de Redimensionamiento

- **LANCZOS**: Mejor calidad, recomendado para fotografías
- **BICUBIC**: Alta calidad, buen balance calidad/velocidad
- **BILINEAR**: Calidad media, más rápido
- **NEAREST**: Más rápido, menor calidad (para pixelart)
- **BOX**: Optimizado para reducir tamaño
- **HAMMING**: Balance entre velocidad y calidad

## 💾 Formatos y Compresión

### JPG/JPEG
- **Calidad**: 1-100 (recomendado: 85-95)
- Optimización automática activada

### PNG
- **Compresión**: 0-9 (0=sin compresión, 9=máxima compresión)
- Recomendado: 6 (buen balance)

### WebP
- **Calidad**: 1-100 (recomendado: 80-90)
- Formato moderno con excelente compresión

## 🔍 Características Técnicas

- Procesamiento en thread separado (no bloquea la interfaz)
- Preservación de proporciones automática
- Conversión de modos de color automática (RGBA -> RGB para JPG)
- Manejo de errores robusto
- Barra de progreso y log detallado

## 📁 Estructura del Proyecto

```
ExpertResizer/
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias Python
├── build.bat           # Script para generar .exe
└── README.md           # Este archivo
```

## 🐛 Resolución de Problemas

**Error al cargar WebP**: Asegúrate de tener Pillow actualizado:
```bash
pip install --upgrade Pillow
```

**El .exe no se genera**: Verifica que PyInstaller esté instalado:
```bash
pip install --upgrade pyinstaller
```

## 📄 Licencia

Este proyecto está disponible para uso personal y comercial.

## 👨‍💻 Autor

Expert Image Tools - 2025

---

¿Preguntas o sugerencias? Abre un issue en el repositorio.
