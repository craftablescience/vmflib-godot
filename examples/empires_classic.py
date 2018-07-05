
from vmflib2.games import empires, base, halflife2
from vmflib2.tools import HollowBox, DisplacementMap
from vmflib2.vmf import ValveMap
import PIL.Image

# Empires maps need to be quite tall to allow artillery shells to traverse the map.
map_size = ((64 + 32) * 256, (64 + 32) * 256, 64 * 256)
water_height = 1024

m = ValveMap()

# We surround the map with a giant box, to be a skybox
skybox = HollowBox(size=map_size)
for brush in skybox.brushes:
    brush.set_material('tools/toolsskybox2d')
skybox.floor.set_material("tools/toolsnodraw")

# This is the water brush. As is good practice, only the surface of the water has a water texture; the rest is nodraw
water = skybox.get_level_brush(water_height / 2 - map_size[2] / 2, water_height)
water.set_material("tools/toolsnodraw")
water.top().material = 'nature/water_canals_city_murky'

# Add everything we prepared to the world geometry
m.add_solids(skybox.brushes)
m.add_solid(water)

# Enclosing maps with big, open skyboxes like the one we just made is inefficient because we have a bunch of visleaves
#   touching each other. Instead of letting vvis.exe check all of them, we just tell it they're all connected via
#   a func_viscluster
# (we create two, one at the top of the map, and one at the bottom. this is because the water brush splits the visleafs)
for h in (map_size[2] / 2 - 16, -map_size[2] / 2 + 16):
    viscluster = base.FuncViscluster(m)
    viscluster_brush = skybox.get_level_brush(h, 32)
    viscluster_brush.set_material('tools/toolstrigger')
    viscluster.children.append(viscluster_brush)


# TODO: Import or Generate heightmap, use Simulated annealing to place refs, bases, and potential base locations.






# Write the map to a file
m.write_vmf('empires_classic.vmf')