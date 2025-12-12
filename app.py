from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
from config import Config

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Función para conectar a la base de datos
def get_db_connection():
    import os        #borrar si da errores, es por railway
    import tempfile    #borrar si da errores, es por railway

    db_path = os.path.join(tempfile.gettempdir(), 'proyectos.db')
    conn = sqlite3.connect(db_path)
    
    #conn = sqlite3.connect(':memory:') # para arrancar en Railway
    #conn = sqlite3.connect(app.config['DATABASE_PATH']) # para arrancar en local original esto y el de abajo
    conn.row_factory = sqlite3.Row  # Para obtener diccionarios en lugar de tuplas
    return conn


# Crear tablas de la base de datos si no existen
def init_db():
    conn = get_db_connection()
    
    # Tabla de proyectos (como tu PRIMERA FASE en Excel)
    conn.execute('''
CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo_actividad TEXT,
    tiene_inversion INTEGER DEFAULT 0,
    valor_inversion REAL DEFAULT 0,
    tasa_descuento REAL DEFAULT 0.001,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
    
    # En la función init_db(), después de la tabla de proyectos, añade:
    conn.execute('''
    CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id INTEGER,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    )
    ''')
    
    # Tabla de costos por producto (cada costo asociado a un producto específico)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS costos_productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        nombre TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY (producto_id) REFERENCES productos (id)
    )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS costos_generales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER,
        nombre TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    )
    ''')
    
    # Tabla de costos (como tu SEGUNDA FASE - Costos)
    # conn.execute('''
    # CREATE TABLE IF NOT EXISTS costos (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     proyecto_id INTEGER,
    #     nombre TEXT NOT NULL,
    #     valor REAL NOT NULL,
    #     FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    # )
    # ''')
    
    # Modificar la tabla de costos para que incluya producto_id
    
    
    # conn.execute('''
    # CREATE TABLE IF NOT EXISTS costos (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     proyecto_id INTEGER,
    #     producto_id INTEGER,
    #     nombre TEXT NOT NULL,
    #     valor REAL NOT NULL,
    #     FOREIGN KEY (proyecto_id) REFERENCES proyectos (id),
    #     FOREIGN KEY (producto_id) REFERENCES productos (id)
    # )
    # ''')
    
    # Tabla de gastos (como tu SEGUNDA FASE - Gastos)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER,
        nombre TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    )
    ''')
    
    # Tabla de personal (como tu TERCERA FASE - Viabilidad Operativa)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS personal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER,
        nombre TEXT NOT NULL,
        perfil TEXT,
        salario_mensual REAL NOT NULL,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    )
    ''')
    
    # Tabla de materiales (como tu Equipo y maquinaria)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS materiales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER,
        nombre TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    )
    ''')
    
    # Tabla para ventas por día
    conn.execute('''
    CREATE TABLE IF NOT EXISTS ventas_dias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER,
        lunes INTEGER DEFAULT 0,
        martes INTEGER DEFAULT 0,
        miercoles INTEGER DEFAULT 0,
        jueves INTEGER DEFAULT 0,
        viernes INTEGER DEFAULT 0,
        sabado INTEGER DEFAULT 0,
        domingo INTEGER DEFAULT 0,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    )
    ''')
    
    # Tabla para ventas por semana
    conn.execute('''
    CREATE TABLE IF NOT EXISTS ventas_semanas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER,
        semana1 INTEGER DEFAULT 0,
        semana2 INTEGER DEFAULT 0,
        semana3 INTEGER DEFAULT 0,
        semana4 INTEGER DEFAULT 0,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    )
    ''')
    
    # Tabla para ventas por mes
    conn.execute('''
    CREATE TABLE IF NOT EXISTS ventas_meses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER,
        enero INTEGER DEFAULT 0,
        febrero INTEGER DEFAULT 0,
        marzo INTEGER DEFAULT 0,
        abril INTEGER DEFAULT 0,
        mayo INTEGER DEFAULT 0,
        junio INTEGER DEFAULT 0,
        julio INTEGER DEFAULT 0,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    )
    ''')
    
    # Tabla para ventas por año
    conn.execute('''
    CREATE TABLE IF NOT EXISTS ventas_anos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER,
        año1 INTEGER DEFAULT 0,
        año2 INTEGER DEFAULT 0,
        año3 INTEGER DEFAULT 0,
        año4 INTEGER DEFAULT 0,
        año5 INTEGER DEFAULT 0,
        año6 INTEGER DEFAULT 0,
        año7 INTEGER DEFAULT 0,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
    )
    ''')
    
    # Tabla para ingresos por día (igual que ventas_dias)
    conn.execute('''
CREATE TABLE IF NOT EXISTS ingresos_dias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id INTEGER,
    lunes REAL DEFAULT 0,
    martes REAL DEFAULT 0,
    miercoles REAL DEFAULT 0,
    jueves REAL DEFAULT 0,
    viernes REAL DEFAULT 0,
    sabado REAL DEFAULT 0,
    domingo REAL DEFAULT 0,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
)
''')

# Tabla para ingresos por semana (igual que ventas_semanas)
    conn.execute('''
CREATE TABLE IF NOT EXISTS ingresos_semanas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id INTEGER,
    semana1 REAL DEFAULT 0,
    semana2 REAL DEFAULT 0,
    semana3 REAL DEFAULT 0,
    semana4 REAL DEFAULT 0,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
)
''')

# Tabla para ingresos por mes (igual que ventas_meses)
    conn.execute('''
CREATE TABLE IF NOT EXISTS ingresos_meses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id INTEGER,
    enero REAL DEFAULT 0,
    febrero REAL DEFAULT 0,
    marzo REAL DEFAULT 0,
    abril REAL DEFAULT 0,
    mayo REAL DEFAULT 0,
    junio REAL DEFAULT 0,
    julio REAL DEFAULT 0,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
)
''')

# Tabla para ingresos por año (igual que ventas_anos)
    conn.execute('''
CREATE TABLE IF NOT EXISTS ingresos_anos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id INTEGER,
    año1 REAL DEFAULT 0,
    año2 REAL DEFAULT 0,
    año3 REAL DEFAULT 0,
    año4 REAL DEFAULT 0,
    año5 REAL DEFAULT 0,
    año6 REAL DEFAULT 0,
    año7 REAL DEFAULT 0,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
)
''')
    # En init_db(), añade estas tablas:
    conn.execute('''
CREATE TABLE IF NOT EXISTS utilidad_dias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id INTEGER,
    lunes REAL DEFAULT 0,
    martes REAL DEFAULT 0,
    miercoles REAL DEFAULT 0,
    jueves REAL DEFAULT 0,
    viernes REAL DEFAULT 0,
    sabado REAL DEFAULT 0,
    domingo REAL DEFAULT 0,
    total_semana REAL DEFAULT 0,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
)
''')

    conn.execute('''
CREATE TABLE IF NOT EXISTS utilidad_semanas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id INTEGER,
    semana1 REAL DEFAULT 0,
    semana2 REAL DEFAULT 0,
    semana3 REAL DEFAULT 0,
    semana4 REAL DEFAULT 0,
    total_mes REAL DEFAULT 0,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
)
''')

    conn.execute('''
CREATE TABLE IF NOT EXISTS utilidad_meses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id INTEGER,
    enero REAL DEFAULT 0,
    febrero REAL DEFAULT 0,
    marzo REAL DEFAULT 0,
    abril REAL DEFAULT 0,
    mayo REAL DEFAULT 0,
    junio REAL DEFAULT 0,
    julio REAL DEFAULT 0,
    total_periodo REAL DEFAULT 0,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
)
''')

    conn.execute('''
CREATE TABLE IF NOT EXISTS utilidad_anos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proyecto_id INTEGER,
    año1 REAL DEFAULT 0,
    año2 REAL DEFAULT 0,
    año3 REAL DEFAULT 0,
    año4 REAL DEFAULT 0,
    año5 REAL DEFAULT 0,
    año6 REAL DEFAULT 0,
    año7 REAL DEFAULT 0,
    total_7anos REAL DEFAULT 0,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
)
''')
    
    conn.commit()
    conn.close()

# Llamar a init_db al iniciar la aplicación
with app.app_context():
    init_db()

# ==================== RUTAS PRINCIPALES ====================

@app.route('/')
def index():
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    
    return render_template('index.html', proyecto=proyecto)

@app.route('/proyecto/datos-iniciales', methods=['GET', 'POST'])
def datos_iniciales():
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo_actividad = request.form.get('tipo_actividad')
        tiene_inversion = 1 if request.form.get('tiene_inversion') == 'si' else 0
        valor_inversion = float(request.form.get('valor_inversion', 0))
        tasa_descuento = float(request.form.get('tasa_descuento', 0.001))
        
        proyecto_existente = conn.execute('SELECT * FROM proyectos').fetchone()
        
        if proyecto_existente:
            conn.execute('''
                UPDATE proyectos SET 
                nombre = ?, tipo_actividad = ?, tiene_inversion = ?, 
                valor_inversion = ?, tasa_descuento = ?
                WHERE id = ?
            ''', (nombre, tipo_actividad, tiene_inversion, valor_inversion, 
                  tasa_descuento, proyecto_existente['id']))
            flash('Proyecto actualizado correctamente', 'success')
        else:
            conn.execute('''
                INSERT INTO proyectos 
                (nombre, tipo_actividad, tiene_inversion, valor_inversion, 
                 tasa_descuento)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, tipo_actividad, tiene_inversion, valor_inversion, 
                  tasa_descuento))
            flash('Proyecto creado correctamente', 'success')
        
        conn.commit()
    
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    # Obtener productos si hay proyecto
    productos = []
    total_productos = 0
    if proyecto:
        productos = conn.execute('SELECT * FROM productos WHERE proyecto_id = ? ORDER BY id', 
                               (proyecto['id'],)).fetchall()
        total_productos_result = conn.execute('SELECT SUM(precio) as total FROM productos WHERE proyecto_id = ?', 
                                            (proyecto['id'],)).fetchone()
        total_productos = total_productos_result['total'] or 0 if total_productos_result else 0
    
    conn.close()
    
    return render_template('proyecto/datos_iniciales.html', 
                         proyecto=proyecto,
                         productos=productos,
                         total_productos=total_productos)

# ==================== FUNCIONES PARA PRODUCTOS ====================

@app.route('/proyecto/agregar-producto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre_producto')
        precio = float(request.form.get('precio_producto', 0))
        
        conn = get_db_connection()
        proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
        
        if proyecto:
            conn.execute('INSERT INTO productos (proyecto_id, nombre, precio) VALUES (?, ?, ?)',
                        (proyecto['id'], nombre, precio))
            conn.commit()
            flash(f'Producto "{nombre}" agregado correctamente', 'success')
        else:
            flash('Primero debes crear un proyecto', 'warning')
        
        conn.close()
    
    return redirect(url_for('datos_iniciales'))

@app.route('/proyecto/editar-producto/<int:id>', methods=['POST'])
def editar_producto(id):
    if request.method == 'POST':
        nombre = request.form.get('nombre_producto')
        precio = float(request.form.get('precio_producto', 0))
        
        conn = get_db_connection()
        conn.execute('UPDATE productos SET nombre = ?, precio = ? WHERE id = ?',
                    (nombre, precio, id))
        conn.commit()
        conn.close()
        
        flash(f'Producto actualizado correctamente', 'success')
    
    return redirect(url_for('datos_iniciales'))

@app.route('/proyecto/eliminar-producto/<int:id>')
def eliminar_producto(id):
    conn = get_db_connection()
    
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    if producto:
        # También eliminar los costos asociados a este producto
        conn.execute('DELETE FROM costos_productos WHERE producto_id = ?', (id,))
        conn.execute('DELETE FROM productos WHERE id = ?', (id,))
        conn.commit()
        flash(f'Producto "{producto["nombre"]}" eliminado correctamente', 'success')
    
    conn.close()
    return redirect(url_for('datos_iniciales'))

# ==================== VIABILIDAD TÉCNICA ====================

# ==================== VIABILIDAD TÉCNICA ====================

@app.route('/proyecto/viabilidad-tecnica')
def viabilidad_tecnica():
    conn = get_db_connection()
    
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    # Obtener productos
    productos = []
    if proyecto:
        productos = conn.execute('SELECT * FROM productos WHERE proyecto_id = ? ORDER BY id', 
                               (proyecto['id'],)).fetchall()
    
    # Costos generales
    costos_generales = []
    total_costos_generales = 0
    if proyecto:
        costos_generales = conn.execute('SELECT * FROM costos_generales WHERE proyecto_id = ? ORDER BY id', 
                                       (proyecto['id'],)).fetchall()
        total_costos_generales_result = conn.execute('SELECT SUM(valor) as total FROM costos_generales WHERE proyecto_id = ?', 
                                                   (proyecto['id'],)).fetchone()
        total_costos_generales = total_costos_generales_result['total'] or 0 if total_costos_generales_result else 0
    
    # Costos por producto
    costos_por_producto = {}
    total_costos_productos = 0
    if productos:
        for producto in productos:
            costos_producto = conn.execute('SELECT * FROM costos_productos WHERE producto_id = ? ORDER BY id', 
                                         (producto['id'],)).fetchall()
            
            # Calcular total por producto
            total_producto_result = conn.execute('SELECT SUM(valor) as total FROM costos_productos WHERE producto_id = ?', 
                                               (producto['id'],)).fetchone()
            total_producto = total_producto_result['total'] or 0 if total_producto_result else 0
            
            costos_por_producto[producto['id']] = {
                'producto': producto,
                'costos': costos_producto,
                'total': total_producto
            }
            
            total_costos_productos += total_producto
    
    gastos = []
    total_gastos = 0
    if proyecto:
        gastos = conn.execute('SELECT * FROM gastos WHERE proyecto_id = ? ORDER BY id', 
                             (proyecto['id'],)).fetchall()
        total_gastos_result = conn.execute('SELECT SUM(valor) as total FROM gastos WHERE proyecto_id = ?', 
                                         (proyecto['id'],)).fetchone()
        total_gastos = total_gastos_result['total'] or 0 if total_gastos_result else 0
    
    conn.close()
    
    return render_template('proyecto/viabilidad_tecnica.html', 
                         proyecto=proyecto,
                         productos=productos,
                         costos_generales=costos_generales,
                         total_costos_generales=total_costos_generales,
                         costos_por_producto=costos_por_producto,
                         total_costos_productos=total_costos_productos,
                         gastos=gastos,
                         total_gastos=total_gastos)
# Nueva función para agregar costo a un producto específico
# ==================== COSTOS POR PRODUCTO ====================

@app.route('/proyecto/agregar-costo-producto/<int:producto_id>', methods=['POST'])
def agregar_costo_producto(producto_id):
    if request.method == 'POST':
        nombre = request.form.get('nombre_costo_producto')
        valor = float(request.form.get('valor_costo_producto', 0))
        
        conn = get_db_connection()
        
        # Verificar que el producto existe
        producto = conn.execute('SELECT * FROM productos WHERE id = ?', (producto_id,)).fetchone()
        if producto:
            conn.execute('INSERT INTO costos_productos (producto_id, nombre, valor) VALUES (?, ?, ?)',
                        (producto_id, nombre, valor))
            conn.commit()
            flash(f'Costo para "{producto["nombre"]}" agregado correctamente', 'success')
        else:
            flash('Producto no encontrado', 'error')
        
        conn.close()
    
    return redirect(url_for('viabilidad_tecnica'))

@app.route('/proyecto/editar-costo-producto/<int:id>', methods=['POST'])
def editar_costo_producto(id):
    if request.method == 'POST':
        nombre = request.form.get('nombre_costo_producto')
        valor = float(request.form.get('valor_costo_producto', 0))
        
        conn = get_db_connection()
        conn.execute('UPDATE costos_productos SET nombre = ?, valor = ? WHERE id = ?',
                    (nombre, valor, id))
        conn.commit()
        conn.close()
        
        flash(f'Costo por producto actualizado correctamente', 'success')
    
    return redirect(url_for('viabilidad_tecnica'))

@app.route('/proyecto/eliminar-costo-producto/<int:id>')
def eliminar_costo_producto(id):
    conn = get_db_connection()
    
    costo = conn.execute('SELECT * FROM costos_productos WHERE id = ?', (id,)).fetchone()
    if costo:
        conn.execute('DELETE FROM costos_productos WHERE id = ?', (id,))
        conn.commit()
        flash(f'Costo por producto eliminado correctamente', 'success')
    
    conn.close()
    return redirect(url_for('viabilidad_tecnica'))

@app.route('/proyecto/agregar-costo', methods=['POST'])
def agregar_costo():
    if request.method == 'POST':
        nombre = request.form.get('nombre_costo')
        valor = float(request.form.get('valor_costo', 0))
        
        conn = get_db_connection()
        proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
        
        if proyecto:
            conn.execute('INSERT INTO costos_generales (proyecto_id, nombre, valor) VALUES (?, ?, ?)',
                        (proyecto['id'], nombre, valor))
            conn.commit()
            flash(f'Costo general "{nombre}" agregado correctamente', 'success')
        else:
            flash('Primero debes crear un proyecto', 'warning')
        
        conn.close()
    
    return redirect(url_for('viabilidad_tecnica'))

@app.route('/proyecto/editar-costo/<int:id>', methods=['POST'])
def editar_costo(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre_costo')
        valor = float(request.form.get('valor_costo', 0))
        
        conn.execute('UPDATE costos_generales SET nombre = ?, valor = ? WHERE id = ?',
                    (nombre, valor, id))
        conn.commit()
        conn.close()
        
        flash(f'Costo general actualizado correctamente', 'success')
        return redirect(url_for('viabilidad_tecnica'))
    
    costo = conn.execute('SELECT * FROM costos_generales WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if not costo:
        flash('Costo no encontrado', 'error')
        return redirect(url_for('viabilidad_tecnica'))
    
    return render_template('componentes/modal_editar_costo.html', costo=costo)

@app.route('/proyecto/eliminar-costo/<int:id>')
def eliminar_costo(id):
    conn = get_db_connection()
    
    costo = conn.execute('SELECT * FROM costos_generales WHERE id = ?', (id,)).fetchone()
    if costo:
        conn.execute('DELETE FROM costos_generales WHERE id = ?', (id,))
        conn.commit()
        flash(f'Costo general "{costo["nombre"]}" eliminado correctamente', 'success')
    
    conn.close()
    return redirect(url_for('viabilidad_tecnica'))

# @app.route('/proyecto/viabilidad-tecnica')
# def viabilidad_tecnica():
#     conn = get_db_connection()
    
#     proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
#     costos = []
#     total_costos = 0
#     if proyecto:
#         costos = conn.execute('SELECT * FROM costos WHERE proyecto_id = ? ORDER BY id', 
#                              (proyecto['id'],)).fetchall()
#         total_costos_result = conn.execute('SELECT SUM(valor) as total FROM costos WHERE proyecto_id = ?', 
#                                          (proyecto['id'],)).fetchone()
#         total_costos = total_costos_result['total'] or 0 if total_costos_result else 0
    
#     gastos = []
#     total_gastos = 0
#     if proyecto:
#         gastos = conn.execute('SELECT * FROM gastos WHERE proyecto_id = ? ORDER BY id', 
#                              (proyecto['id'],)).fetchall()
#         total_gastos_result = conn.execute('SELECT SUM(valor) as total FROM gastos WHERE proyecto_id = ?', 
#                                          (proyecto['id'],)).fetchone()
#         total_gastos = total_gastos_result['total'] or 0 if total_gastos_result else 0
    
#     conn.close()
    
#     return render_template('proyecto/viabilidad_tecnica.html', 
#                          proyecto=proyecto, 
#                          costos=costos, 
#                          gastos=gastos,
#                          total_costos=total_costos,
#                          total_gastos=total_gastos)

# @app.route('/proyecto/agregar-costo', methods=['POST'])
# def agregar_costo():
#     if request.method == 'POST':
#         nombre = request.form.get('nombre_costo')
#         valor = float(request.form.get('valor_costo', 0))
        
#         conn = get_db_connection()
#         proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
        
#         if proyecto:
#             conn.execute('INSERT INTO costos (proyecto_id, nombre, valor) VALUES (?, ?, ?)',
#                         (proyecto['id'], nombre, valor))
#             conn.commit()
#             flash(f'Costo "{nombre}" agregado correctamente', 'success')
#         else:
#             flash('Primero debes crear un proyecto', 'warning')
        
#         conn.close()
    
#     return redirect(url_for('viabilidad_tecnica'))

# @app.route('/proyecto/editar-costo/<int:id>', methods=['GET', 'POST'])
# def editar_costo(id):
#     conn = get_db_connection()
    
#     if request.method == 'POST':
#         nombre = request.form.get('nombre_costo')
#         valor = float(request.form.get('valor_costo', 0))
        
#         conn.execute('UPDATE costos SET nombre = ?, valor = ? WHERE id = ?',
#                     (nombre, valor, id))
#         conn.commit()
#         conn.close()
        
#         flash(f'Costo actualizado correctamente', 'success')
#         return redirect(url_for('viabilidad_tecnica'))
    
#     costo = conn.execute('SELECT * FROM costos WHERE id = ?', (id,)).fetchone()
#     conn.close()
    
#     if not costo:
#         flash('Costo no encontrado', 'error')
#         return redirect(url_for('viabilidad_tecnica'))
    
#     return render_template('componentes/modal_editar_costo.html', costo=costo)

# @app.route('/proyecto/eliminar-costo/<int:id>')
# def eliminar_costo(id):
#     conn = get_db_connection()
    
#     costo = conn.execute('SELECT * FROM costos WHERE id = ?', (id,)).fetchone()
#     if costo:
#         conn.execute('DELETE FROM costos WHERE id = ?', (id,))
#         conn.commit()
#         flash(f'Costo "{costo["nombre"]}" eliminado correctamente', 'success')
    
#     conn.close()
#     return redirect(url_for('viabilidad_tecnica'))

@app.route('/proyecto/agregar-gasto', methods=['POST'])
def agregar_gasto():
    if request.method == 'POST':
        nombre = request.form.get('nombre_gasto')
        valor = float(request.form.get('valor_gasto', 0))
        
        conn = get_db_connection()
        proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
        
        if proyecto:
            conn.execute('INSERT INTO gastos (proyecto_id, nombre, valor) VALUES (?, ?, ?)',
                        (proyecto['id'], nombre, valor))
            conn.commit()
            flash(f'Gasto "{nombre}" agregado correctamente', 'success')
        else:
            flash('Primero debes crear un proyecto', 'warning')
        
        conn.close()
    
    return redirect(url_for('viabilidad_tecnica'))

@app.route('/proyecto/editar-gasto/<int:id>', methods=['GET', 'POST'])
def editar_gasto(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre_gasto')
        valor = float(request.form.get('valor_gasto', 0))
        
        conn.execute('UPDATE gastos SET nombre = ?, valor = ? WHERE id = ?',
                    (nombre, valor, id))
        conn.commit()
        conn.close()
        
        flash(f'Gasto actualizado correctamente', 'success')
        return redirect(url_for('viabilidad_tecnica'))
    
    gasto = conn.execute('SELECT * FROM gastos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if not gasto:
        flash('Gasto no encontrado', 'error')
        return redirect(url_for('viabilidad_tecnica'))
    
    return render_template('componentes/modal_editar_gasto.html', gasto=gasto)

@app.route('/proyecto/eliminar-gasto/<int:id>')
def eliminar_gasto(id):
    conn = get_db_connection()
    
    gasto = conn.execute('SELECT * FROM gastos WHERE id = ?', (id,)).fetchone()
    if gasto:
        conn.execute('DELETE FROM gastos WHERE id = ?', (id,))
        conn.commit()
        flash(f'Gasto "{gasto["nombre"]}" eliminado correctamente', 'success')
    
    conn.close()
    return redirect(url_for('viabilidad_tecnica'))

# ==================== VIABILIDAD OPERATIVA ====================

@app.route('/proyecto/viabilidad-operativa')
def viabilidad_operativa():
    conn = get_db_connection()
    
    # Obtener proyecto actual
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        conn.close()
        flash('Primero debes crear un proyecto', 'warning')
        return redirect(url_for('datos_iniciales'))
    
    # Obtener productos (opcional, para mostrar info)
    productos = []
    productos = conn.execute('SELECT * FROM productos WHERE proyecto_id = ? ORDER BY id', 
                           (proyecto['id'],)).fetchall()
    
    # Obtener personal
    personal = []
    total_salarios = 0
    personal = conn.execute('SELECT * FROM personal WHERE proyecto_id = ? ORDER BY id', 
                           (proyecto['id'],)).fetchall()
    
    total_salarios_result = conn.execute('SELECT SUM(salario_mensual) as total FROM personal WHERE proyecto_id = ?', 
                                       (proyecto['id'],)).fetchone()
    total_salarios = total_salarios_result['total'] or 0 if total_salarios_result else 0
    
    # Obtener costos generales (NO costos, es costos_generales)
    total_costos_generales = 0
    total_costos_result = conn.execute('SELECT SUM(valor) as total FROM costos_generales WHERE proyecto_id = ?', 
                                     (proyecto['id'],)).fetchone()
    total_costos_generales = total_costos_result['total'] or 0 if total_costos_result else 0
    
    # Obtener costos por producto
    total_costos_productos = 0
    if productos:
        for producto in productos:
            total_producto_result = conn.execute('SELECT SUM(valor) as total FROM costos_productos WHERE producto_id = ?', 
                                               (producto['id'],)).fetchone()
            total_producto = total_producto_result['total'] or 0 if total_producto_result else 0
            total_costos_productos += total_producto
    
    # Obtener gastos
    total_gastos = 0
    total_gastos_result = conn.execute('SELECT SUM(valor) as total FROM gastos WHERE proyecto_id = ?', 
                                     (proyecto['id'],)).fetchone()
    total_gastos = total_gastos_result['total'] or 0 if total_gastos_result else 0
    
    conn.close()
    
    # Calcular total general
    total_general = total_costos_generales + total_costos_productos + total_gastos + total_salarios
    
    return render_template('proyecto/viabilidad_operativa.html', 
                         proyecto=proyecto,
                         productos=productos,
                         personal=personal,
                         total_salarios=total_salarios,
                         total_costos_generales=total_costos_generales,
                         total_costos_productos=total_costos_productos,
                         total_gastos=total_gastos,
                         total_general=total_general)

@app.route('/proyecto/agregar-personal', methods=['POST'])
def agregar_personal():
    if request.method == 'POST':
        nombre = request.form.get('nombre_personal')
        perfil = request.form.get('perfil_personal')
        salario_mensual = float(request.form.get('salario_mensual', 0))
        
        conn = get_db_connection()
        proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
        
        if proyecto:
            conn.execute('INSERT INTO personal (proyecto_id, nombre, perfil, salario_mensual) VALUES (?, ?, ?, ?)',
                        (proyecto['id'], nombre, perfil, salario_mensual))
            conn.commit()
            flash(f'Personal "{nombre}" agregado correctamente', 'success')
        else:
            flash('Primero debes crear un proyecto', 'warning')
        
        conn.close()
    
    return redirect(url_for('viabilidad_operativa'))

@app.route('/proyecto/editar-personal/<int:id>', methods=['GET', 'POST'])
def editar_personal(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre_personal')
        perfil = request.form.get('perfil_personal')
        salario_mensual = float(request.form.get('salario_mensual', 0))
        
        conn.execute('UPDATE personal SET nombre = ?, perfil = ?, salario_mensual = ? WHERE id = ?',
                    (nombre, perfil, salario_mensual, id))
        conn.commit()
        conn.close()
        
        flash(f'Personal actualizado correctamente', 'success')
        return redirect(url_for('viabilidad_operativa'))
    
    persona = conn.execute('SELECT * FROM personal WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if not persona:
        flash('Personal no encontrado', 'error')
        return redirect(url_for('viabilidad_operativa'))
    
    return render_template('componentes/modal_editar_personal.html', persona=persona)

@app.route('/proyecto/eliminar-personal/<int:id>')
def eliminar_personal(id):
    conn = get_db_connection()
    
    persona = conn.execute('SELECT * FROM personal WHERE id = ?', (id,)).fetchone()
    if persona:
        conn.execute('DELETE FROM personal WHERE id = ?', (id,))
        conn.commit()
        flash(f'Personal "{persona["nombre"]}" eliminado correctamente', 'success')
    
    conn.close()
    return redirect(url_for('viabilidad_operativa'))

# ==================== EQUIPO Y MAQUINARIA ====================

@app.route('/proyecto/equipo-maquinaria')
def equipo_maquinaria():
    conn = get_db_connection()
    
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    materiales = []
    total_materiales = 0
    if proyecto:
        materiales = conn.execute('SELECT * FROM materiales WHERE proyecto_id = ? ORDER BY id', 
                                 (proyecto['id'],)).fetchall()
        total_materiales_result = conn.execute('SELECT SUM(valor) as total FROM materiales WHERE proyecto_id = ?', 
                                             (proyecto['id'],)).fetchone()
        total_materiales = total_materiales_result['total'] or 0 if total_materiales_result else 0
    
    total_costos = 0
    total_gastos = 0
    total_salarios = 0
    if proyecto:
        total_costos_result = conn.execute('SELECT SUM(valor) as total FROM costos WHERE proyecto_id = ?', 
                                         (proyecto['id'],)).fetchone()
        total_costos = total_costos_result['total'] or 0 if total_costos_result else 0
        
        total_gastos_result = conn.execute('SELECT SUM(valor) as total FROM gastos WHERE proyecto_id = ?', 
                                         (proyecto['id'],)).fetchone()
        total_gastos = total_gastos_result['total'] or 0 if total_gastos_result else 0
        
        total_salarios_result = conn.execute('SELECT SUM(salario_mensual) as total FROM personal WHERE proyecto_id = ?', 
                                           (proyecto['id'],)).fetchone()
        total_salarios = total_salarios_result['total'] or 0 if total_salarios_result else 0
    
    conn.close()
    
    return render_template('proyecto/equipo_maquinaria.html', 
                         proyecto=proyecto, 
                         materiales=materiales,
                         total_materiales=total_materiales,
                         total_costos=total_costos,
                         total_gastos=total_gastos,
                         total_salarios=total_salarios)

@app.route('/proyecto/agregar-material', methods=['POST'])
def agregar_material():
    if request.method == 'POST':
        nombre = request.form.get('nombre_material')
        valor = float(request.form.get('valor_material', 0))
        
        conn = get_db_connection()
        proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
        
        if proyecto:
            conn.execute('INSERT INTO materiales (proyecto_id, nombre, valor) VALUES (?, ?, ?)',
                        (proyecto['id'], nombre, valor))
            conn.commit()
            flash(f'Material "{nombre}" agregado correctamente', 'success')
        else:
            flash('Primero debes crear un proyecto', 'warning')
        
        conn.close()
    
    return redirect(url_for('equipo_maquinaria'))

@app.route('/proyecto/editar-material/<int:id>', methods=['GET', 'POST'])
def editar_material(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre_material')
        valor = float(request.form.get('valor_material', 0))
        
        conn.execute('UPDATE materiales SET nombre = ?, valor = ? WHERE id = ?',
                    (nombre, valor, id))
        conn.commit()
        conn.close()
        
        flash(f'Material actualizado correctamente', 'success')
        return redirect(url_for('equipo_maquinaria'))
    
    material = conn.execute('SELECT * FROM materiales WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if not material:
        flash('Material no encontrado', 'error')
        return redirect(url_for('equipo_maquinaria'))
    
    return render_template('componentes/modal_editar_material.html', material=material)

@app.route('/proyecto/eliminar-material/<int:id>')
def eliminar_material(id):
    conn = get_db_connection()
    
    material = conn.execute('SELECT * FROM materiales WHERE id = ?', (id,)).fetchone()
    if material:
        conn.execute('DELETE FROM materiales WHERE id = ?', (id,))
        conn.commit()
        flash(f'Material "{material["nombre"]}" eliminado correctamente', 'success')
    
    conn.close()
    return redirect(url_for('equipo_maquinaria'))

# ==================== FLUJOS DE CAJA ====================

@app.route('/proyecto/flujos-caja')
def flujos_caja():
    conn = get_db_connection()
    
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    totales = {
        'costos': 0,
        'gastos': 0,
        'salarios': 0,
        'materiales': 0
    }
    
    ventas_dias = None
    ventas_semanas = None
    ventas_meses = None
    ventas_anos = None
    
    # Obtener INGRESOS (nuevo)
    ingresos_dias = None
    ingresos_semanas = None
    ingresos_meses = None
    ingresos_anos = None

    
    if proyecto:
        # Costos
        total_costos_result = conn.execute('SELECT SUM(valor) as total FROM costos WHERE proyecto_id = ?', 
                                         (proyecto['id'],)).fetchone()
        totales['costos'] = total_costos_result['total'] or 0 if total_costos_result else 0
        
        # Gastos
        total_gastos_result = conn.execute('SELECT SUM(valor) as total FROM gastos WHERE proyecto_id = ?', 
                                         (proyecto['id'],)).fetchone()
        totales['gastos'] = total_gastos_result['total'] or 0 if total_gastos_result else 0
        
        # Personal
        total_salarios_result = conn.execute('SELECT SUM(salario_mensual) as total FROM personal WHERE proyecto_id = ?', 
                                           (proyecto['id'],)).fetchone()
        totales['salarios'] = total_salarios_result['total'] or 0 if total_salarios_result else 0
        
        # Materiales
        total_materiales_result = conn.execute('SELECT SUM(valor) as total FROM materiales WHERE proyecto_id = ?', 
                                             (proyecto['id'],)).fetchone()
        totales['materiales'] = total_materiales_result['total'] or 0 if total_materiales_result else 0
        
        # Obtener ventas
        ventas_dias = conn.execute('SELECT * FROM ventas_dias WHERE proyecto_id = ?', 
                                  (proyecto['id'],)).fetchone()
        ventas_semanas = conn.execute('SELECT * FROM ventas_semanas WHERE proyecto_id = ?', 
                                     (proyecto['id'],)).fetchone()
        ventas_meses = conn.execute('SELECT * FROM ventas_meses WHERE proyecto_id = ?', 
                                   (proyecto['id'],)).fetchone()
        ventas_anos = conn.execute('SELECT * FROM ventas_anos WHERE proyecto_id = ?', 
                                  (proyecto['id'],)).fetchone()
    
        # Obtener ingresos (NUEVO)
        ingresos_dias = conn.execute('SELECT * FROM ingresos_dias WHERE proyecto_id = ?', 
                                   (proyecto['id'],)).fetchone()
        ingresos_semanas = conn.execute('SELECT * FROM ingresos_semanas WHERE proyecto_id = ?', 
                                      (proyecto['id'],)).fetchone()
        ingresos_meses = conn.execute('SELECT * FROM ingresos_meses WHERE proyecto_id = ?', 
                                    (proyecto['id'],)).fetchone()
        ingresos_anos = conn.execute('SELECT * FROM ingresos_anos WHERE proyecto_id = ?', 
                                   (proyecto['id'],)).fetchone()
        
    conn.close()
    
    return render_template('proyecto/flujos_caja.html', 
                         proyecto=proyecto,
                         totales=totales,
                         ventas_dias=ventas_dias,
                         ventas_semanas=ventas_semanas,
                         ventas_meses=ventas_meses,
                         ventas_anos=ventas_anos,
                         # Nuevos parámetros
                         ingresos_dias=ingresos_dias,
                         ingresos_semanas=ingresos_semanas,
                         ingresos_meses=ingresos_meses,
                         ingresos_anos=ingresos_anos)

@app.route('/proyecto/guardar-ventas-dias', methods=['POST'])
def guardar_ventas_dias():
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        flash('Primero debes crear un proyecto', 'warning')
        conn.close()
        return redirect(url_for('flujos_caja'))
    
    datos = {
        'lunes': int(request.form.get('lunes', 0)),
        'martes': int(request.form.get('martes', 0)),
        'miercoles': int(request.form.get('miercoles', 0)),
        'jueves': int(request.form.get('jueves', 0)),
        'viernes': int(request.form.get('viernes', 0)),
        'sabado': int(request.form.get('sabado', 0)),
        'domingo': int(request.form.get('domingo', 0))
    }
    
    datos_ingresos = {
        'lunes': float(request.form.get('ingresos_lunes', 0)),
        'martes': float(request.form.get('ingresos_martes', 0)),
        'miercoles': float(request.form.get('ingresos_miercoles', 0)),
        'jueves': float(request.form.get('ingresos_jueves', 0)),
        'viernes': float(request.form.get('ingresos_viernes', 0)),
        'sabado': float(request.form.get('ingresos_sabado', 0)),
        'domingo': float(request.form.get('ingresos_domingo', 0))
    }
    
    existente = conn.execute('SELECT * FROM ventas_dias WHERE proyecto_id = ?', 
                            (proyecto['id'],)).fetchone()
    
    if existente:
        conn.execute('''
            UPDATE ventas_dias SET 
            lunes = ?, martes = ?, miercoles = ?, jueves = ?, 
            viernes = ?, sabado = ?, domingo = ?
            WHERE proyecto_id = ?
        ''', (datos['lunes'], datos['martes'], datos['miercoles'], datos['jueves'],
              datos['viernes'], datos['sabado'], datos['domingo'], proyecto['id']))
    else:
        conn.execute('''
            INSERT INTO ventas_dias 
            (proyecto_id, lunes, martes, miercoles, jueves, viernes, sabado, domingo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (proyecto['id'], datos['lunes'], datos['martes'], datos['miercoles'], 
              datos['jueves'], datos['viernes'], datos['sabado'], datos['domingo']))
    
    # Guardar INGRESOS (si decides guardarlos aquí también)
    existente_ingresos = conn.execute('SELECT * FROM ingresos_dias WHERE proyecto_id = ?', 
                                    (proyecto['id'],)).fetchone()
    
    if existente_ingresos:
        conn.execute('''
            UPDATE ingresos_dias SET 
            lunes = ?, martes = ?, miercoles = ?, jueves = ?, 
            viernes = ?, sabado = ?, domingo = ?
            WHERE proyecto_id = ?
        ''', (datos_ingresos['lunes'], datos_ingresos['martes'], datos_ingresos['miercoles'], datos_ingresos['jueves'],
              datos_ingresos['viernes'], datos_ingresos['sabado'], datos_ingresos['domingo'], proyecto['id']))
    else:
        conn.execute('''
            INSERT INTO ingresos_dias 
            (proyecto_id, lunes, martes, miercoles, jueves, viernes, sabado, domingo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (proyecto['id'], datos_ingresos['lunes'], datos_ingresos['martes'], datos_ingresos['miercoles'], 
              datos_ingresos['jueves'], datos_ingresos['viernes'], datos_ingresos['sabado'], datos_ingresos['domingo']))
    
    conn.commit()
    conn.close()
    
    flash('Ventas por día guardadas correctamente', 'success')
    return redirect(url_for('flujos_caja'))

@app.route('/proyecto/guardar-ventas-semanas', methods=['POST'])
def guardar_ventas_semanas():
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        flash('Primero debes crear un proyecto', 'warning')
        conn.close()
        return redirect(url_for('flujos_caja'))
    
    datos = {
        'semana1': int(request.form.get('semana1', 0)),
        'semana2': int(request.form.get('semana2', 0)),
        'semana3': int(request.form.get('semana3', 0)),
        'semana4': int(request.form.get('semana4', 0))
    }
    
    existente = conn.execute('SELECT * FROM ventas_semanas WHERE proyecto_id = ?', 
                            (proyecto['id'],)).fetchone()
    
    if existente:
        conn.execute('''
            UPDATE ventas_semanas SET 
            semana1 = ?, semana2 = ?, semana3 = ?, semana4 = ?
            WHERE proyecto_id = ?
        ''', (datos['semana1'], datos['semana2'], datos['semana3'], 
              datos['semana4'], proyecto['id']))
    else:
        conn.execute('''
            INSERT INTO ventas_semanas 
            (proyecto_id, semana1, semana2, semana3, semana4)
            VALUES (?, ?, ?, ?, ?)
        ''', (proyecto['id'], datos['semana1'], datos['semana2'], 
              datos['semana3'], datos['semana4']))
    
    conn.commit()
    conn.close()
    
    flash('Ventas por semana guardadas correctamente', 'success')
    return redirect(url_for('flujos_caja'))

@app.route('/proyecto/guardar-ventas-meses', methods=['POST'])
def guardar_ventas_meses():
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        flash('Primero debes crear un proyecto', 'warning')
        conn.close()
        return redirect(url_for('flujos_caja'))
    
    datos = {
        'enero': int(request.form.get('enero', 0)),
        'febrero': int(request.form.get('febrero', 0)),
        'marzo': int(request.form.get('marzo', 0)),
        'abril': int(request.form.get('abril', 0)),
        'mayo': int(request.form.get('mayo', 0)),
        'junio': int(request.form.get('junio', 0)),
        'julio': int(request.form.get('julio', 0))
    }
    
    existente = conn.execute('SELECT * FROM ventas_meses WHERE proyecto_id = ?', 
                            (proyecto['id'],)).fetchone()
    
    if existente:
        conn.execute('''
            UPDATE ventas_meses SET 
            enero = ?, febrero = ?, marzo = ?, abril = ?, 
            mayo = ?, junio = ?, julio = ?
            WHERE proyecto_id = ?
        ''', (datos['enero'], datos['febrero'], datos['marzo'], datos['abril'],
              datos['mayo'], datos['junio'], datos['julio'], proyecto['id']))
    else:
        conn.execute('''
            INSERT INTO ventas_meses 
            (proyecto_id, enero, febrero, marzo, abril, mayo, junio, julio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (proyecto['id'], datos['enero'], datos['febrero'], datos['marzo'], 
              datos['abril'], datos['mayo'], datos['junio'], datos['julio']))
    
    conn.commit()
    conn.close()
    
    flash('Ventas por mes guardadas correctamente', 'success')
    return redirect(url_for('flujos_caja'))

@app.route('/proyecto/guardar-ventas-anos', methods=['POST'])
def guardar_ventas_anos():
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        flash('Primero debes crear un proyecto', 'warning')
        conn.close()
        return redirect(url_for('flujos_caja'))
    
    datos = {
        'año1': int(request.form.get('año1', 0)),
        'año2': int(request.form.get('año2', 0)),
        'año3': int(request.form.get('año3', 0)),
        'año4': int(request.form.get('año4', 0)),
        'año5': int(request.form.get('año5', 0)),
        'año6': int(request.form.get('año6', 0)),
        'año7': int(request.form.get('año7', 0))
    }
    
    existente = conn.execute('SELECT * FROM ventas_anos WHERE proyecto_id = ?', 
                            (proyecto['id'],)).fetchone()
    
    if existente:
        conn.execute('''
            UPDATE ventas_anos SET 
            año1 = ?, año2 = ?, año3 = ?, año4 = ?, 
            año5 = ?, año6 = ?, año7 = ?
            WHERE proyecto_id = ?
        ''', (datos['año1'], datos['año2'], datos['año3'], datos['año4'],
              datos['año5'], datos['año6'], datos['año7'], proyecto['id']))
    else:
        conn.execute('''
            INSERT INTO ventas_anos 
            (proyecto_id, año1, año2, año3, año4, año5, año6, año7)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (proyecto['id'], datos['año1'], datos['año2'], datos['año3'], 
              datos['año4'], datos['año5'], datos['año6'], datos['año7']))
    
    conn.commit()
    conn.close()
    
    flash('Ventas por año guardadas correctamente', 'success')
    return redirect(url_for('flujos_caja'))

# ==================== INGRESOS ====================

@app.route('/proyecto/guardar-ingresos-dias', methods=['POST'])
def guardar_ingresos_dias():
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        flash('Primero debes crear un proyecto', 'warning')
        conn.close()
        return redirect(url_for('flujos_caja'))
    
    datos = {
        'lunes': float(request.form.get('lunes_ingreso', 0)),
        'martes': float(request.form.get('martes_ingreso', 0)),
        'miercoles': float(request.form.get('miercoles_ingreso', 0)),
        'jueves': float(request.form.get('jueves_ingreso', 0)),
        'viernes': float(request.form.get('viernes_ingreso', 0)),
        'sabado': float(request.form.get('sabado_ingreso', 0)),
        'domingo': float(request.form.get('domingo_ingreso', 0))
    }
    
    existente = conn.execute('SELECT * FROM ingresos_dias WHERE proyecto_id = ?', 
                            (proyecto['id'],)).fetchone()
    
    if existente:
        conn.execute('''
            UPDATE ingresos_dias SET 
            lunes = ?, martes = ?, miercoles = ?, jueves = ?, 
            viernes = ?, sabado = ?, domingo = ?
            WHERE proyecto_id = ?
        ''', (datos['lunes'], datos['martes'], datos['miercoles'], datos['jueves'],
              datos['viernes'], datos['sabado'], datos['domingo'], proyecto['id']))
    else:
        conn.execute('''
            INSERT INTO ingresos_dias 
            (proyecto_id, lunes, martes, miercoles, jueves, viernes, sabado, domingo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (proyecto['id'], datos['lunes'], datos['martes'], datos['miercoles'], 
              datos['jueves'], datos['viernes'], datos['sabado'], datos['domingo']))
    
    conn.commit()
    conn.close()
    
    flash('Ingresos por día guardados correctamente', 'success')
    return redirect(url_for('flujos_caja'))

# Repite lo mismo para semanas, meses y años
# (copia las funciones de ventas y cambia "ventas" por "ingresos")

@app.route('/proyecto/guardar-ingresos-semanas', methods=['POST'])
def guardar_ingresos_semanas():
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        flash('Primero debes crear un proyecto', 'warning')
        conn.close()
        return redirect(url_for('flujos_caja'))
    
    datos = {
        'semana1': int(request.form.get('semana1', 0)),
        'semana2': int(request.form.get('semana2', 0)),
        'semana3': int(request.form.get('semana3', 0)),
        'semana4': int(request.form.get('semana4', 0))
    }
    
    existente = conn.execute('SELECT * FROM ingresos_semanas WHERE proyecto_id = ?', 
                            (proyecto['id'],)).fetchone()
    
    if existente:
        conn.execute('''
            UPDATE ingresos_semanas SET 
            semana1 = ?, semana2 = ?, semana3 = ?, semana4 = ?
            WHERE proyecto_id = ?
        ''', (datos['semana1'], datos['semana2'], datos['semana3'], 
              datos['semana4'], proyecto['id']))
    else:
        conn.execute('''
            INSERT INTO ingresos_semanas 
            (proyecto_id, semana1, semana2, semana3, semana4)
            VALUES (?, ?, ?, ?, ?)
        ''', (proyecto['id'], datos['semana1'], datos['semana2'], 
              datos['semana3'], datos['semana4']))
    
    conn.commit()
    conn.close()
    
    flash('Ingresos por semana guardadas correctamente', 'success')
    return redirect(url_for('flujos_caja'))

@app.route('/proyecto/guardar-ingresos-meses', methods=['POST'])
def guardar_ingresos_meses():
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        flash('Primero debes crear un proyecto', 'warning')
        conn.close()
        return redirect(url_for('flujos_caja'))
    
    datos = {
        'enero': int(request.form.get('enero', 0)),
        'febrero': int(request.form.get('febrero', 0)),
        'marzo': int(request.form.get('marzo', 0)),
        'abril': int(request.form.get('abril', 0)),
        'mayo': int(request.form.get('mayo', 0)),
        'junio': int(request.form.get('junio', 0)),
        'julio': int(request.form.get('julio', 0))
    }
    
    existente = conn.execute('SELECT * FROM ingresos_meses WHERE proyecto_id = ?', 
                            (proyecto['id'],)).fetchone()
    
    if existente:
        conn.execute('''
            UPDATE ingresos_meses SET 
            enero = ?, febrero = ?, marzo = ?, abril = ?, 
            mayo = ?, junio = ?, julio = ?
            WHERE proyecto_id = ?
        ''', (datos['enero'], datos['febrero'], datos['marzo'], datos['abril'],
              datos['mayo'], datos['junio'], datos['julio'], proyecto['id']))
    else:
        conn.execute('''
            INSERT INTO ingresos_meses 
            (proyecto_id, enero, febrero, marzo, abril, mayo, junio, julio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (proyecto['id'], datos['enero'], datos['febrero'], datos['marzo'], 
              datos['abril'], datos['mayo'], datos['junio'], datos['julio']))
    
    conn.commit()
    conn.close()
    
    flash('Ingresos por mes guardadas correctamente', 'success')
    return redirect(url_for('flujos_caja'))

@app.route('/proyecto/guardar-ingresos-anos', methods=['POST'])
def guardar_ingresos_anos():
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        flash('Primero debes crear un proyecto', 'warning')
        conn.close()
        return redirect(url_for('flujos_caja'))
    
    datos = {
        'año1': int(request.form.get('año1', 0)),
        'año2': int(request.form.get('año2', 0)),
        'año3': int(request.form.get('año3', 0)),
        'año4': int(request.form.get('año4', 0)),
        'año5': int(request.form.get('año5', 0)),
        'año6': int(request.form.get('año6', 0)),
        'año7': int(request.form.get('año7', 0))
    }
    
    existente = conn.execute('SELECT * FROM ingresos_anos WHERE proyecto_id = ?', 
                            (proyecto['id'],)).fetchone()
    
    if existente:
        conn.execute('''
            UPDATE ingresos_anos SET 
            año1 = ?, año2 = ?, año3 = ?, año4 = ?, 
            año5 = ?, año6 = ?, año7 = ?
            WHERE proyecto_id = ?
        ''', (datos['año1'], datos['año2'], datos['año3'], datos['año4'],
              datos['año5'], datos['año6'], datos['año7'], proyecto['id']))
    else:
        conn.execute('''
            INSERT INTO ingresos_anos 
            (proyecto_id, año1, año2, año3, año4, año5, año6, año7)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (proyecto['id'], datos['año1'], datos['año2'], datos['año3'], 
              datos['año4'], datos['año5'], datos['año6'], datos['año7']))
    
    conn.commit()
    conn.close()
    
    flash('ingresos por año guardadas correctamente', 'success')
    return redirect(url_for('flujos_caja'))

# ==================== FUNCIONES DE CÁLCULO ====================

def calcular_van(tasa_descuento, flujos):
    """Calcula el VAN dado una tasa de descuento y una lista de flujos."""
    van = 0
    for i, flujo in enumerate(flujos):
        van += flujo / ((1 + tasa_descuento) ** i)
    return van

def calcular_tir(flujos, iteraciones=1000, precision=0.0001):
    """Calcula la TIR usando el método de bisección."""
    def van_con_tasa(tasa):
        total = 0
        for i, flujo in enumerate(flujos):
            total += flujo / ((1 + tasa) ** i)
        return total
    
    tasa_min = -0.99
    tasa_max = 10.0
    
    van_min = van_con_tasa(tasa_min)
    van_max = van_con_tasa(tasa_max)
    
    if van_min * van_max > 0:
        return None
    
    for _ in range(iteraciones):
        tasa_media = (tasa_min + tasa_max) / 2
        van_media = van_con_tasa(tasa_media)
        
        if abs(van_media) < precision:
            return tasa_media
        
        if van_min * van_media < 0:
            tasa_max = tasa_media
            van_max = van_media
        else:
            tasa_min = tasa_media
            van_min = van_media
    
    return (tasa_min + tasa_max) / 2

def calcular_bc(flujos, tasa_descuento):
    """Calcula la relación Beneficio/Costo."""
    beneficios_pv = 0
    costos_pv = 0
    
    for i, flujo in enumerate(flujos):
        if flujo > 0:
            beneficios_pv += flujo / ((1 + tasa_descuento) ** i)
        else:
            costos_pv += abs(flujo) / ((1 + tasa_descuento) ** i)
    
    if costos_pv == 0:
        return float('inf')
    
    return beneficios_pv / costos_pv

def calcular_pri(flujos):
    """Calcula el Periodo de Recuperación de la Inversión."""
    inversion_inicial = abs(flujos[0]) if flujos and flujos[0] < 0 else 0
    if inversion_inicial == 0:
        return 0
    
    acumulado = 0
    
    for i, flujo in enumerate(flujos):
        if i == 0:
            continue
        
        acumulado += flujo
        
        if acumulado >= inversion_inicial:
            flujo_anterior = flujos[i-1] if i > 1 else 0
            faltante_antes = inversion_inicial - (acumulado - flujo)
            proporcion = faltante_antes / flujo if flujo != 0 else 0
            
            return (i - 1) + proporcion
    
    return None

# Función helper para plantillas
def calcular_van_template(tasa, flujos):
    """Versión para usar en plantillas Jinja2"""
    return calcular_van(tasa, flujos)

@app.context_processor
def utility_processor():
    """Inyecta funciones en todas las plantillas"""
    return dict(calcular_van=calcular_van_template)


def calcular_resumen_ventas(ventas_dias):
    """Calcula resumen de ventas por día"""
    if ventas_dias is None:
        return {'total': 0, 'dias_activos': 0, 'promedio': 0}
    
    # Convertir a diccionario si es SQLite Row
    if hasattr(ventas_dias, 'keys'):
        ventas = dict(ventas_dias)
    else:
        ventas = ventas_dias or {}
    
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    total = 0
    dias_activos = 0
    
    for dia in dias:
        venta = ventas.get(dia, 0)
        if venta and venta > 0:
            total += venta
            dias_activos += 1
    
    return {
        'total': total,
        'dias_activos': dias_activos,
        'promedio': total / dias_activos if dias_activos > 0 else 0
    }

def calcular_resumen_ingresos(ingresos_dias):
    """Calcula resumen de ingresos por día"""
    if not ingresos_dias:
        return {'total': 0, 'promedio_diario': 0}
    
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    total = 0
    
    for dia in dias:
        ingreso = ingresos_dias.get(dia, 0)
        total += ingreso
    
    return {
        'total': total,
        'promedio_diario': total / 7
    }

# ==================== CÁLCULOS FINANCIEROS ====================

@app.route('/resultados/calculos-financieros')
def calculos_financieros():
    conn = get_db_connection()
    
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        flash('Primero debes crear un proyecto', 'warning')
        conn.close()
        return redirect(url_for('index'))
    
    resultados = {
        'proyecto': proyecto,
        'totales': {},
        'calculos': {},
        'ventas': {},    # Nuevo: para datos de ventas
        'ingresos': {}   # Nuevo: para datos de ingresos
    }
    
    # Obtener totales
    # Costos
    total_costos_result = conn.execute('SELECT SUM(valor) as total FROM costos WHERE proyecto_id = ?', 
                                     (proyecto['id'],)).fetchone()
    resultados['totales']['costos'] = total_costos_result['total'] or 0 if total_costos_result else 0
    
    # Gastos
    total_gastos_result = conn.execute('SELECT SUM(valor) as total FROM gastos WHERE proyecto_id = ?', 
                                     (proyecto['id'],)).fetchone()
    resultados['totales']['gastos'] = total_gastos_result['total'] or 0 if total_costos_result else 0
    
    # Personal
    total_salarios_result = conn.execute('SELECT SUM(salario_mensual) as total FROM personal WHERE proyecto_id = ?', 
                                       (proyecto['id'],)).fetchone()
    resultados['totales']['salarios'] = total_salarios_result['total'] or 0 if total_salarios_result else 0
    
    # Materiales
    total_materiales_result = conn.execute('SELECT SUM(valor) as total FROM materiales WHERE proyecto_id = ?', 
                                         (proyecto['id'],)).fetchone()
    resultados['totales']['materiales'] = total_materiales_result['total'] or 0 if total_materiales_result else 0
    
    # Inversión inicial
    inversion_inicial = proyecto['valor_inversion'] if proyecto['tiene_inversion'] == 1 else 0
    
    # Obtener ventas por año para flujos
    ventas_anos = conn.execute('SELECT * FROM ventas_anos WHERE proyecto_id = ?', 
                              (proyecto['id'],)).fetchone()
    
    # ========== OBTENER DATOS DE VENTAS ==========
    # Obtener ventas
    ventas_dias = conn.execute('SELECT * FROM ventas_dias WHERE proyecto_id = ?', 
                                  (proyecto['id'],)).fetchone()
    ventas_semanas = conn.execute('SELECT * FROM ventas_semanas WHERE proyecto_id = ?', 
                                     (proyecto['id'],)).fetchone()
    ventas_meses = conn.execute('SELECT * FROM ventas_meses WHERE proyecto_id = ?', 
                                   (proyecto['id'],)).fetchone()
    ventas_anos = conn.execute('SELECT * FROM ventas_anos WHERE proyecto_id = ?', 
                                  (proyecto['id'],)).fetchone()
    
    resultados['ventas'] = {
        'anos': ventas_anos,
        'meses': ventas_meses,
        'semanas': ventas_semanas,
        'dias': ventas_dias
    }
    
    # ========== OBTENER DATOS DE INGRESOS ==========
    ingresos_anos = conn.execute('SELECT * FROM ingresos_anos WHERE proyecto_id = ?', 
                                (proyecto['id'],)).fetchone()
    ingresos_meses = conn.execute('SELECT * FROM ingresos_meses WHERE proyecto_id = ?', 
                                 (proyecto['id'],)).fetchone()
    ingresos_semanas = conn.execute('SELECT * FROM ingresos_semanas WHERE proyecto_id = ?', 
                                   (proyecto['id'],)).fetchone()
    ingresos_dias = conn.execute('SELECT * FROM ingresos_dias WHERE proyecto_id = ?', 
                                (proyecto['id'],)).fetchone()
    
    resultados['ingresos'] = {
        'anos': ingresos_anos,
        'meses': ingresos_meses,
        'semanas': ingresos_semanas,
        'dias': ingresos_dias
    }
    
    conn.close()
    
    # ========== CALCULAR TOTALES DE VENTAS/INGRESOS ==========
    
    # Total ventas anuales (suma de los 7 años)
    total_ventas_anuales = 0
    if ventas_anos:
        for i in range(1, 8):
            año_key = f'año{i}'
            if año_key in ventas_anos.keys():
                total_ventas_anuales += ventas_anos[año_key] or 0
    
    # Total ingresos anuales (suma de los 7 años)
    total_ingresos_anuales = 0
    if ingresos_anos:
        for i in range(1, 8):
            año_key = f'año{i}'
            if año_key in ingresos_anos.keys():
                total_ingresos_anuales += ingresos_anos[año_key] or 0
    
    resultados['calculos']['total_ventas_anuales'] = total_ventas_anuales
    resultados['calculos']['total_ingresos_anuales'] = total_ingresos_anuales
    
    # ========== CALCULAR PROMEDIOS ==========
    
    # Si no hay ingresos directos, calcularlos desde ventas
    if total_ingresos_anuales == 0 and total_ventas_anuales > 0:
        # Asumir que ingresos = ventas * precio del primer producto
        productos = obtener_productos_actuales()  # Tu función existente
        if productos and len(productos) > 0:
            precio_promedio = productos[0]['precio']  # O calcular promedio
            total_ingresos_anuales = total_ventas_anuales * precio_promedio
    
    resultados['calculos']['ingresos_promedio_anual'] = total_ingresos_anuales / 7 if total_ingresos_anuales > 0 else 0
    
    # Construir flujos de caja para 7 años
    flujos_anuales = []
    
    # Año 0: Inversión inicial (negativa)
    flujos_anuales.append(-inversion_inicial)
    
    # Años 1-7: Flujos netos
    if ventas_anos:
        # Calcular ingresos anuales usando get()
        for i in range(1, 8):
            ventas_key = f'año{i}'
            # Usar get() en lugar de getattr para mayor seguridad
            ventas = ventas_anos[ventas_key] if ventas_key in ventas_anos.keys() else 0
            ingresos_anuales = ventas * proyecto['precio_producto']
            
            # Calcular flujo neto
            costo_anual = resultados['totales']['costos'] / 7 if resultados['totales']['costos'] > 0 else 0
            gasto_anual = resultados['totales']['gastos'] / 7 if resultados['totales']['gastos'] > 0 else 0
            salario_anual = resultados['totales']['salarios'] * 12 if resultados['totales']['salarios'] > 0 else 0
            
            flujo_neto = ingresos_anuales - costo_anual - gasto_anual - salario_anual
            flujos_anuales.append(flujo_neto)
    else:
        # Valores por defecto si no hay ventas registradas
        for i in range(7):
            flujos_anuales.append(0)
    
    # Realizar cálculos financieros
    tasa_descuento = proyecto['tasa_descuento']
    
    try:
        # VAN
        van = calcular_van(tasa_descuento, flujos_anuales)
        resultados['calculos']['van'] = van
        
        # TIR
        tir = calcular_tir(flujos_anuales)
        resultados['calculos']['tir'] = tir * 100 if tir else 0
        
        # B/C
        bc = calcular_bc(flujos_anuales, tasa_descuento)
        resultados['calculos']['bc'] = bc
        
        # PRI
        pri = calcular_pri(flujos_anuales)
        resultados['calculos']['pri'] = pri
        
        # Otros indicadores
        resultados['calculos']['flujos'] = flujos_anuales
        resultados['calculos']['inversion_total'] = (
            inversion_inicial + 
            resultados['totales']['costos'] + 
            resultados['totales']['gastos'] + 
            (resultados['totales']['salarios'] * 12 * 7) +  # 7 años de salarios
            resultados['totales']['materiales']
        )
        
        # Rentabilidad
        if inversion_inicial > 0:
            resultados['calculos']['rentabilidad'] = (van / inversion_inicial) * 100
        else:
            resultados['calculos']['rentabilidad'] = 0
            
    except Exception as e:
        resultados['calculos']['error'] = f"Error en cálculos: {str(e)}"
        resultados['calculos']['van'] = 0
        resultados['calculos']['tir'] = 0
        resultados['calculos']['bc'] = 0
        resultados['calculos']['pri'] = 0
        resultados['calculos']['flujos'] = flujos_anuales
        resultados['calculos']['inversion_total'] = 0
        resultados['calculos']['rentabilidad'] = 0
    
    # CALCULAR RESUMEN DE VENTAS
    resumen_ventas = calcular_resumen_ventas(ventas_dias)
    
    # ¡IMPORTANTE: PASAR resumen_ventas AL TEMPLATE!
    return render_template('resultados/calculo_financiero.html',
                        resultados=resultados,
                        ventas_anos=ventas_anos,
                        ingresos_anos=ingresos_anos,
                        productos=productos,
                        resumen_ventas=resumen_ventas)  # ¡ESTA LÍNEA ES LA CLAVE!  # También pasa productos
    

def obtener_proyecto_actual():
    """Obtiene el proyecto actual"""
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    return proyecto

def obtener_productos_actuales():
    """Obtiene los productos del proyecto actual"""
    proyecto = obtener_proyecto_actual()
    if not proyecto:
        return []
    
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos WHERE proyecto_id = ? ORDER BY id', 
                           (proyecto['id'],)).fetchall()
    conn.close()
    return productos

# Añade esta función en app.py
def contar_productos():
    """Retorna solo el número de productos del proyecto actual"""
    conn = get_db_connection()
    
    # Primero obtener el proyecto actual
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    if not proyecto:
        conn.close()
        return 0
    
    # Contar productos
    resultado = conn.execute('SELECT COUNT(*) as total FROM productos WHERE proyecto_id = ?', 
                           (proyecto['id'],)).fetchone()
    
    conn.close()
    return resultado['total'] if resultado else 0

# Después de get_db_connection()
def calcular_total_costos_productos():
    """Calcula el total de costos de todos los productos"""
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    total = 0
    if proyecto:
        productos = conn.execute('SELECT id FROM productos WHERE proyecto_id = ?', 
                               (proyecto['id'],)).fetchall()
        
        for producto in productos:
            resultado = conn.execute('SELECT SUM(valor) as total FROM costos_productos WHERE producto_id = ?', 
                                   (producto['id'],)).fetchone()
            total_producto = resultado['total'] or 0 if resultado else 0
            total += total_producto
    
    conn.close()
    return total

def calcular_total_costos_generales():
    """Calcula el total de costos generales"""
    conn = get_db_connection()
    proyecto = conn.execute('SELECT * FROM proyectos ORDER BY id DESC LIMIT 1').fetchone()
    
    total = 0
    if proyecto:
        resultado = conn.execute('SELECT SUM(valor) as total FROM costos_generales WHERE proyecto_id = ?', 
                               (proyecto['id'],)).fetchone()
        total = resultado['total'] or 0 if resultado else 0
    
    conn.close()
    return total

# Hacerlas disponibles en todos los templates
@app.context_processor
def inject_calculos():
    return {
        'total_costos_productos': calcular_total_costos_productos,
        'total_costos_generales': calcular_total_costos_generales,
        'contar_productos': contar_productos  # La que ya tienes
    }

# Ruta para limpiar todos los datos
@app.route('/limpiar-datos')
def limpiar_datos():
    conn = get_db_connection()
    
    conn.execute('DELETE FROM costos')
    conn.execute('DELETE FROM gastos')
    conn.execute('DELETE FROM personal')
    conn.execute('DELETE FROM materiales')
    conn.execute('DELETE FROM ventas_dias')
    conn.execute('DELETE FROM ventas_semanas')
    conn.execute('DELETE FROM ventas_meses')
    conn.execute('DELETE FROM ventas_anos')
    
    conn.commit()
    conn.close()
    
    flash('Todos los datos han sido limpiados (excepto el proyecto)', 'warning')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
