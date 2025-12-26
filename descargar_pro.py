#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Descargador Automático de Datos Históricos
- Forex (usando duka/Dukascopy)
- Índices y Acciones (usando yfinance/Yahoo Finance)
"""

import subprocess
import sys
import os
from datetime import datetime, timedelta

# pandas se importará después si es necesario

class DataDownloader:
    def __init__(self):
        self.fecha_inicio = None
        self.fecha_fin = None
        self.tipo_descarga = None  # 'forex' o 'indices'
        self.instrumentos = []
        self.temporalidad = None
        self.ruta_guardado = None
        
        # Temporalidades para Forex
        self.timeframes_forex = {
            '1': 'tick',
            '2': 'M1',   # 1 minuto
            '3': 'M5',   # 5 minutos
            '4': 'M15',  # 15 minutos
            '5': 'M30',  # 30 minutos
            '6': 'H1',   # 1 hora
            '7': 'H4',   # 4 horas
            '8': 'D1'    # Diario
        }
        
        # Temporalidades para Índices/Acciones
        self.timeframes_indices = {
            '1': '1m',   # 1 minuto
            '2': '5m',   # 5 minutos
            '3': '15m',  # 15 minutos
            '4': '30m',  # 30 minutos
            '5': '1h',   # 1 hora
            '6': '1d',   # Diario
            '7': '1wk',  # Semanal
            '8': '1mo'   # Mensual
        }
        
    def instalar_dependencias(self):
        """Instala duka y yfinance automáticamente"""
        print("\n" + "="*60)
        print("VERIFICANDO E INSTALANDO DEPENDENCIAS")
        print("="*60)
        
        dependencias_instaladas = True
        
        # Instalar/Verificar pandas primero
        try:
            import pandas
            print("✓ pandas ya está instalado")
        except ImportError:
            print("Instalando pandas...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
                print("✓ pandas instalado correctamente")
            except Exception as e:
                print(f"✗ Error al instalar pandas: {e}")
                dependencias_instaladas = False
        
        # Verificar/Instalar duka (SIN GIT)
        try:
            result = subprocess.run(['pip', 'show', 'duka'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Duka ya está instalado")
            else:
                print("Instalando duka (descarga directa, sin Git)...")
                # Descargar ZIP del repositorio directamente
                import urllib.request
                import zipfile
                import tempfile
                import shutil
                
                # URL del ZIP del repositorio
                zip_url = "https://github.com/giuse88/duka/archive/refs/heads/master.zip"
                
                with tempfile.TemporaryDirectory() as tmpdir:
                    zip_path = os.path.join(tmpdir, "duka.zip")
                    
                    # Descargar
                    print("  Descargando duka...")
                    urllib.request.urlretrieve(zip_url, zip_path)
                    
                    # Extraer
                    print("  Extrayendo archivos...")
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(tmpdir)
                    
                    # Instalar
                    print("  Instalando duka...")
                    duka_dir = os.path.join(tmpdir, "duka-master")
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', duka_dir])
                
                print("✓ Duka instalado correctamente (sin Git)")
        except Exception as e:
            print(f"✗ Error al instalar duka: {e}")
            print("💡 Si usas FOREX, duka es necesario. Para índices, no lo necesitas.")
            # No falla completamente, solo advierte
        
        # Verificar/Instalar yfinance
        try:
            result = subprocess.run(['pip', 'show', 'yfinance'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ yfinance ya está instalado")
            else:
                print("Instalando yfinance...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', 'yfinance'
                ])
                print("✓ yfinance instalado correctamente")
        except Exception as e:
            print(f"✗ Error al instalar yfinance: {e}")
            dependencias_instaladas = False
        
        return dependencias_instaladas
    
    def mostrar_banner(self):
        """Muestra el banner de bienvenida"""
        print("\n" + "="*60)
        print("  DESCARGADOR DE DATOS HISTÓRICOS")
        print("  - Forex (Dukascopy)")
        print("  - Índices y Acciones (Yahoo Finance)")
        print("="*60)
        print("  Descarga automática de datos históricos")
        print("="*60 + "\n")
    
    def seleccionar_tipo_descarga(self):
        """Selecciona entre Forex o Índices/Acciones"""
        print("\n--- TIPO DE DATOS A DESCARGAR ---")
        print("\n1. FOREX - Pares de divisas (EURUSD, GBPUSD, etc.)")
        print("2. ÍNDICES Y ACCIONES - S&P 500, NASDAQ, Apple, etc.")
        
        while True:
            opcion = input("\nSeleccione una opción (1-2): ").strip()
            if opcion == '1':
                self.tipo_descarga = 'forex'
                print("✓ Modo: FOREX seleccionado")
                break
            elif opcion == '2':
                self.tipo_descarga = 'indices'
                print("✓ Modo: ÍNDICES Y ACCIONES seleccionado")
                break
            else:
                print("✗ Opción inválida")
    
    def configurar_fechas(self):
        """Configura las fechas de inicio y fin"""
        print("\n--- CONFIGURACIÓN DE FECHAS ---")
        
        while True:
            try:
                # Fecha de inicio
                print("\nFecha de inicio (formato: YYYY-MM-DD)")
                fecha_inicio_str = input("Ejemplo: 2023-01-01: ").strip()
                self.fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
                
                # Fecha de fin
                print("\nFecha de fin (formato: YYYY-MM-DD)")
                print(f"Fecha actual: {datetime.now().strftime('%Y-%m-%d')}")
                fecha_fin_str = input("Presiona Enter para usar hoy o ingresa fecha: ").strip()
                
                if fecha_fin_str == "":
                    self.fecha_fin = datetime.now()
                else:
                    self.fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
                
                # Validar que fecha_inicio < fecha_fin
                if self.fecha_inicio >= self.fecha_fin:
                    print("✗ La fecha de inicio debe ser anterior a la fecha de fin")
                    continue
                
                print(f"\n✓ Fechas configuradas:")
                print(f"  Inicio: {self.fecha_inicio.strftime('%Y-%m-%d')}")
                print(f"  Fin: {self.fecha_fin.strftime('%Y-%m-%d')}")
                print(f"  Período: {(self.fecha_fin - self.fecha_inicio).days} días")
                break
                
            except ValueError:
                print("✗ Formato de fecha inválido. Use YYYY-MM-DD")
    
    def configurar_instrumentos_forex(self):
        """Configura los pares de forex a descargar"""
        print("\n--- SELECCIÓN DE PARES DE FOREX ---")
        
        pares_comunes = [
            'EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF',
            'AUDUSD', 'USDCAD', 'NZDUSD', 'EURGBP',
            'EURJPY', 'GBPJPY', 'AUDJPY', 'EURAUD'
        ]
        
        print("\nPares más comunes:")
        for i, par in enumerate(pares_comunes, 1):
            print(f"  {i:2d}. {par}")
        
        print("\nOpciones:")
        print("  - Ingrese números separados por comas (ej: 1,2,3)")
        print("  - Ingrese 'todos' para todos los pares comunes")
        print("  - Ingrese pares manualmente (ej: EURUSD,GBPJPY)")
        
        seleccion = input("\nSu selección: ").strip().upper()
        
        if seleccion == 'TODOS':
            self.instrumentos = pares_comunes
        elif seleccion.replace(',', '').replace(' ', '').isdigit():
            indices = [int(x.strip()) for x in seleccion.split(',')]
            self.instrumentos = [pares_comunes[i-1] for i in indices if 1 <= i <= len(pares_comunes)]
        else:
            self.instrumentos = [p.strip() for p in seleccion.split(',')]
        
        print(f"\n✓ Pares seleccionados: {', '.join(self.instrumentos)}")
    
    def configurar_instrumentos_indices(self):
        """Configura los índices/acciones a descargar"""
        print("\n--- SELECCIÓN DE ÍNDICES Y ACCIONES ---")
        
        instrumentos_comunes = {
            'Índices': [
                ('^GSPC', 'S&P 500'),
                ('^DJI', 'Dow Jones'),
                ('^IXIC', 'NASDAQ'),
                ('^RUT', 'Russell 2000'),
                ('^VIX', 'VIX - Volatilidad'),
                ('^FTSE', 'FTSE 100'),
                ('^GDAXI', 'DAX'),
                ('^N225', 'Nikkei 225')
            ],
            'Acciones Populares': [
                ('AAPL', 'Apple'),
                ('MSFT', 'Microsoft'),
                ('GOOGL', 'Google'),
                ('AMZN', 'Amazon'),
                ('TSLA', 'Tesla'),
                ('NVDA', 'NVIDIA'),
                ('META', 'Meta'),
                ('JPM', 'JPMorgan')
            ]
        }
        
        print("\n📊 ÍNDICES PRINCIPALES:")
        idx = 1
        mapeo = {}
        for simbolo, nombre in instrumentos_comunes['Índices']:
            print(f"  {idx:2d}. {simbolo:8s} - {nombre}")
            mapeo[idx] = simbolo
            idx += 1
        
        print("\n📈 ACCIONES POPULARES:")
        for simbolo, nombre in instrumentos_comunes['Acciones Populares']:
            print(f"  {idx:2d}. {simbolo:8s} - {nombre}")
            mapeo[idx] = simbolo
            idx += 1
        
        print("\n⚠️ IMPORTANTE: Para otros instrumentos, use los símbolos de Yahoo Finance")
        print("   Ejemplo: BTC-USD (Bitcoin), GC=F (Oro), CL=F (Petróleo)")
        
        print("\nOpciones:")
        print("  - Ingrese números separados por comas (ej: 1,2,3)")
        print("  - Ingrese símbolos manualmente (ej: ^GSPC,AAPL,MSFT)")
        
        seleccion = input("\nSu selección: ").strip().upper()
        
        if seleccion.replace(',', '').replace(' ', '').isdigit():
            indices = [int(x.strip()) for x in seleccion.split(',')]
            self.instrumentos = [mapeo[i] for i in indices if i in mapeo]
        else:
            self.instrumentos = [s.strip() for s in seleccion.split(',')]
        
        print(f"\n✓ Instrumentos seleccionados: {', '.join(self.instrumentos)}")
    
    def validar_temporalidad_periodo(self):
        """Valida que la temporalidad sea compatible con el período seleccionado"""
        if self.tipo_descarga != 'indices':
            return True
        
        dias_diferencia = (self.fecha_fin - self.fecha_inicio).days
        
        # Límites de Yahoo Finance
        limites = {
            '1m': 7,
            '5m': 60,
            '15m': 60,
            '30m': 60,
            '1h': 730  # ~2 años
        }
        
        if self.temporalidad in limites:
            max_dias = limites[self.temporalidad]
            if dias_diferencia > max_dias:
                print(f"\n⚠️ ADVERTENCIA: Yahoo Finance no permite descargar {self.temporalidad}")
                print(f"   para períodos mayores a {max_dias} días.")
                print(f"   Tu período es de {dias_diferencia} días.")
                print(f"\n   Opciones:")
                print(f"   1. Cambiar a temporalidad diaria (1d) o mayor")
                print(f"   2. Reducir el período de fechas a máx. {max_dias} días")
                return False
        
        return True
    
    def configurar_temporalidad(self):
        """Configura la temporalidad de los datos"""
        print("\n--- TEMPORALIDAD DE LOS DATOS ---")
        
        if self.tipo_descarga == 'forex':
            print("\nSeleccione la temporalidad:")
            print("  1. TICK    - Datos tick por tick (más detallado)")
            print("  2. M1      - 1 minuto")
            print("  3. M5      - 5 minutos")
            print("  4. M15     - 15 minutos")
            print("  5. M30     - 30 minutos")
            print("  6. H1      - 1 hora")
            print("  7. H4      - 4 horas")
            print("  8. D1      - Diario")
            
            while True:
                opcion = input("\nIngrese el número (1-8): ").strip()
                if opcion in self.timeframes_forex:
                    self.temporalidad = self.timeframes_forex[opcion]
                    print(f"✓ Temporalidad seleccionada: {self.temporalidad}")
                    break
                else:
                    print("✗ Opción inválida")
        else:
            dias_periodo = (self.fecha_fin - self.fecha_inicio).days
            
            print(f"\n📅 Tu período seleccionado: {dias_periodo} días")
            print("\nSeleccione la temporalidad:")
            print("  1. 1m      - 1 minuto    [Máx. 7 días]")
            print("  2. 5m      - 5 minutos   [Máx. 60 días]")
            print("  3. 15m     - 15 minutos  [Máx. 60 días]")
            print("  4. 30m     - 30 minutos  [Máx. 60 días]")
            print("  5. 1h      - 1 hora      [Máx. ~2 años]")
            print("  6. 1d      - Diario      [✓ Recomendado para tu período]")
            print("  7. 1wk     - Semanal")
            print("  8. 1mo     - Mensual")
            
            print("\n⚠️ IMPORTANTE: Yahoo Finance restringe datos intradiarios")
            if dias_periodo > 60:
                print(f"   Para tu período de {dias_periodo} días, usa opción 6 (Diario) o superior")
            
            while True:
                opcion = input("\nIngrese el número (1-8): ").strip()
                if opcion in self.timeframes_indices:
                    self.temporalidad = self.timeframes_indices[opcion]
                    print(f"✓ Temporalidad seleccionada: {self.temporalidad}")
                    
                    # Validar después de seleccionar
                    if not self.validar_temporalidad_periodo():
                        print("\n¿Desea seleccionar otra temporalidad? (S/n): ", end='')
                        if input().strip().upper() != 'N':
                            continue
                    break
                else:
                    print("✗ Opción inválida")
    
    def configurar_ruta_guardado(self):
        """Configura la ruta donde se guardarán los datos"""
        print("\n--- UBICACIÓN DE GUARDADO ---")
        
        carpeta = 'datos_forex' if self.tipo_descarga == 'forex' else 'datos_indices'
        ruta_default = os.path.join(os.getcwd(), carpeta)
        print(f"\nRuta por defecto: {ruta_default}")
        
        ruta = input("Presione Enter para usar la ruta por defecto o ingrese una nueva: ").strip()
        
        if ruta == "":
            self.ruta_guardado = ruta_default
        else:
            self.ruta_guardado = ruta
        
        # Crear el directorio si no existe
        os.makedirs(self.ruta_guardado, exist_ok=True)
        print(f"✓ Los datos se guardarán en: {self.ruta_guardado}")
    
    def mostrar_resumen(self):
        """Muestra un resumen de la configuración"""
        print("\n" + "="*60)
        print("RESUMEN DE CONFIGURACIÓN")
        print("="*60)
        print(f"Tipo:            {'FOREX' if self.tipo_descarga == 'forex' else 'ÍNDICES/ACCIONES'}")
        print(f"Fecha inicio:    {self.fecha_inicio.strftime('%Y-%m-%d')}")
        print(f"Fecha fin:       {self.fecha_fin.strftime('%Y-%m-%d')}")
        print(f"Período:         {(self.fecha_fin - self.fecha_inicio).days} días")
        print(f"Instrumentos:    {', '.join(self.instrumentos)}")
        print(f"Temporalidad:    {self.temporalidad}")
        print(f"Guardar en:      {self.ruta_guardado}")
        
        # Advertencias específicas para índices
        if self.tipo_descarga == 'indices':
            dias = (self.fecha_fin - self.fecha_inicio).days
            advertencias = []
            
            if self.temporalidad == '1m' and dias > 7:
                advertencias.append("⚠️  Temporalidad 1m solo funciona para últimos 7 días")
            elif self.temporalidad in ['5m', '15m', '30m'] and dias > 60:
                advertencias.append(f"⚠️  Temporalidad {self.temporalidad} solo funciona para últimos 60 días")
            
            if advertencias:
                print("="*60)
                for adv in advertencias:
                    print(adv)
                print("💡 Recomendación: Usa temporalidad '1d' (diaria)")
        
        print("="*60)
        
        confirmar = input("\n¿Desea proceder con la descarga? (S/n): ").strip().upper()
        return confirmar != 'N'
    
    def descargar_forex(self):
        """
        Descarga Forex con duka. 
        Si falla (0KB), intenta usar yfinance como respaldo automáticamente.
        """
        print("\n" + "="*60)
        print("DESCARGANDO DATOS DE FOREX (INTELIGENTE)")
        print("="*60)
        
        # 1. VALIDACIÓN DE FECHA FINAL
        # Dukascopy no da datos del día presente. Si fecha_fin es hoy, restamos 1 día.
        if self.fecha_fin.date() >= datetime.now().date():
            print("⚠️ AVISO: No se pueden descargar datos históricos del día en curso.")
            self.fecha_fin = self.fecha_fin - timedelta(days=1)
            print(f"   -> Fecha fin ajustada a ayer: {self.fecha_fin.strftime('%Y-%m-%d')}")

        total = len(self.instrumentos)
        
        for idx, par in enumerate(self.instrumentos, 1):
            print(f"\n[{idx}/{total}] Intentando descargar {par} con Duka...")
            
            fecha_inicio_str = self.fecha_inicio.strftime("%Y-%m-%d")
            fecha_fin_str = self.fecha_fin.strftime("%Y-%m-%d")
            
            # Construcción del comando duka corregido
            cmd = [
                'duka', par, '-s', fecha_inicio_str, '-e', fecha_fin_str,
                '--folder', self.ruta_guardado
            ]
            
            if self.temporalidad != 'tick':
                cmd.extend(['-c', self.temporalidad]) # -c para velas (candles)
            
            try:
                subprocess.run(cmd, capture_output=True, text=True)
                
                # 2. VERIFICACIÓN DE ARCHIVO 0KB
                # Buscamos el archivo más reciente creado en la carpeta
                archivos = [os.path.join(self.ruta_guardado, f) for f in os.listdir(self.ruta_guardado) if par in f]
                descarga_exitosa = False
                
                if archivos:
                    archivo_reciente = max(archivos, key=os.path.getctime)
                    tamano = os.path.getsize(archivo_reciente)
                    
                    if tamano > 0:
                        print(f"  ✓ ÉXITO: {par} descargado ({tamano/1024:.2f} KB)")
                        descarga_exitosa = True
                    else:
                        print(f"  ✗ FALLO: El archivo se creó pero está vacío (0 KB).")
                        print("    Posible causa: Duka no tiene datos para este rango o bloqueó la IP.")
                        try:
                            os.remove(archivo_reciente) # Borrar archivo basura
                        except: pass
                
                # 3. PLAN B: USAR YFINANCE SI DUKA FALLA
                if not descarga_exitosa:
                    print(f"\n  ⚠️ ACTIVANDO PLAN B: Intentando descargar {par} desde Yahoo Finance...")
                    self.descargar_forex_backup_yfinance(par)

            except Exception as e:
                print(f"  ✗ Error crítico: {e}")

    def descargar_forex_backup_yfinance(self, par):
        """Método de respaldo para bajar Forex si Duka falla"""
        try:
            import yfinance as yf
            # Convertir formato EURUSD -> EURUSD=X
            simbolo_yahoo = f"{par}=X"
            
            # Mapeo de temporalidades duka -> yahoo
            mapa_temp = {
                'M1': '1m', 'M5': '5m', 'M15': '15m', 'M30': '30m',
                'H1': '1h', 'D1': '1d'
            }
            intervalo = mapa_temp.get(self.temporalidad, '1d')
            
            print(f"    -> Conectando a Yahoo Finance ({simbolo_yahoo})...")
            ticker = yf.Ticker(simbolo_yahoo)
            df = ticker.history(start=self.fecha_inicio, end=self.fecha_fin, interval=intervalo)
            
            if not df.empty:
                nombre_archivo = f"{par}_BACKUP_{intervalo}.csv"
                ruta_final = os.path.join(self.ruta_guardado, nombre_archivo)
                df.to_csv(ruta_final)
                print(f"    ✓ RECUPERADO: Datos guardados en {nombre_archivo}")
            else:
                print("    ✗ Yahoo tampoco tiene datos para este rango.")
                
        except Exception as e:
            print(f"    ✗ Falló el respaldo: {e}")
    
    def descargar_indices(self):
        """Descarga datos de Índices/Acciones usando yfinance"""
        print("\n" + "="*60)
        print("DESCARGANDO DATOS DE ÍNDICES/ACCIONES")
        print("="*60)
        
        try:
            import yfinance as yf
        except ImportError:
            print("✗ yfinance no está instalado. Instalando...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance'])
            import yfinance as yf
        
        total = len(self.instrumentos)
        exitosos = 0
        fallidos = 0
        
        for idx, simbolo in enumerate(self.instrumentos, 1):
            print(f"\n[{idx}/{total}] Descargando {simbolo}...")
            
            try:
                ticker = yf.Ticker(simbolo)
                
                # Descargar datos con manejo de errores mejorado
                try:
                    df = ticker.history(
                        start=self.fecha_inicio,
                        end=self.fecha_fin,
                        interval=self.temporalidad,
                        auto_adjust=True,
                        actions=False
                    )
                except Exception as download_error:
                    error_msg = str(download_error)
                    if "1m data not available" in error_msg:
                        print(f"  ✗ Yahoo Finance solo permite 1m para los últimos 7 días")
                        print(f"  💡 Solución: Usa temporalidad '1d' (diaria) para este período")
                    elif "5m data not available" in error_msg:
                        print(f"  ✗ Yahoo Finance solo permite 5m para los últimos 60 días")
                        print(f"  💡 Solución: Usa temporalidad '1d' (diaria) o reduce el período")
                    else:
                        print(f"  ✗ Error de descarga: {error_msg}")
                    fallidos += 1
                    continue
                
                if df.empty:
                    print(f"  ✗ No se encontraron datos para {simbolo}")
                    print(f"  💡 Verifica que el símbolo sea correcto")
                    fallidos += 1
                    continue
                
                # Guardar a CSV
                fecha_inicio_str = self.fecha_inicio.strftime("%Y-%m-%d")
                fecha_fin_str = self.fecha_fin.strftime("%Y-%m-%d")
                nombre_archivo = f"{simbolo.replace('^', '')}_{self.temporalidad}_{fecha_inicio_str}_to_{fecha_fin_str}.csv"
                ruta_archivo = os.path.join(self.ruta_guardado, nombre_archivo)
                
                df.to_csv(ruta_archivo)
                
                tamaño = os.path.getsize(ruta_archivo) / 1024
                print(f"  ✓ {simbolo} descargado correctamente")
                print(f"  📊 Registros: {len(df):,}")
                print(f"  💾 Tamaño: {tamaño:.2f} KB")
                print(f"  📁 Archivo: {nombre_archivo}")
                
                # Mostrar primeras y últimas fechas
                print(f"  📅 Desde: {df.index[0].strftime('%Y-%m-%d %H:%M')}")
                print(f"  📅 Hasta: {df.index[-1].strftime('%Y-%m-%d %H:%M')}")
                exitosos += 1
                
            except Exception as e:
                print(f"  ✗ Error inesperado al descargar {simbolo}: {e}")
                fallidos += 1
        
        # Resumen final
        print(f"\n{'='*60}")
        print(f"RESUMEN DE DESCARGA")
        print(f"{'='*60}")
        print(f"✓ Exitosos: {exitosos}/{total}")
        if fallidos > 0:
            print(f"✗ Fallidos:  {fallidos}/{total}")
            print(f"\n💡 TIP: Para períodos largos (>60 días), usa temporalidad '1d' (diaria)")
    
    def ejecutar(self):
        """Ejecuta el flujo completo del programa"""
        self.mostrar_banner()
        
        # Instalar dependencias
        if not self.instalar_dependencias():
            print("\n✗ Error al instalar dependencias. Saliendo...")
            return
        
        # Configurar
        self.seleccionar_tipo_descarga()
        self.configurar_fechas()
        
        if self.tipo_descarga == 'forex':
            self.configurar_instrumentos_forex()
        else:
            self.configurar_instrumentos_indices()
        
        self.configurar_temporalidad()
        self.configurar_ruta_guardado()
        
        # Confirmar y descargar
        if self.mostrar_resumen():
            if self.tipo_descarga == 'forex':
                self.descargar_forex()
            else:
                self.descargar_indices()
            
            print("\n" + "="*60)
            print("✓ DESCARGA COMPLETADA")
            print("="*60)
            print(f"📁 Archivos guardados en: {self.ruta_guardado}")
        else:
            print("\n✗ Descarga cancelada por el usuario")

def main():
    try:
        downloader = DataDownloader()
        downloader.ejecutar()
    except KeyboardInterrupt:
        print("\n\n✗ Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()