import bpy
import math

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create the bulb base
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.2)
base = bpy.context.active_object
base.name = 'BulbBase'

# Create the glass bulb
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3)
bulb = bpy.context.active_object
bulb.name = 'BulbGlass'
bulb.location = (0, 0, 0.3)

# Scale the bulb to be more elongated
bulb.scale = (1, 1, 1.5)

# Add materials
base_mat = bpy.data.materials.new(name="MetalBase")
base_mat.use_nodes = True
base_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.8, 1)
base_mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.8
base.data.materials.append(base_mat)

glass_mat = bpy.data.materials.new(name="GlassBulb")
glass_mat.use_nodes = True
glass_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.9, 0.9, 1)
glass_mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2
bulb.data.materials.append(glass_mat)

# Set up camera for side view
bpy.ops.object.camera_add(location=(3, 0, 1))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(90), 0, math.radians(90))

# Set up lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))

# Render settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = True

# Render and save
bpy.context.scene.camera = camera
bpy.context.scene.render.filepath = "//xxl_bulb_side_render.png"
bpy.ops.render.render(write_still=True)
