import sys
import os
#sys.path.append("src")

from core.logica import (
    AhorroProgramado,
    ErrorMetaInvalida,
    ErrorPlazoInvalido,
    ErrorAbonoInvalido,
    ErrorAbonoSuperaMeta,
    ErrorMesExtraFueraDeRango
)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image as KivyImage
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
from kivy.config import Config

if not os.environ.get('ANDROID_APP_PATH'):
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '600')

# Ruta base del archivo actual
BASE_DIR = os.path.dirname(__file__)

# Registrar Times New Roman de forma multiplataforma
RUTAS_FUENTE = [
    "C:/Windows/Fonts/times.ttf",           # Windows
    "/usr/share/fonts/msttcorefonts/Times_New_Roman.ttf",  # Linux
    "/Library/Fonts/Times New Roman.ttf",   # macOS
]

fuente_encontrada = next((r for r in RUTAS_FUENTE if os.path.exists(r)), None)

if fuente_encontrada:
    LabelBase.register(name="TimesNewRoman", fn_regular=fuente_encontrada)
    FUENTE = "TimesNewRoman"
else:
    FUENTE = "Roboto"  # fuente por defecto de Kivy si no encuentra Times New Roman

# Ruta de la imagen de error relativa al archivo
RUTA_ERROR = os.path.join(BASE_DIR, "error.png")

# Paleta de colores
COLOR_FONDO       = (0.95, 0.95, 0.92, 1)
COLOR_TEXTO       = (0.15, 0.15, 0.25, 1)
COLOR_BOTON       = (0.2, 0.45, 0.75, 1)
COLOR_BOTON_TEXTO = (1, 1, 1, 1)
COLOR_RESULTADO   = (0.1, 0.45, 0.2, 1)
COLOR_INFO        = (0.35, 0.35, 0.5, 1)

TAMAÑO_TITULO = 28
TAMAÑO_NORMAL = 18
TAMAÑO_BOTON  = 20


def crear_label(texto, color=COLOR_TEXTO, bold=False, tamaño=TAMAÑO_NORMAL):
    return Label(
        text=texto,
        color=color,
        bold=bold,
        font_size=tamaño,
        font_name=FUENTE
    )


def crear_input(hint):
    return TextInput(
        hint_text=hint,
        multiline=False,
        background_color=(1, 1, 1, 1),
        foreground_color=(0.1, 0.1, 0.2, 1),
        hint_text_color=(0.6, 0.6, 0.7, 1),
        cursor_color=(0.1, 0.1, 0.3, 1),
        padding=[12, 10],
        font_size=TAMAÑO_NORMAL,
        font_name=FUENTE
    )


class CalculadoraAhorroGUI(App):

    def build(self):
        self.title = "Calculadora de Ahorro Programado"

        raiz = BoxLayout(orientation="vertical", padding=25, spacing=18)

        with raiz.canvas.before:
            Color(*COLOR_FONDO)
            self.rect = Rectangle(size=raiz.size, pos=raiz.pos)

        raiz.bind(size=self._actualizar_fondo, pos=self._actualizar_fondo)

        raiz.add_widget(crear_label(
            "Calculadora de Ahorro Programado",
            color=(0.1, 0.3, 0.65, 1),
            bold=True,
            tamaño=TAMAÑO_TITULO
        ))

        raiz.add_widget(crear_label(
            "Calcula el ahorro mensual necesario para alcanzar tu meta,\n"
            "teniendo en cuenta un abono extra opcional.",
            color=COLOR_INFO
        ))

        formulario = GridLayout(cols=2, spacing=12, size_hint_y=None, height=280)

        formulario.add_widget(crear_label("Meta de ahorro ($):"))
        self.meta_input = crear_input("Ej: 5000000")
        formulario.add_widget(self.meta_input)

        formulario.add_widget(crear_label("Plazo en meses:"))
        self.plazo_input = crear_input("Ej: 12")
        formulario.add_widget(self.plazo_input)

        formulario.add_widget(crear_label("Abono extra ($):"))
        self.abono_input = crear_input("0 si no hay")
        formulario.add_widget(self.abono_input)

        formulario.add_widget(crear_label("Mes del abono extra:"))
        self.mes_abono_input = crear_input("0 si no hay")
        formulario.add_widget(self.mes_abono_input)

        raiz.add_widget(formulario)

        boton = Button(
            text="Calcular Ahorro",
            background_color=COLOR_BOTON,
            color=COLOR_BOTON_TEXTO,
            font_size=TAMAÑO_BOTON,
            font_name=FUENTE,
            bold=True,
            size_hint_y=None,
            height=60
        )
        boton.bind(on_press=self.calcular_ahorro)
        raiz.add_widget(boton)

        self.resultado_label = crear_label("", color=COLOR_RESULTADO, bold=True)
        raiz.add_widget(self.resultado_label)

        return raiz

    def _actualizar_fondo(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos  = instance.pos

    def calcular_ahorro(self, sender):
        try:
            meta        = float(self.meta_input.text)
            plazo       = int(self.plazo_input.text)
            abono_extra = float(self.abono_input.text)
            mes_abono   = int(self.mes_abono_input.text)

            ahorro    = AhorroProgramado(meta=meta, plazo=plazo, abono_extra=abono_extra, mes_abono_extra=mes_abono)
            resultado = ahorro.calcular_cuota_mensual()

            self.resultado_label.text = f"Ahorro mensual necesario: ${resultado:,.2f}"

        except (ErrorMetaInvalida, ErrorPlazoInvalido, ErrorAbonoInvalido,
                ErrorAbonoSuperaMeta, ErrorMesExtraFueraDeRango) as e:
            self._mostrar_error(str(e))

        except ValueError:
            self._mostrar_error("Todos los campos deben ser valores numéricos.")

    def _mostrar_error(self, mensaje):
        modal = ModalView(size_hint=(0.85, 0.65), auto_dismiss=False)

        contenido = BoxLayout(orientation="vertical", padding=20, spacing=15)

        with contenido.canvas.before:
            Color(*COLOR_FONDO)
            rect_fondo = Rectangle(size=contenido.size, pos=contenido.pos)

        contenido.bind(
            size=lambda i, v: setattr(rect_fondo, 'size', v),
            pos=lambda i, v: setattr(rect_fondo, 'pos', v)
        )

        encabezado = BoxLayout(orientation="horizontal", size_hint_y=None, height=45, padding=[10, 5])

        with encabezado.canvas.before:
            Color(*COLOR_BOTON)
            rect_enc = Rectangle(size=encabezado.size, pos=encabezado.pos)

        encabezado.bind(
            size=lambda i, v: setattr(rect_enc, 'size', v),
            pos=lambda i, v: setattr(rect_enc, 'pos', v)
        )

        encabezado.add_widget(Label(
            text="Error de validación",
            color=(1, 1, 1, 1),
            font_size=20,
            font_name=FUENTE,
            bold=True,
            halign="left",
            valign="middle"
        ))

        contenido.add_widget(encabezado)

        if os.path.exists(RUTA_ERROR):
            contenido.add_widget(KivyImage(
                source=RUTA_ERROR,
                size_hint=(1, None),
                height=180,
                allow_stretch=True,
                keep_ratio=True
            ))

        contenido.add_widget(Label(
            text=mensaje,
            color=(0, 0, 0, 1),
            font_size=26,
            font_name=FUENTE,
            bold=True,
            text_size=(520, None),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=100
        ))

        boton_cerrar = Button(
            text="Cerrar",
            size_hint=(0.5, None),
            pos_hint={"center_x": 0.5},
            height=55,
            background_color=COLOR_BOTON,
            color=COLOR_BOTON_TEXTO,
            font_size=20,
            font_name=FUENTE,
            bold=True
        )

        boton_cerrar.bind(on_press=modal.dismiss)
        contenido.add_widget(boton_cerrar)

        modal.add_widget(contenido)
        modal.open()


if __name__ == "__main__":
    CalculadoraAhorroGUI().run()
