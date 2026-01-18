# Notas - Editor de Texto GTK4

Editor de texto minimalista escrito en Python usando GTK4 nativo (PyGObject). Diseñado para tomar notas rápidas con características esenciales y arquitectura modular.

## Requisitos

- Python 3.10 o superior
- GTK 4 + PyGObject. En Arch Linux:

```bash
sudo pacman -S python-gobject gtk4 libadwaita
```

En Debian/Ubuntu:
```bash
sudo apt install python3-gi gir1.2-gtk-4.0 libadwaita-1-0
```

## Ejecución

Desde el código fuente:
```bash
python3 notas.py
```

O instalar el paquete:
```bash
sudo pacman -U notas-*.pkg.tar.zst
notas
```

## Funcionalidad

- Crear, abrir, editar y guardar archivos de texto plano
- Deshacer/Rehacer (Ctrl+Z / Ctrl+Y)
- Buscar texto dentro del documento (Ctrl+F)
- Corrección ortográfica integrada
- Vista previa básica de Markdown
- Drag & drop mejorado (múltiples archivos, URIs)
- Autosave automático con notificaciones
- Tema oscuro/claro (F11)
- Exportar a HTML
- Estadísticas de palabras/caracteres
- Números de línea opcionales
- Lista de archivos recientes
- Argumentos de línea de comandos (`notas archivo.txt`)
- Notificaciones del sistema discretas
- Zoom del texto (Ctrl+/-, Ctrl+0 para reset)
- Modo distraction-free (F10)

Minimalista y eficiente, con buena integración nativa.

## Desarrollo

### Arquitectura
- **Modular**: Separación clara entre core (lógica), ui (interfaz) y main (orquestación)
- **Event-driven**: Comunicación desacoplada mediante GObject signals
- **MVC-like**: Model (FileManager/TextProcessor), View (UI components), Controller (NotasApp)
- **Simplificado**: Sin wrappers innecesarios, ejecución directa del script principal

### Estructura del Proyecto
```
src/
├── core/           # Lógica de negocio
│   ├── file_manager.py
│   └── text_processor.py
├── ui/             # Componentes de interfaz
│   ├── main_window.py
│   ├── status_bar.py
│   └── file_dialogs.py
└── notas.py        # Aplicación principal
```

### Mantenimiento del Repositorio

Para mantener el repositorio limpio:

```bash
# Limpiar archivos temporales y cache
./clean.sh

# O manualmente
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
rm -rf pkg/
rm -f *.pkg.tar.zst
```

### Build y Package

```bash
# Construir paquete
makepkg -f

# Instalar
sudo pacman -U notas-*.pkg.tar.zst
```

## Funcionalidades

### Core
- Editor de texto con fuente monospace
- Abrir/guardar archivos con diálogos nativos
- Drag & drop de archivos y texto
- Barra de estado con estadísticas

### Avanzadas
- **Menús completos**: Archivo, Editar, Ver
- **Terminal integration**: Ejecutar comandos desde la app
- **Modo oscuro**: Toggle con persistencia
- **Markdown preview**: Vista previa básica
- **Notificaciones complejas**: GNotification para comandos terminados
- **GSettings**: Configuraciones persistentes

### 🚀 **Funcionalidades Únicas y Diferenciadoras**

#### **Context-Aware Notes** 🧠
- **Detección automática de contexto**: La app analiza la hora del día, aplicaciones activas y sugiere tipos de notas apropiadas
- **Sugerencias inteligentes**: Basado en el momento del día (mañana = TODO, tarde = reuniones)
- **Notas contextuales**: Templates automáticos según el contexto detectado

#### **Quick Capture System** ⚡
- **Captura instantánea**: `Ctrl+Shift+N` para crear notas al vuelo sin abrir la app completa
- **Templates inteligentes**: 7 templates predefinidos (reuniones, proyectos, investigación, ideas, bugs, TODO)
- **Context-aware templates**: La app sugiere templates basados en qué estás haciendo
- **Flujo de trabajo fluido**: De idea a nota estructurada en segundos



#### **Deep Linux Integration** 🐧
- **File system awareness**: Notas organizadas automáticamente en `~/Notas`
- **Terminal-first workflow**: Comandos que generan notas automáticamente
- **D-Bus integration**: Comunicación con otras aplicaciones del sistema
- **Desktop-native**: Funciona perfectamente en entornos GTK sin dependencias web
- **File system awareness**: Directorio `~/Notas` automático

### Atajos de Teclado
- `Ctrl+O`: Abrir archivo
- `Ctrl+S`: Guardar archivo
- `Ctrl+Shift+N`: Captura rápida (desde cualquier ventana)
- `Ctrl+F`: Buscar (futuro)



### Quick Capture Templates
- **Reunión**: Notas estructuradas para reuniones
- **Proyecto**: Planificación de proyectos
- **Investigación**: Notas de investigación con fuentes
- **Idea**: Captura rápida de ideas
- **Bug**: Reportes de bugs estructurados
- **TODO**: Listas de tareas
- **Código**: Revisiones de código

## Guía de Uso

### Primeros Pasos
```bash
# Instalar
sudo pacman -U notas-*.pkg.tar.zst

# Ejecutar
notas
```

### Flujo de Trabajo Recomendado
1. **Captura rápida**: Usa `Ctrl+Shift+N` para ideas instantáneas
2. **Organiza con templates**: Menú Editar → Captura Rápida
3. **Visualiza datos**: Menú Ver → Vista de Datos para overview
4. **Gestiona tareas**: Crea notas con formato `- [ ] tarea` y `- [x] completada`

### Ejemplos Prácticos

**Para tareas diarias:**
```
# TODO - Lunes
- [ ] Revisar emails
- [x] Reunión con equipo
- [ ] Preparar presentación
```

**Para proyectos:**
```
# Proyecto X
**Objective:** Desarrollar nueva funcionalidad
**Scope:** Módulos A, B, C
**Timeline:** 2 semanas
**Status:** En progreso
```

## Licencia

MIT
# writearch
