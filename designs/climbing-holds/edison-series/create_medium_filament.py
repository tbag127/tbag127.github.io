import bpy
import math
import bmesh

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def create_spiral_filament():
    # Create a new mesh and bmesh
    mesh = bpy.data.meshes.new('FilamentMesh')
    bm = bmesh.new()
    
    # Create spiral vertices
    segments = 64
    radius = 0.15
    height = 0.4
    revolutions = 2.5
    
    for i in range(segments + 1):
        t = i / segments
        angle = t * math.pi * 2 * revolutions
        x = math.cos(angle) * radius * (1 - t * 0.3)  # Gradually decrease radius
        y = math.sin(angle) * radius * (1 - t * 0.3)
        z = t * height
        bm.verts.new((x, y, z))
    
    # Create edges between vertices
    verts = bm.verts[:]
    for i in range(len(verts) - 1):
        bm.edges.new((verts[i], verts[i + 1]))
    
    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Create object and link to scene
    obj = bpy.data.objects.new('Filament', mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# Create base cylinder
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.15)
base = bpy.context.active_object
base.name = 'FilamentBase'

# Create filament
filament = create_spiral_filament()
filament.location = (0, 0, 0.075)

# Add materials
base_mat = bpy.data.materials.new(name="MetalBase")
base_mat.use_nodes = True
base_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.8, 1)
base_mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.8
base.data.materials.append(base_mat)

filament_mat = bpy.data.materials.new(name="FilamentMetal")
filament_mat.use_nodes = True
filament_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.7, 0.4, 1)
filament_mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.6
filament.data.materials.append(filament_mat)

# Set up camera
bpy.ops.object.camera_add(location=(2, -2, 2))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))

# Set up lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))

# Render settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = True

# Render and save
bpy.context.scene.camera = camera
bpy.context.scene.render.filepath = "//medium_filament_render.png"
bpy.ops.render.render(write_still=True)
