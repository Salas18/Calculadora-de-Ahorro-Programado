from flask import Blueprint, render_template, request
from src.controller.ahorro_controller import AhorroController
from src.controller.usuario_controller import UsuarioController
from src.model.meta_ahorro import MetaAhorro


web_bp = Blueprint('web', __name__, template_folder='templates')


@web_bp.route('/')
def inicio():
    return render_template('index.html')

@web_bp.route('/crear-tablas')
def crear_tablas():
    try:
        UsuarioController.crear_tablas()
        return "✅ Tablas creadas exitosamente en Render. <br><br> <a href='/'>Volver al inicio</a>"
    except Exception as e:
        return f"❌ Error al crear tablas: {e}"

@web_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    mensaje = None
    if request.method == 'POST':
        try:
            id_usuario = int(request.form['id_usuario'])
            meta = float(request.form['meta'])
            plazo = int(request.form['plazo'])
            extra = float(request.form['extra'])
            mes_extra = int(request.form['mes_extra'])

            # Usamos TU mismo modelo y controlador
            nueva_meta = MetaAhorro(id_usuario, meta, plazo, extra, mes_extra)
            AhorroController.insertar_ahorro(nueva_meta)
            
            mensaje = "✅ ¡Meta de ahorro guardada con éxito en la nube!"
        except Exception as e:
            mensaje = f"❌ Error al guardar: {e}"
            
    return render_template('insertar.html', mensaje=mensaje)

@web_bp.route('/buscar', methods=['GET', 'POST'])
def buscar():
    meta_encontrada = None
    mensaje = None
    
    if request.method == 'POST':
        try:
            id_buscar = int(request.form['id_meta'])
            
            meta_encontrada = AhorroController.buscar_meta(id_buscar)
            
            if not meta_encontrada:
                mensaje = "No hay ninguna meta guardada con ese ID."
        except Exception as e:
            mensaje = f"Error al buscar: {e}"
            
    return render_template('buscar.html', meta_encontrada=meta_encontrada, mensaje=mensaje)