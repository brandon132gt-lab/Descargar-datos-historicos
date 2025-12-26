# Descargar-datos-historicos

# 📈 Descargador de Datos Históricos (Forex & Stocks)


**¿Cansado de pagar por datos de mercado o usar data sucia de tu bróker?**

Este repositorio contiene una herramienta automatizada ("El Recolector") diseñada para descargar millones de datos financieros históricos de alta calidad totalmente **GRATIS**. Es ideal para Traders, Quants y desarrolladores que necesitan data confiable para Backtesting en MetaTrader, TradingView o Python.

## 🚀 Características Principales

* **Forex de Alta Precisión:** Descarga datos reales de **Dukascopy**, incluyendo **Tick Data** (movimiento milimétrico del precio) y velas temporales (M1, H1, D1).
* **Mercado de Valores:** Conexión directa con **Yahoo Finance** para descargar Acciones (Apple, Tesla), Índices (S&P500, NASDAQ) y Criptomonedas.
* **Instalación Inteligente:** No necesitas ser experto. El script detecta si te faltan librerías (como `pandas`, `yfinance` o `duka`) y las instala automáticamente por ti.
* **Sistema "Fail-Safe":** Si la descarga de Forex falla con un proveedor, el script intenta automáticamente una ruta de respaldo para asegurar que obtengas los datos.
* **Formato Universal:** Todo se exporta a archivos `.CSV` limpios y listos para usar.

## 📋 Requisitos Previos

* Tener instalado **Python 3** en tu computadora.
* Conexión a internet estable.

## 🛠️ Instalación y Uso

1.  **Clona el repositorio** o descarga el archivo ZIP (botón verde "Code" -> "Download ZIP").
    ```bash
    git clone [https://github.com/brandon132gt-lab/Descargar-datos-historicos.git](https://github.com/brandon132gt-lab/Descargar-datos-historicos.git)
    ```

2.  **Entra en la carpeta** del proyecto.

3.  **Ejecuta el script**:
    ```bash
    python descargar_pro.py
    ```
    *(Nota: La primera vez puede tardar unos segundos mientras instala las dependencias necesarias).*

## 🎮 Guía Rápida del Menú

Una vez inicies el programa, verás un menú interactivo:

1.  **Selecciona el Tipo:** Elige entre Forex (1) o Índices/Acciones (2).
2.  **Fechas:** Ingresa la fecha de inicio (formato `YYYY-MM-DD`).
3.  **Activos:**
    * Puedes elegir de la lista predefinida (ej: EURUSD, S&P500).
    * O escribir el símbolo manual (ej: `BTC-USD` para Bitcoin).
4.  **Temporalidad:** El script te avisará qué temporalidades están permitidas según el rango de fechas para evitar errores.

## 📂 Estructura de Archivos

Los datos se guardarán automáticamente en carpetas organizadas:
* `/datos_forex`: Para divisas.
* `/datos_indices`: Para acciones e índices.

## ⚠️ Disclaimer

Este software es para fines educativos y de investigación. El trading conlleva riesgos significativos. Asegúrate de verificar la integridad de los datos antes de utilizarlos con dinero real.

---
*Desarrollado con ❤️ para la comunidad de Trading Algorítmico.*
