import bpy
import math

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def create_mini_bulb(location, rotation=(0,0,0), scale=1.0):
    # Create the bulb base
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08*scale, depth=0.1*scale)
    base = bpy.context.active_object
    base.name = f'MiniBase_{location[0]}_{location[1]}'
    base.location = location
    base.rotation_euler = rotation
    
    # Create the glass bulb
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15*scale)
    bulb = bpy.context.active_object
    bulb.name = f'MiniBulb_{location[0]}_{location[1]}'
    bulb.location = (location[0], location[1], location[2] + 0.15*scale)
    bulb.rotation_euler = rotation
    bulb.scale = (1, 1, 1.2)
    
    return base, bulb

# Create a cluster of mini bulbs
positions = [
    ((0, 0, 0), (0, 0, 0), 1.0),
    ((0.3, 0.2, 0.1), (math.radians(15), math.radians(10), 0), 0.9),
    ((-0.3, 0.1, 0.05), (math.radians(-10), math.radians(5), 0), 0.8),
    ((0.1, -0.3, 0.08), (math.radians(5), math.radians(-15), 0), 0.85),
]

bases = []
bulbs = []
for pos, rot, scale in positions:
    base, bulb = create_mini_bulb(pos, rot, scale)
    bases.append(base)
    bulbs.append(bulb)

# Add materials
base_mat = bpy.data.materials.new(name="MetalBase")
base_mat.use_nodes = True
base_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.8, 1)
base_mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.8

glass_mat = bpy.data.materials.new(name="GlassBulb")
glass_mat.use_nodes = True
glass_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.9, 0.9, 1)
glass_mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2

for base in bases:
    base.data.materials.append(base_mat)
for bulb in bulbs:
    bulb.data.materials.append(glass_mat)

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
bpy.context.scene.render.filepath = "//mini_bulbs_render.png"
bpy.ops.render.render(write_still=True)
