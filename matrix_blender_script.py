import bpy
import random
import math

# --- 1. CONFIGURACIÓN DE LA ESCENA ---

def setup_scene():
    """Limpia la escena y configura el render y el mundo."""
    # Limpiar todos los objetos de la escena
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Configurar el motor de render a Eevee Next (para Blender 4.2+)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT'

    # Configurar el fondo a negro
    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg_node = world.node_tree.nodes['Background']
    bg_node.inputs['Color'].default_value = (0, 0, 0, 1)
    bg_node.inputs['Strength'].default_value = 1.0

    # Configurar el glow/bloom en el compositor
    scene.use_nodes = True
    tree = scene.node_tree

    # Limpiar nodos existentes
    for node in tree.nodes:
        tree.nodes.remove(node)

    # Crear nodos de render y composite
    render_layers_node = tree.nodes.new(type='CompositorNodeRLayers')
    composite_node = tree.nodes.new(type='CompositorNodeComposite')

    # Crear nodo Glare para el efecto bloom
    glare_node = tree.nodes.new(type='CompositorNodeGlare')
    glare_node.glare_type = 'FOG'
    glare_node.threshold = 0.8
    glare_node.mix = -0.8
    glare_node.size = 9

    # Conectar los nodos
    tree.links.new(render_layers_node.outputs['Image'], glare_node.inputs['Image'])
    tree.links.new(glare_node.outputs['Image'], composite_node.inputs['Image'])

    # Posicionar nodos para que se vean bien
    render_layers_node.location = -300, 300
    glare_node.location = 0, 300
    composite_node.location = 300, 300

    # Establecer la duración de la animación
    scene.frame_start = 1
    scene.frame_end = 240


# --- 2. CREACIÓN DEL GLOW HEAD ---

def create_glow_head():
    """Crea la cabeza brillante estilizada y la anima."""
    # Crear la cabeza a partir de una esfera
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
    head = bpy.context.active_object
    head.name = "GlowHead"

    # Entrar en modo edición para darle forma
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    # Seleccionar el vértice inferior (barbilla)
    obj_matrix = head.matrix_world
    mesh = head.data
    min_z_vert = min(mesh.vertices, key=lambda v: (obj_matrix @ v.co).z)
    min_z_vert.select = True

    # Usar edición proporcional para crear la forma de la barbilla
    bpy.context.scene.tool_settings.use_proportional_edit = True
    bpy.context.scene.tool_settings.proportional_edit_falloff = 'SMOOTH'
    bpy.ops.transform.translate(
        value=(0, 0, -0.4),
        proportional_size=0.6
    )
    bpy.context.scene.tool_settings.use_proportional_edit = False
    bpy.ops.object.mode_set(mode='OBJECT')

    # Suavizar el sombreado
    bpy.ops.object.shade_smooth()

    # Crear material para la cabeza
    mat_head = bpy.data.materials.new(name="HeadGlowMaterial")
    mat_head.use_nodes = True
    head.data.materials.append(mat_head)

    # Configurar nodos del material (Emission)
    nodes = mat_head.node_tree.nodes
    principled_bsdf = nodes.get('Principled BSDF')
    if principled_bsdf:
        nodes.remove(principled_bsdf)

    emission_node = nodes.new(type='ShaderNodeEmission')
    emission_node.inputs['Color'].default_value = (0.1, 1.0, 0.2, 1) # Color verde

    # Usar el método links.new() para mayor robustez
    mat_output = nodes.get('Material Output')
    mat_head.node_tree.links.new(emission_node.outputs['Emission'], mat_output.inputs['Surface'])

    # Añadir driver para la pulsación del brillo
    strength_input = emission_node.inputs['Strength']
    fcurve = strength_input.driver_add('default_value')
    driver = fcurve.driver
    driver.type = 'SCRIPTED'
    # Expresión: 5 + 5 * sin(frame / 10) -> pulsa entre 0 y 10
    driver.expression = "5 + 5 * sin(frame / 10)"


# --- 3. CREACIÓN DE LA LLUVIA MATRIX ---

# Caracteres a usar en la lluvia
KATAKANA = "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン"

def create_rainbow_material():
    """Crea un material de emisión cuyo color cambia con el tiempo (arcoíris)."""
    mat_rain = bpy.data.materials.new(name="RainMaterial")
    mat_rain.use_nodes = True

    nodes = mat_rain.node_tree.nodes
    nodes.remove(nodes.get('Principled BSDF')) # Quitar el nodo por defecto

    # Crear nodos necesarios
    material_output = nodes.get('Material Output')
    emission_node = nodes.new(type='ShaderNodeEmission')
    hsv_node = nodes.new(type='ShaderNodeHueSaturation')

    # Conectar nodos: HSV -> Emission -> Output
    mat_rain.node_tree.links.new(hsv_node.outputs['Color'], emission_node.inputs['Color'])
    mat_rain.node_tree.links.new(emission_node.outputs['Emission'], material_output.inputs['Surface'])

    # Configurar valores iniciales
    hsv_node.inputs['Color'].default_value = (0.3, 1, 1, 1) # Verde base
    emission_node.inputs['Strength'].default_value = 7.0

    # Añadir driver al Hue para el efecto arcoíris
    fcurve = hsv_node.inputs['Hue'].driver_add('default_value')
    driver = fcurve.driver
    driver.type = 'SCRIPTED'
    # Expresión: (frame / 100) % 1 -> cicla el matiz de 0 a 1
    driver.expression = "(frame / 100) % 1.0"

    return mat_rain

def update_rain_characters(scene):
    """Handler que se ejecuta en cada frame para cambiar los caracteres."""
    # Solo se ejecuta si estamos en un frame de la animación
    if scene.frame_current >= scene.frame_start and scene.frame_current <= scene.frame_end:
        for obj in scene.objects:
            if obj.name.startswith("RainDrop_"):
                obj.data.body = random.choice(KATAKANA)

def create_matrix_rain(columns=20, rows=15, spacing=0.8):
    """Crea las columnas de texto que caen."""
    rainbow_material = create_rainbow_material()

    # Definir el área de la lluvia
    x_start = - (columns - 1) * spacing / 2
    y_start = - (rows - 1) * spacing / 2
    z_top = 5.0
    z_bottom = -5.0

    for i in range(columns):
        for j in range(rows):
            # Posición de la columna
            x = x_start + i * spacing
            y = y_start + j * spacing

            # Crear el objeto de texto
            bpy.ops.object.text_add(location=(x, y, z_top))
            text_obj = bpy.context.active_object
            text_obj.name = f"RainDrop_{i}_{j}"
            text_obj.data.body = random.choice(KATAKANA)
            text_obj.data.size = 0.5
            text_obj.data.align_x = 'CENTER'
            text_obj.data.materials.append(rainbow_material)

            # Animación de caída
            text_obj.keyframe_insert(data_path="location", frame=1, index=2) # Z en el top

            # Mover a la parte inferior y crear otro keyframe
            text_obj.location.z = z_bottom
            text_obj.keyframe_insert(data_path="location", frame=100, index=2) # Z en el bottom

            # Hacer que la animación sea cíclica
            fcurve = text_obj.animation_data.action.fcurves.find('location', index=2)
            modifier = fcurve.modifiers.new(type='CYCLES')

            # Desfase aleatorio en la animación para que no caigan todos a la vez
            fcurve.keyframe_points[0].co.x += random.uniform(-50, 50)
            fcurve.keyframe_points[1].co.x += random.uniform(-50, 50)

    # Registrar el handler para el cambio de caracteres
    # Primero, nos aseguramos de que no esté ya registrado
    for handler in bpy.app.handlers.frame_change_pre:
        if handler.__name__ == 'update_rain_characters':
            bpy.app.handlers.frame_change_pre.remove(handler)

    bpy.app.handlers.frame_change_pre.append(update_rain_characters)


# --- 4. CONFIGURACIÓN DE LA CÁMARA ---

def setup_camera():
    """Crea y posiciona la cámara."""
    bpy.ops.object.camera_add(location=(0, -8, 0))
    camera = bpy.context.active_object
    camera.name = "MainCamera"
    # Apuntar la cámara al centro
    camera.rotation_euler[0] = math.radians(90)
    bpy.context.scene.camera = camera


# --- EJECUCIÓN PRINCIPAL ---

if __name__ == "__main__":
    setup_scene()
    create_glow_head()
    create_matrix_rain(columns=30, rows=20, spacing=0.7)
    setup_camera()
    print("Script de Blender para Matrix Rain ejecutado.")
