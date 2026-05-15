import sys
import os


ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)
sys.path.append(os.path.join(ruta_raiz, 'src'))

from model.usuario import Usuario
from controller.usuario_controller import UsuarioController

usuario = Usuario(id_usuario=0, nombre="", email="")

print("Por favor ingrese los datos del usuario que desea crear")

usuario.nombre = input("Nombre : ")
usuario.email = input("Email : ")

UsuarioController.insertar(usuario)

print("¡Usuario insertado correctamente!")