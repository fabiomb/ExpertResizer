"""
ExpertResizer - Herramienta profesional para redimensionar imágenes
Autor: Expert Image Tools
Versión: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageOps
import os
from pathlib import Path
from typing import List, Dict, Optional
import threading


class ImageInfo:
    """Clase para almacenar información de una imagen"""
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.selected = True
        
        try:
            with Image.open(filepath) as img:
                self.width, self.height = img.size
                self.format = img.format
                self.size_kb = os.path.getsize(filepath) / 1024
        except Exception as e:
            self.width = self.height = 0
            self.format = "ERROR"
            self.size_kb = 0
            print(f"Error loading {filepath}: {e}")


class ExpertResizerApp:
    """Aplicación principal de ExpertResizer"""
    
    # Métodos de resize disponibles
    RESIZE_METHODS = {
        "LANCZOS (Mejor calidad)": Image.Resampling.LANCZOS,
        "BICUBIC (Alta calidad)": Image.Resampling.BICUBIC,
        "BILINEAR (Calidad media)": Image.Resampling.BILINEAR,
        "NEAREST (Más rápido)": Image.Resampling.NEAREST,
        "BOX": Image.Resampling.BOX,
        "HAMMING": Image.Resampling.HAMMING
    }
    
    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.webp')
    
    def __init__(self, root):
        self.root = root
        self.root.title("ExpertResizer - Redimensionador de Imágenes")
        self.root.geometry("1200x800")
        
        # Variables
        self.source_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.max_width = tk.IntVar(value=1920)
        self.max_height = tk.IntVar(value=1080)
        self.quality_jpg = tk.IntVar(value=85)
        self.quality_webp = tk.IntVar(value=85)
        self.compression_png = tk.IntVar(value=6)
        self.resize_method = tk.StringVar(value="LANCZOS (Mejor calidad)")
        
        self.images_info: List[ImageInfo] = []
        self.processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # === SECCIÓN 1: Selección de carpetas ===
        folders_frame = ttk.LabelFrame(main_frame, text="Carpetas", padding="10")
        folders_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        folders_frame.columnconfigure(1, weight=1)
        
        # Carpeta origen
        ttk.Label(folders_frame, text="Carpeta origen:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(folders_frame, textvariable=self.source_folder, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(folders_frame, text="Seleccionar", command=self.select_source_folder).grid(row=0, column=2, padx=5)
        
        # Carpeta destino
        ttk.Label(folders_frame, text="Carpeta destino:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(folders_frame, textvariable=self.dest_folder, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(folders_frame, text="Seleccionar", command=self.select_dest_folder).grid(row=1, column=2, padx=5)
        
        ttk.Button(folders_frame, text="Cargar Archivos", command=self.load_images).grid(row=2, column=1, pady=10)
        
        # === SECCIÓN 2: Opciones de redimensionamiento ===
        options_frame = ttk.LabelFrame(main_frame, text="Opciones de Redimensionamiento", padding="10")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Frame izquierdo - Dimensiones
        left_options = ttk.Frame(options_frame)
        left_options.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        ttk.Label(left_options, text="Ancho máximo (px):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(left_options, from_=1, to=10000, textvariable=self.max_width, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(left_options, text="Alto máximo (px):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(left_options, from_=1, to=10000, textvariable=self.max_height, width=15).grid(row=1, column=1, padx=5)
        
        ttk.Label(left_options, text="Método de resize:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Combobox(left_options, textvariable=self.resize_method, 
                     values=list(self.RESIZE_METHODS.keys()), 
                     state='readonly', width=25).grid(row=2, column=1, padx=5)
        
        # Frame derecho - Calidad/Compresión
        right_options = ttk.Frame(options_frame)
        right_options.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        ttk.Label(right_options, text="Calidad JPG (1-100):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(right_options, from_=1, to=100, textvariable=self.quality_jpg, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(right_options, text="Calidad WebP (1-100):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(right_options, from_=1, to=100, textvariable=self.quality_webp, width=15).grid(row=1, column=1, padx=5)
        
        ttk.Label(right_options, text="Compresión PNG (0-9):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(right_options, from_=0, to=9, textvariable=self.compression_png, width=15).grid(row=2, column=1, padx=5)
        
        # === SECCIÓN 3: Lista de archivos ===
        files_frame = ttk.LabelFrame(main_frame, text="Archivos Encontrados", padding="10")
        files_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(0, weight=1)
        
        # Treeview con scrollbar
        tree_frame = ttk.Frame(files_frame)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                                  columns=("Archivo", "Ancho", "Alto", "Formato", "Tamaño KB"),
                                  show="tree headings",
                                  yscrollcommand=vsb.set,
                                  xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading("#0", text="✓")
        self.tree.heading("Archivo", text="Archivo")
        self.tree.heading("Ancho", text="Ancho")
        self.tree.heading("Alto", text="Alto")
        self.tree.heading("Formato", text="Formato")
        self.tree.heading("Tamaño KB", text="Tamaño (KB)")
        
        self.tree.column("#0", width=30, stretch=False)
        self.tree.column("Archivo", width=300)
        self.tree.column("Ancho", width=80, anchor=tk.CENTER)
        self.tree.column("Alto", width=80, anchor=tk.CENTER)
        self.tree.column("Formato", width=80, anchor=tk.CENTER)
        self.tree.column("Tamaño KB", width=100, anchor=tk.E)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind para selección/deselección
        self.tree.bind("<Button-1>", self.on_tree_click)
        
        # Botones de selección
        select_frame = ttk.Frame(files_frame)
        select_frame.grid(row=1, column=0, pady=5)
        ttk.Button(select_frame, text="Seleccionar Todos", command=self.select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(select_frame, text="Deseleccionar Todos", command=self.deselect_all).pack(side=tk.LEFT, padx=5)
        
        # === SECCIÓN 4: Log y procesamiento ===
        log_frame = ttk.LabelFrame(main_frame, text="Progreso", padding="10")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barra de progreso
        self.progress = ttk.Progressbar(log_frame, mode='determinate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Botón de procesar
        self.process_btn = ttk.Button(log_frame, text="PROCESAR IMÁGENES", 
                                       command=self.process_images,
                                       style='Accent.TButton')
        self.process_btn.grid(row=2, column=0, pady=5)
        
    def select_source_folder(self):
        """Selecciona la carpeta de origen"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta origen")
        if folder:
            self.source_folder.set(folder)
            self.log_message(f"Carpeta origen: {folder}")
            
    def select_dest_folder(self):
        """Selecciona la carpeta de destino"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta destino")
        if folder:
            self.dest_folder.set(folder)
            self.log_message(f"Carpeta destino: {folder}")
            
    def load_images(self):
        """Carga las imágenes de la carpeta origen"""
        source = self.source_folder.get()
        
        if not source or not os.path.exists(source):
            messagebox.showerror("Error", "Por favor selecciona una carpeta origen válida")
            return
            
        self.log_message("Cargando archivos...")
        self.images_info.clear()
        
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Buscar archivos
        for file in os.listdir(source):
            if file.lower().endswith(self.SUPPORTED_FORMATS):
                filepath = os.path.join(source, file)
                img_info = ImageInfo(filepath)
                self.images_info.append(img_info)
                
                # Agregar al tree
                self.tree.insert("", tk.END, 
                                text="☑",
                                values=(img_info.filename, 
                                       img_info.width, 
                                       img_info.height, 
                                       img_info.format,
                                       f"{img_info.size_kb:.2f}"),
                                tags=("checked",))
                                
        self.log_message(f"Se encontraron {len(self.images_info)} imágenes")
        
    def on_tree_click(self, event):
        """Maneja el click en el tree para seleccionar/deseleccionar"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "tree":
            item = self.tree.identify_row(event.y)
            if item:
                current_text = self.tree.item(item, "text")
                if current_text == "☑":
                    self.tree.item(item, text="☐")
                    idx = self.tree.index(item)
                    self.images_info[idx].selected = False
                else:
                    self.tree.item(item, text="☑")
                    idx = self.tree.index(item)
                    self.images_info[idx].selected = True
                    
    def select_all(self):
        """Selecciona todos los archivos"""
        for item in self.tree.get_children():
            self.tree.item(item, text="☑")
        for img in self.images_info:
            img.selected = True
            
    def deselect_all(self):
        """Deselecciona todos los archivos"""
        for item in self.tree.get_children():
            self.tree.item(item, text="☐")
        for img in self.images_info:
            img.selected = False
            
    def log_message(self, message: str):
        """Agrega un mensaje al log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
        
    def calculate_new_dimensions(self, width: int, height: int) -> tuple:
        """Calcula las nuevas dimensiones manteniendo la proporción"""
        max_w = self.max_width.get()
        max_h = self.max_height.get()
        
        # Si la imagen ya es más pequeña, no redimensionar
        if width <= max_w and height <= max_h:
            return width, height
            
        # Calcular ratio
        ratio_w = max_w / width
        ratio_h = max_h / height
        ratio = min(ratio_w, ratio_h)
        
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        return new_width, new_height
        
    def process_images(self):
        """Procesa las imágenes seleccionadas"""
        if self.processing:
            return
            
        dest = self.dest_folder.get()
        if not dest:
            messagebox.showerror("Error", "Por favor selecciona una carpeta destino")
            return
            
        # Verificar que hay imágenes seleccionadas
        selected_images = [img for img in self.images_info if img.selected]
        if not selected_images:
            messagebox.showwarning("Advertencia", "No hay imágenes seleccionadas")
            return
            
        # Crear carpeta destino si no existe
        os.makedirs(dest, exist_ok=True)
        
        # Procesar en thread separado
        self.processing = True
        self.process_btn.config(state='disabled')
        thread = threading.Thread(target=self._process_thread, args=(selected_images, dest))
        thread.daemon = True
        thread.start()
        
    def _process_thread(self, images: List[ImageInfo], dest_folder: str):
        """Thread de procesamiento de imágenes"""
        try:
            total = len(images)
            method = self.RESIZE_METHODS[self.resize_method.get()]
            
            self.log_message(f"\n=== Iniciando procesamiento de {total} imágenes ===")
            self.progress['maximum'] = total
            self.progress['value'] = 0
            
            success_count = 0
            error_count = 0
            
            for idx, img_info in enumerate(images, 1):
                try:
                    self.log_message(f"[{idx}/{total}] Procesando {img_info.filename}...")
                    
                    # Abrir imagen
                    with Image.open(img_info.filepath) as img:
                        # Extraer datos EXIF antes de cualquier procesamiento
                        exif_data = img.getexif()
                        
                        # Aplicar rotación automática según EXIF (respeta orientación)
                        img = ImageOps.exif_transpose(img)
                        
                        # Calcular nuevas dimensiones
                        new_w, new_h = self.calculate_new_dimensions(img.width, img.height)
                        
                        # Redimensionar
                        if new_w != img.width or new_h != img.height:
                            resized_img = img.resize((new_w, new_h), method)
                            self.log_message(f"  Redimensionado: {img.width}x{img.height} -> {new_w}x{new_h}")
                        else:
                            resized_img = img
                            self.log_message(f"  Sin cambios (ya cumple restricciones)")
                        
                        # Guardar según formato
                        dest_path = os.path.join(dest_folder, img_info.filename)
                        
                        if img_info.format in ['JPEG', 'JPG']:
                            # Convertir a RGB si es necesario
                            if resized_img.mode in ('RGBA', 'LA', 'P'):
                                resized_img = resized_img.convert('RGB')
                            # Guardar con datos EXIF preservados
                            resized_img.save(dest_path, 'JPEG', quality=self.quality_jpg.get(), 
                                           optimize=True, exif=exif_data)
                            
                        elif img_info.format == 'PNG':
                            # PNG puede almacenar EXIF desde Pillow 6.0
                            resized_img.save(dest_path, 'PNG', compress_level=self.compression_png.get(), 
                                           optimize=True, exif=exif_data)
                            
                        elif img_info.format == 'WEBP':
                            # WebP también soporta EXIF
                            resized_img.save(dest_path, 'WEBP', quality=self.quality_webp.get(), 
                                           exif=exif_data)
                        
                        # Tamaño final
                        final_size = os.path.getsize(dest_path) / 1024
                        self.log_message(f"  Guardado: {final_size:.2f} KB (original: {img_info.size_kb:.2f} KB)")
                        success_count += 1
                        
                except Exception as e:
                    self.log_message(f"  ERROR: {str(e)}")
                    error_count += 1
                    
                self.progress['value'] = idx
                self.root.update_idletasks()
                
            self.log_message(f"\n=== Proceso completado ===")
            self.log_message(f"Exitosos: {success_count} | Errores: {error_count}")
            messagebox.showinfo("Completado", 
                               f"Proceso finalizado.\nExitosos: {success_count}\nErrores: {error_count}")
            
        except Exception as e:
            self.log_message(f"\nERROR CRÍTICO: {str(e)}")
            messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")
            
        finally:
            self.processing = False
            self.process_btn.config(state='normal')


def main():
    """Función principal"""
    root = tk.Tk()
    app = ExpertResizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
