# Guía Rápida de ExpertResizer

## 🚀 Inicio Rápido

### Opción 1: Usar el Ejecutable (.exe)
1. Ejecuta `dist\ExpertResizer.exe`
2. ¡Listo para usar! No necesitas Python instalado

### Opción 2: Ejecutar desde Python
1. Instala dependencias: `install.bat` o `pip install -r requirements.txt`
2. Ejecuta: `python main.py`

### Opción 3: Crear tu propio ejecutable
1. Ejecuta: `build.bat`
2. El .exe se creará en la carpeta `dist\`

---

## 📝 Pasos para Redimensionar Imágenes

### 1. Seleccionar Carpetas
- **Carpeta origen**: Donde están tus imágenes originales
- **Carpeta destino**: Donde se guardarán las imágenes procesadas
- Click en "Cargar Archivos"

### 2. Configurar Opciones
```
Dimensiones Máximas:
├── Ancho: 1920 px (ejemplo: para Full HD)
└── Alto: 1080 px

Método de Resize:
└── LANCZOS (recomendado para mejor calidad)

Calidad:
├── JPG: 85 (recomendado: 80-95)
├── WebP: 85 (recomendado: 80-90)
└── PNG: 6 (recomendado: 5-7)
```

### 3. Seleccionar Imágenes
- Todas vienen seleccionadas por defecto (☑)
- Click en la casilla para deseleccionar imágenes específicas
- Usa botones "Seleccionar Todos" / "Deseleccionar Todos"

### 4. Procesar
- Click en "PROCESAR IMÁGENES"
- Observa el progreso en la barra y el log
- ¡Listo! Las imágenes están en la carpeta destino

---

## 💡 Casos de Uso Comunes

### Para Web (Optimización máxima)
```
Ancho: 1920 px
Alto: 1080 px
Método: LANCZOS
JPG: 80
WebP: 85
```

### Para Impresión (Alta calidad)
```
Ancho: 4000 px
Alto: 3000 px
Método: LANCZOS
JPG: 95
PNG: 9
```

### Para Redes Sociales
```
Instagram Post: 1080x1080 px
Instagram Story: 1080x1920 px
Facebook: 1200x630 px
Método: LANCZOS
JPG: 85
```

### Para Email (Archivos pequeños)
```
Ancho: 800 px
Alto: 600 px
Método: BICUBIC
JPG: 75
```

---

## 🎯 Consejos y Trucos

### Métodos de Resize
- **LANCZOS**: Fotografías de alta calidad → Mejor resultado
- **BICUBIC**: Balance calidad/velocidad → Uso general
- **NEAREST**: Pixel art, capturas de pantalla → Mantiene bordes nítidos

### Calidad vs Tamaño
| Calidad JPG | Uso Recomendado | Reducción Aprox. |
|-------------|-----------------|------------------|
| 95-100      | Impresión       | 10-20%           |
| 85-95       | Web profesional | 30-50%           |
| 75-85       | Web general     | 50-70%           |
| 60-75       | Email           | 70-85%           |

### PNG Compresión
- **0-3**: Rápido, archivos más grandes
- **6**: Balance perfecto (recomendado)
- **9**: Archivos más pequeños, más lento

---

## ⚠️ Notas Importantes

### Proporciones
- El resize SIEMPRE mantiene la proporción original
- Si la imagen ya es más pequeña que el máximo, no se modifica
- Se ajusta al límite más restrictivo (ancho o alto)

### Ejemplo de Resize Proporcional
```
Imagen original: 3000x2000 px
Límites: 1920x1080 px

Cálculo:
- Ratio ancho: 1920/3000 = 0.64
- Ratio alto: 1080/2000 = 0.54
- Se usa el menor: 0.54

Resultado: 1620x1080 px (proporcional)
```

### Formatos
- **JPG**: No soporta transparencia (se convierte a RGB)
- **PNG**: Soporta transparencia, archivos más grandes
- **WebP**: Formato moderno, excelente compresión

---

## 🐛 Solución de Problemas

### La aplicación no inicia
```bash
# Reinstala las dependencias
pip install --upgrade -r requirements.txt
```

### Error "No module named PIL"
```bash
pip install --upgrade Pillow
```

### El .exe no se crea
```bash
pip install --upgrade pyinstaller
# Luego ejecuta build.bat nuevamente
```

### Error con WebP
WebP está soportado en Pillow 10.1+. Actualiza:
```bash
pip install --upgrade Pillow
```

---

## 📊 Tabla de Referencia Rápida

| Formato | Transparencia | Compresión | Mejor Para |
|---------|--------------|------------|------------|
| JPG     | ❌           | Con pérdida | Fotografías |
| PNG     | ✅           | Sin pérdida | Gráficos, logos |
| WebP    | ✅           | Con pérdida | Web moderna |

---

## 🎓 Workflow Recomendado

1. **Backup**: Siempre guarda las originales
2. **Test**: Prueba con 2-3 imágenes primero
3. **Ajusta**: Modifica calidad según resultado
4. **Proceso**: Ejecuta el batch completo
5. **Verifica**: Revisa las imágenes de salida

---

¿Necesitas ayuda? Revisa el README.md completo para más detalles.
