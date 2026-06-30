import hashlib
import os
import secrets
import sqlite3
import string
import sys
from cryptography.fernet import Fernet
import customtkinter as ctk

# =====================================================================
# CONFIGURACIÓN DE IDENTIDAD VISUAL (PALETA CYBERPUNK - DARK)
# =====================================================================
COLOR_BG = "#0A0E17"          
COLOR_CARD = "#131A26"        
COLOR_SIDEBAR = "#0F1420"     
COLOR_TEXT_MAIN = "#F0F4F8"   
COLOR_TEXT_MUTED = "#6272A4"  

COLOR_CYAN = "#00F0FF"        
COLOR_CYAN_HOVER = "#00B8CC"  
COLOR_ERROR = "#FF5555"       
COLOR_GRAY_BTN = "#242F41"    
COLOR_GRAY_HOVER = "#34435C"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =====================================================================
# PANTALLA DE PREVISUALIZACIÓN (SPLASH SCREEN)
# =====================================================================
class PreviewSplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cargando...")
        self.geometry("550x350")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        
        frame_interior = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=16, border_width=1, border_color="#1E293B")
        frame_interior.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.lbl_nombre_grande = ctk.CTkLabel(frame_interior, text="CIPHERGATE", font=("Consolas", 48, "bold"), text_color=COLOR_CYAN)
        self.lbl_nombre_grande.pack(pady=(65, 5))
        
        self.lbl_suite = ctk.CTkLabel(frame_interior, text="SUITE DE CIFRADO", font=("Segoe UI", 16, "bold"), text_color=COLOR_TEXT_MAIN)
        self.lbl_suite.pack(pady=5)
        
        self.lbl_sub = ctk.CTkLabel(frame_interior, text="Gestión de Credenciales & Algoritmos Simétricos", font=("Segoe UI", 12, "italic"), text_color=COLOR_TEXT_MUTED)
        self.lbl_sub.pack(pady=(0, 35))
        
        self.progreso = ctk.CTkProgressBar(frame_interior, width=320, mode="indefinite", progress_color=COLOR_CYAN, fg_color=COLOR_BG)
        self.progreso.pack(pady=10)
        self.progreso.start()


# =====================================================================
# PANTALLA DE INICIO DE SESIÓN (LOGIN SCREEN)
# =====================================================================
class LoginScreen(ctk.CTkToplevel):
    def __init__(self, parent, on_success_callback):
        super().__init__(parent)
        self.on_success = on_success_callback
        self.title("CipherGate — Autenticación")
        self.geometry("420x400")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"420x400+{x}+{y}")
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        frame_login = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=16, border_width=1, border_color="#1E293B")
        frame_login.pack(fill="both", expand=True, padx=20, pady=20)
        
        lbl_titulo = ctk.CTkLabel(frame_login, text="ACCESO REQUERIDO", font=("Consolas", 22, "bold"), text_color=COLOR_CYAN)
        lbl_titulo.pack(pady=(35, 20))
        
        self.entry_user = ctk.CTkEntry(frame_login, placeholder_text="Usuario Operador", width=280, height=42, fg_color=COLOR_BG, border_color="#1E293B", text_color=COLOR_TEXT_MAIN, placeholder_text_color=COLOR_TEXT_MUTED)
        self.entry_user.pack(pady=10)
        self.entry_user.focus_set()
        
        self.entry_pass = ctk.CTkEntry(frame_login, placeholder_text="Clave de Acceso", show="*", width=280, height=42, fg_color=COLOR_BG, border_color="#1E293B", text_color=COLOR_TEXT_MAIN, placeholder_text_color=COLOR_TEXT_MUTED)
        self.entry_pass.pack(pady=10)
        
        self.lbl_error = ctk.CTkLabel(frame_login, text="", text_color=COLOR_ERROR, font=("Segoe UI", 12, "bold"))
        self.lbl_error.pack(pady=5)
        
        self.btn_ingresar = ctk.CTkButton(frame_login, text="Ingresar", width=280, height=45, font=("Segoe UI", 14, "bold"), fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_HOVER, text_color=COLOR_BG, command=self.validar_credenciales)
        self.btn_ingresar.pack(pady=15)
        
        self.bind("<Return>", lambda e: self.validar_credenciales())

    def validar_credenciales(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get().strip()
        
        if not user or not pwd:
            self.lbl_error.configure(text="[!] Por favor, llene todos los campos.")
            return

        pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
        
        if hasattr(sys, '_MEIPASS'):
            ruta_carpeta = os.path.dirname(os.path.abspath(sys.executable))
        else:
            ruta_carpeta = os.path.dirname(os.path.abspath(__file__))
            
        self.ruta_base_datos = os.path.join(ruta_carpeta, "ciphergate_users.db")
        
        try:
            conn = sqlite3.connect(self.ruta_base_datos)
            cursor = conn.cursor()
            cursor.execute("SELECT usuario, rol FROM usuarios WHERE usuario = ? AND contrasena_hash = ?", (user, pwd_hash))
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                nombre_usuario, rol_usuario = resultado[0], resultado[1]
                self.destroy()
                self.on_success(rol_usuario)
            else:
                self.lbl_error.configure(text="[!] Credenciales Inválidas. Intente de nuevo.")
                self.entry_pass.delete(0, 'end')
                
        except sqlite3.OperationalError:
            self.lbl_error.configure(text="[!] Error: 'ciphergate_users.db' no encontrado.")

    def on_close(self):
        self.master.destroy()


# =====================================================================
# APLICACIÓN PRINCIPAL
# =====================================================================
class CipherGateApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.clave_simetrica = Fernet.generate_key()
        self.fernet = Fernet(self.clave_simetrica)

        self.title("CipherGate Suite v1.0 — Gestión y Criptografía")
        self.app_width = 950
        self.app_height = 580
        self.geometry(f"{self.app_width}x{self.app_height}")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        # Layout Principal
        self.grid_columnconfigure(0, minsize=230, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. PANEL LATERAL (SIDEBAR)
        self.sidebar_frame = ctk.CTkFrame(self, width=230, corner_radius=0, fg_color=COLOR_SIDEBAR, border_width=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.pack_propagate(False) 
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CIPHERGATE\nSUITE", font=("Consolas", 22, "bold"), text_color=COLOR_CYAN)
        self.logo_label.pack(pady=(35, 30))

        self.botones_menu = {}
        self.pantallas = {}

        # Opciones base de operador normal
        self.opciones_menu_base = [
            ("gen", "1. Generar Password (F1)"),
            ("eval", "2. Evaluar Password (F2)"),
            ("cifrar", "3. Cifrar Mensaje (F3)"),
            ("descifrar", "4. Descifrar Mensaje (F4)")
        ]

        self.footer_label = ctk.CTkLabel(self.sidebar_frame, text="2026 © LURRVO", font=("Segoe UI", 11), text_color=COLOR_TEXT_MUTED)
        self.footer_label.pack(side="bottom", pady=25)

        # 2. CONTENEDOR PRINCIPAL DERECHO
        self.main_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=COLOR_CARD, border_width=1, border_color="#1E293B")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Flujo de arranque con Splash
        self.withdraw()
        self.splash = PreviewSplashScreen(self)
        self.after(5000, self.finalizar_previsualizacion)

    def finalizar_previsualizacion(self):
        self.splash.destroy()
        self.login = LoginScreen(self, on_success_callback=self.construir_y_mostrar_app)

    def construir_y_mostrar_app(self, rol):
        """Construye las pestañas dinámicamente dependiendo del rol recibido."""
        opciones = list(self.opciones_menu_base)
        
        if rol == 1:
            opciones.append(("admin_users", "🛡️ Control Usuarios (F5)"))

        for clave, texto in opciones:
            btn = ctk.CTkButton(
                self.sidebar_frame, text=texto, height=40, anchor="w", font=("Segoe UI", 12, "bold"),
                fg_color="transparent", hover_color=COLOR_GRAY_BTN, text_color=COLOR_TEXT_MAIN,
                command=lambda k=clave: self.mostrar_pantalla(k)
            )
            btn.pack(pady=6, padx=15, fill="x")
            self.botones_menu[clave] = btn

        self.crear_pantalla_generador()
        self.crear_pantalla_evaluador()
        self.crear_pantalla_cifrado()
        self.crear_pantalla_descifrado()
        
        if rol == 1:
            self.crear_pantalla_admin_usuarios()
            self.bind("<F5>", lambda e: self.mostrar_pantalla("admin_users"))

        self.bind("<F1>", lambda e: self.mostrar_pantalla("gen"))
        self.bind("<F2>", lambda e: self.mostrar_pantalla("eval"))
        self.bind("<F3>", lambda e: self.mostrar_pantalla("cifrar"))
        self.bind("<F4>", lambda e: self.mostrar_pantalla("descifrar"))

        self.mostrar_pantalla("gen")
        x = (self.winfo_screenwidth() // 2) - (self.app_width // 2)
        y = (self.winfo_screenheight() // 2) - (self.app_height // 2)
        self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")
        self.deiconify()

    def mostrar_pantalla(self, nombre_pantalla):
        # [El código de mostrar_pantalla se mantiene intacto...]
        for k, frame in self.pantallas.items():
            frame.pack_forget()
            if k in self.botones_menu:
                self.botones_menu[k].configure(fg_color="transparent", text_color=COLOR_TEXT_MAIN)
            
        self.pantallas[nombre_pantalla].pack(fill="both", expand=True, padx=25, pady=25)
        if nombre_pantalla in self.botones_menu:
            self.botones_menu[nombre_pantalla].configure(fg_color=COLOR_GRAY_BTN, text_color=COLOR_CYAN)
        
        self.unbind("<Return>")
        
        if nombre_pantalla == "gen":
            self.entry_largo.focus_set()
            self.bind("<Return>", lambda e: self.accion_generar())
        elif nombre_pantalla == "eval":
            self.entry_eval.focus_set()
            self.bind("<Return>", lambda e: self.accion_evaluar())
        elif nombre_pantalla == "cifrar":
            self.entry_txt_cifrar.focus_set()
            self.bind("<Return>", lambda e: self.accion_cifrar())
        elif nombre_pantalla == "descifrar":
            self.entry_txt_descifrar.focus_set()
            self.bind("<Return>", lambda e: self.accion_descifrar())
        elif nombre_pantalla == "admin_users":
            self.actualizar_tabla_usuarios_gui()

    def liberar_tab_de_textbox(self, evento, siguiente_widget):
        siguiente_widget.focus_set()
        return "break"

    def obtener_ruta_db(self):
        if hasattr(sys, '_MEIPASS'):
            ruta = os.path.dirname(os.path.abspath(sys.executable))
        else:
            ruta = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(ruta, "ciphergate_users.db")

    # =====================================================================
    # LOGICA DE ACCIONES CRIPTOGRÁFICAS
    # =====================================================================
    def accion_generar(self):
        try:
            longitud = int(self.entry_largo.get().strip())
            if longitud < 4:
                longitud = 4
        except ValueError:
            longitud = 16
            
        caracteres = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(caracteres) for _ in range(longitud))
        self.txt_resultado_gen.delete("1.0", "end")
        self.txt_resultado_gen.insert("1.0", password)

    def accion_evaluar(self):
        pwd = self.entry_eval.get()
        if not pwd:
            self.lbl_veredicto.configure(text="Introduce una clave para auditar", text_color=COLOR_TEXT_MUTED)
            return
            
        longitud = len(pwd)
        tiene_mayus = any(c.isupper() for c in pwd)
        tiene_minus = any(c.islower() for c in pwd)
        tiene_num = any(c.isdigit() for c in pwd)
        tiene_simb = any(c in string.punctuation for c in pwd)
        
        tipos = sum([tiene_mayus, tiene_minus, tiene_num, tiene_simb])
        
        if longitud >= 16 and tipos == 4:
            self.lbl_veredicto.configure(text="VEREDICTO: MILITAR 🟢 (Robusta e Inviolable)", text_color="#5b920e")
        elif longitud >= 12 and tipos >= 3:
            self.lbl_veredicto.configure(text="VEREDICTO: SEGURA 🟡 (Buena resistencia)", text_color="#c08a0c")
        elif longitud >= 8 and tipos >= 2:
            self.lbl_veredicto.configure(text="VEREDICTO: DÉBIL 🟠 (Vulnerable a fuerza bruta)", text_color="#fd7e14")
        else:
            self.lbl_veredicto.configure(text="VEREDICTO: CRÍTICA 🔴 (Insegura. Cambiar de inmediato)", text_color="#fa5252")

    def accion_cifrar(self):
        texto = self.entry_txt_cifrar.get().strip()
        if not texto:
            return
        clave = Fernet.generate_key()
        f = Fernet(clave)
        token = f.encrypt(texto.encode())
        
        self.txt_out_cifrado.delete("1.0", "end")
        self.txt_out_cifrado.insert("1.0", token.decode())
        self.txt_out_key.delete("1.0", "end")
        self.txt_out_key.insert("1.0", clave.decode())

    def accion_descifrar(self):
        token_cifrado = self.entry_txt_descifrar.get().strip()
        clave_privada = self.entry_key_descifrar.get().strip()
        if not token_cifrado or not clave_privada:
            return
        try:
            f = Fernet(clave_privada.encode())
            texto_claro = f.decrypt(token_cifrado.encode()).decode()
            self.txt_out_descifrado.delete("1.0", "end")
            self.txt_out_descifrado.insert("1.0", texto_claro)
        except Exception:
            self.txt_out_descifrado.delete("1.0", "end")
            self.txt_out_descifrado.insert("1.0", "ERROR: Clave o mensaje corrupto.")

    # =====================================================================
    # PANTALLA 1: GENERADOR
    # =====================================================================
    def crear_pantalla_generador(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pantallas["gen"] = frame
        
        titulo = ctk.CTkLabel(frame, text="Generador de Contraseñas Criptográficas", font=("Segoe UI", 20, "bold"), text_color=COLOR_CYAN)
        titulo.pack(pady=(20, 20))
        
        info = ctk.CTkLabel(frame, text="Introduce la longitud deseada para la clave (Mínimo 4, Recomendado: 12 a 16):", text_color=COLOR_TEXT_MAIN)
        info.pack(pady=5)
        
        self.entry_largo = ctk.CTkEntry(frame, placeholder_text="Ej. 16", width=250, height=40, fg_color=COLOR_BG, border_color="#1E293B", text_color=COLOR_TEXT_MAIN, justify="center")
        self.entry_largo.pack(pady=10)
        
        self.btn_ejecutar_gen = ctk.CTkButton(frame, text="Generar e Inyectar Entropía", height=42, width=250, font=("Segoe UI", 13, "bold"), fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_HOVER, text_color=COLOR_BG, command=self.accion_generar)
        self.btn_ejecutar_gen.pack(pady=10)
        
        lbl_res = ctk.CTkLabel(frame, text="Resultado:", text_color=COLOR_TEXT_MUTED)
        lbl_res.pack(pady=(15, 2))
        
        self.txt_resultado_gen = ctk.CTkTextbox(frame, height=80, width=550, font=("Consolas", 13), fg_color=COLOR_BG, border_color="#1E293B", border_width=1, text_color=COLOR_CYAN)
        self.txt_resultado_gen.pack(pady=5)

    # =====================================================================
    # PANTALLA 2: EVALUADOR
    # =====================================================================
    def crear_pantalla_evaluador(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pantallas["eval"] = frame
        
        titulo = ctk.CTkLabel(frame, text="Analizador de Seguridad y Robustez", font=("Segoe UI", 20, "bold"), text_color=COLOR_CYAN)
        titulo.pack(pady=(15, 15))
        
        info = ctk.CTkLabel(frame, text="Introduce la contraseña a evaluar (los caracteres se enmascaran por protección):", text_color=COLOR_TEXT_MAIN)
        info.pack(pady=5)
        
        self.entry_eval = ctk.CTkEntry(frame, show="*", width=400, height=40, fg_color=COLOR_BG, border_color="#1E293B", text_color=COLOR_TEXT_MAIN, justify="center")
        self.entry_eval.pack(pady=5)
        
        self.btn_analizar = ctk.CTkButton(frame, text="Auditar Credencial", height=42, width=200, font=("Segoe UI", 13, "bold"), fg_color=COLOR_GRAY_BTN, hover_color=COLOR_GRAY_HOVER, text_color=COLOR_TEXT_MAIN, command=self.accion_evaluar)
        self.btn_analizar.pack(pady=10)
        
        self.lbl_veredicto = ctk.CTkLabel(frame, text="Esperando entrada...", font=("Segoe UI", 13, "bold"), text_color=COLOR_TEXT_MUTED, justify="center")
        self.lbl_veredicto.pack(pady=10)

        tabla_frame = ctk.CTkFrame(frame, fg_color=COLOR_BG, corner_radius=12, border_width=1, border_color="#1E293B")
        tabla_frame.pack(pady=15, padx=20)
        
        tabla_frame.grid_columnconfigure(0, weight=1, minsize=140)
        tabla_frame.grid_columnconfigure(1, weight=1, minsize=90)
        tabla_frame.grid_columnconfigure(2, weight=1, minsize=320)

        headers = ["Nivel / Estado", "Longitud", "Requisitos de Complejidad"]
        for col, h in enumerate(headers):
            ctk.CTkLabel(tabla_frame, text=h, font=("Segoe UI", 11, "bold"), text_color=COLOR_TEXT_MUTED).grid(row=0, column=col, padx=15, pady=8, sticky="nsew")

        criterios = [
            ("MILITAR 🟢", ">= 16", "4 de 4 (Mayús + Minús + Núm + Símbolo)", "#5b920e"),   
            ("SEGURA 🟡", "12 a 15", "Al menos 3 tipos combinados", "#c08a0c"),   
            ("DÉBIL 🟠", "8 a 11", "Menos de 3 tipos combinados", "#fd7e14"),     
            ("CRÍTICA 🔴", "< 8", "Longitud insuficiente (Descifrado inmediato)", "#fa5252")  
        ]
        for row, (niv, lon, t, col_hex) in enumerate(criterios, start=1):
            ctk.CTkLabel(tabla_frame, text=niv, text_color=col_hex, font=("Segoe UI", 12, "bold")).grid(row=row, column=0, padx=15, pady=4, sticky="nsew")
            ctk.CTkLabel(tabla_frame, text=lon, text_color=COLOR_TEXT_MAIN).grid(row=row, column=1, padx=15, pady=4, sticky="nsew")
            ctk.CTkLabel(tabla_frame, text=t, text_color=COLOR_TEXT_MAIN).grid(row=row, column=2, padx=15, pady=4, sticky="nsew")

    # =====================================================================
    # PANTALLA 3: CIFRADO
    # =====================================================================
    def crear_pantalla_cifrado(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pantallas["cifrar"] = frame
        
        titulo = ctk.CTkLabel(frame, text="Módulo de Cifrado de Información", font=("Segoe UI", 20, "bold"), text_color=COLOR_CYAN)
        titulo.pack(pady=(15, 15))
        
        info = ctk.CTkLabel(frame, text="Escribe el texto secreto que deseas bloquear:", text_color=COLOR_TEXT_MAIN)
        info.pack(pady=2)
        
        self.entry_txt_cifrar = ctk.CTkEntry(frame, width=550, height=40, fg_color=COLOR_BG, border_color="#1E293B", text_color=COLOR_TEXT_MAIN, justify="center")
        self.entry_txt_cifrar.pack(pady=5)
        
        self.btn_ejecutar_cif = ctk.CTkButton(frame, text="Cifrar Datos", height=42, width=200, font=("Segoe UI", 13, "bold"), fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_HOVER, text_color=COLOR_BG, command=self.accion_cifrar)
        self.btn_ejecutar_cif.pack(pady=10)
        
        ctk.CTkLabel(frame, text="Mensaje Cifrado Resultante (Output):", text_color=COLOR_TEXT_MUTED).pack(pady=(10, 2))
        self.txt_out_cifrado = ctk.CTkTextbox(frame, height=70, width=550, font=("Consolas", 12), fg_color=COLOR_BG, border_color="#1E293B", border_width=1, text_color=COLOR_TEXT_MAIN)
        self.txt_out_cifrado.pack(pady=5)
        
        ctk.CTkLabel(frame, text="🔑 CLAVE DE SESIÓN PRIVADA (Necesaria para descifrar):", font=("Segoe UI", 12, "bold"), text_color=COLOR_CYAN).pack(pady=(10, 2))
        self.txt_out_key = ctk.CTkTextbox(frame, height=40, width=550, font=("Consolas", 12), fg_color=COLOR_BG, border_color="#1E293B", border_width=1, text_color=COLOR_CYAN) 
        self.txt_out_key.pack(pady=5)

    # =====================================================================
    # PANTALLA 4: DESCIFRADO
    # =====================================================================
    def crear_pantalla_descifrado(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pantallas["descifrar"] = frame
        
        titulo = ctk.CTkLabel(frame, text="Módulo de Descifrado y Recuperación", font=("Segoe UI", 20, "bold"), text_color=COLOR_CYAN)
        titulo.pack(pady=(15, 15))
        
        ctk.CTkLabel(frame, text="Pega el bloque de texto cifrado:", text_color=COLOR_TEXT_MAIN).pack(pady=2)
        self.entry_txt_descifrar = ctk.CTkEntry(frame, width=550, height=40, fg_color=COLOR_BG, border_color="#1E293B", text_color=COLOR_TEXT_MAIN, justify="center")
        self.entry_txt_descifrar.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Introduce la Clave Privada correspondiente:", text_color=COLOR_TEXT_MAIN).pack(pady=2)
        self.entry_key_descifrar = ctk.CTkEntry(frame, width=550, height=40, show="*", fg_color=COLOR_BG, border_color="#1E293B", text_color=COLOR_TEXT_MAIN, justify="center")
        self.entry_key_descifrar.pack(pady=5)
        
        self.btn_ejecutar_des = ctk.CTkButton(frame, text="Descifrar y Revelar", height=42, width=200, font=("Segoe UI", 13, "bold"), fg_color=COLOR_ERROR, hover_color="#CC4444", text_color=COLOR_TEXT_MAIN, command=self.accion_descifrar)
        self.btn_ejecutar_des.pack(pady=15)
        
        ctk.CTkLabel(frame, text="Texto Original Recuperado:", text_color=COLOR_TEXT_MUTED).pack()
        self.txt_out_descifrado = ctk.CTkTextbox(frame, height=70, width=550, font=("Segoe UI", 14, "bold"), fg_color=COLOR_BG, border_color="#1E293B", border_width=1, text_color=COLOR_CYAN)
        self.txt_out_descifrado.pack(pady=5)

    # =====================================================================
    # PANTALLA PRIVILEGIADA 5: ADMINISTRACIÓN DE USUARIOS GUI
    # =====================================================================
    def crear_pantalla_admin_usuarios(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pantallas["admin_users"] = frame

        titulo = ctk.CTkLabel(frame, text="Panel de Gestión de Usuarios y Credenciales", font=("Segoe UI", 20, "bold"), text_color=COLOR_CYAN)
        titulo.pack(pady=(10, 15))

        split_frame = ctk.CTkFrame(frame, fg_color="transparent")
        split_frame.pack(fill="both", expand=True, padx=10)
        split_frame.columnconfigure(0, weight=1, minsize=320)
        split_frame.columnconfigure(1, weight=0, minsize=280)
        split_frame.rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(split_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Operadores en Base de Datos:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_MAIN).pack(pady=2)
        self.txt_lista_usuarios = ctk.CTkTextbox(left_frame, font=("Consolas", 12), fg_color=COLOR_BG, border_color="#1E293B", border_width=1, text_color=COLOR_TEXT_MAIN)
        self.txt_lista_usuarios.pack(fill="both", expand=True, pady=5)

        right_frame = ctk.CTkScrollableFrame(split_frame, fg_color=COLOR_CARD, border_color="#1E293B", border_width=1, label_text="OPERACIONES DE ENTRADA")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.adm_user = ctk.CTkEntry(right_frame, placeholder_text="Nombre de Usuario / Nuevo Nombre", height=35, justify="center")
        self.adm_user.pack(fill="x", pady=5, padx=10)

        self.adm_pass = ctk.CTkEntry(right_frame, placeholder_text="Contraseña (Crear / Cambiar)", show="*", height=35, justify="center")
        self.adm_pass.pack(fill="x", pady=5, padx=10)

        self.adm_id = ctk.CTkEntry(right_frame, placeholder_text="ID Objetivo (Modificar/Eliminar)", height=35, justify="center")
        self.adm_id.pack(fill="x", pady=5, padx=10)

        self.lbl_adm_feedback = ctk.CTkLabel(right_frame, text="", font=("Segoe UI", 12, "bold"), text_color=COLOR_CYAN, justify="center")
        self.lbl_adm_feedback.pack(pady=5)

        ctk.CTkButton(right_frame, text="Registrar Operador", fg_color="#2b9e4b", height=35, font=("Segoe UI", 12, "bold"), command=self.adm_registrar).pack(fill="x", pady=4, padx=10)
        ctk.CTkButton(right_frame, text="Modificar Nombre (Por ID)", fg_color=COLOR_GRAY_BTN, hover_color=COLOR_GRAY_HOVER, height=35, font=("Segoe UI", 12, "bold"), command=self.adm_modificar_nombre).pack(fill="x", pady=4, padx=10)
        ctk.CTkButton(right_frame, text="Cambiar Contraseña (Por ID)", fg_color=COLOR_GRAY_BTN, hover_color=COLOR_GRAY_HOVER, height=35, font=("Segoe UI", 12, "bold"), command=self.adm_cambiar_pass).pack(fill="x", pady=4, padx=10)
        ctk.CTkButton(right_frame, text="Eliminar Operador (Por ID)", fg_color=COLOR_ERROR, hover_color="#CC4444", height=35, font=("Segoe UI", 12, "bold"), command=self.adm_eliminar).pack(fill="x", pady=4, padx=10)

    def actualizar_tabla_usuarios_gui(self):
        self.txt_lista_usuarios.delete("1.0", "end")
        conn = sqlite3.connect(self.obtener_ruta_db())
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario, rol FROM usuarios ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            tipo = "ADMIN" if r[2] == 1 else "OPERADOR"
            self.txt_lista_usuarios.insert("end", f"ID: {r[0]} | Usuario: {r[1]} [{tipo}]\n")

    def adm_registrar(self):
        u, p = self.adm_user.get().strip(), self.adm_pass.get().strip()
        if not u or not p:
            self.lbl_adm_feedback.configure(text="[!] Complete Usuario y Clave", text_color=COLOR_ERROR)
            return
        h = hashlib.sha256(p.encode()).hexdigest()
        conn = sqlite3.connect(self.obtener_ruta_db())
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (usuario, contrasena_hash, rol) VALUES (?, ?, 0)", (u, h))
            conn.commit()
            self.lbl_adm_feedback.configure(text=f"[+] '{u}' registrado.", text_color="#2b9e4b")
            self.actualizar_tabla_usuarios_gui()
        except sqlite3.IntegrityError:
            self.lbl_adm_feedback.configure(text="[!] El usuario ya existe.", text_color=COLOR_ERROR)
        conn.close()

    def adm_modificar_nombre(self):
        target_id, nuevo_nombre = self.adm_id.get().strip(), self.adm_user.get().strip()
        if not target_id or not nuevo_nombre:
            self.lbl_adm_feedback.configure(text="[!] Requiere ID e Input Usuario.", text_color=COLOR_ERROR)
            return
        conn = sqlite3.connect(self.obtener_ruta_db())
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET usuario = ? WHERE id = ?", (nuevo_nombre, target_id))
        if cursor.rowcount > 0:
            conn.commit()
            self.lbl_adm_feedback.configure(text=f"[+] ID {target_id} actualizado.", text_color="#2b9e4b")
            self.actualizar_tabla_usuarios_gui()
        else:
            self.lbl_adm_feedback.configure(text="[!] ID no encontrado.", text_color=COLOR_ERROR)
        conn.close()

    def adm_cambiar_pass(self):
        target_id, nueva_pass = self.adm_id.get().strip(), self.adm_pass.get().strip()
        if not target_id or not nueva_pass:
            self.lbl_adm_feedback.configure(text="[!] Requiere ID e Input Contraseña.", text_color=COLOR_ERROR)
            return
        h = hashlib.sha256(nueva_pass.encode()).hexdigest()
        conn = sqlite3.connect(self.obtener_ruta_db())
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET contrasena_hash = ? WHERE id = ?", (h, target_id))
        if cursor.rowcount > 0:
            conn.commit()
            self.lbl_adm_feedback.configure(text=f"[+] Clave de ID {target_id} cambiada.", text_color="#2b9e4b")
        else:
            self.lbl_adm_feedback.configure(text="[!] ID no encontrado.", text_color=COLOR_ERROR)
        conn.close()

    def adm_eliminar(self):
        target_id = self.adm_id.get().strip()
        if not target_id:
            self.lbl_adm_feedback.configure(text="[!] Escribe el ID a eliminar.", text_color=COLOR_ERROR)
            return
        conn = sqlite3.connect(self.obtener_ruta_db())
        cursor = conn.cursor()
        
        cursor.execute("SELECT usuario FROM usuarios WHERE id = ?", (target_id,))
        res = cursor.fetchone()
        if res and res[0] == "admin":
            self.lbl_adm_feedback.configure(text="[!] No puedes borrar al admin.", text_color=COLOR_ERROR)
            conn.close()
            return

        cursor.execute("DELETE FROM usuarios WHERE id = ?", (target_id,))
        if cursor.rowcount > 0:
            conn.commit()
            self.lbl_adm_feedback.configure(text=f"[-] ID {target_id} eliminado.", text_color=COLOR_ERROR)
            self.actualizar_tabla_usuarios_gui()
        else:
            self.lbl_adm_feedback.configure(text="[!] ID no encontrado.", text_color=COLOR_ERROR)
        conn.close()


if __name__ == "__main__":
    app = CipherGateApp()
    app.mainloop()