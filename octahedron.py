import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_LINES
from pyglet.gl import GL_TRIANGLES, GL_DEPTH_TEST
from pyglet.gl import glClearColor, glEnable, glLineWidth
from pyglet.math import Mat4, Vec3


""" OCTAHEDRON """

window = pyglet.window.Window(1280, 720, caption="OCTAHEDRON")
glEnable(GL_DEPTH_TEST)
# set window background colour
glClearColor(1.0, 1.0, 1.0, 1.0)
glLineWidth(5)

# create the vertex source and fragment source
vertex_source = """
#version 330
layout(location = 0) in vec3 vertices;
layout(location = 1) in vec4 colors;

out vec4 newColor;

uniform mat4 vp;
uniform mat4 model;

void main()
{
    gl_Position = vp * model * vec4(vertices, 1.0f);
    newColor = colors;
}
"""

fragment_source = """
#version 330
in vec4 newColor;

out vec4 outColor;

void main()
{
    outColor = newColor;
}
"""

# compile vertex source and fragment source into the shader program
vert_shader = Shader(vertex_source, 'vertex')
frag_shader = Shader(fragment_source, 'fragment')
program = ShaderProgram(vert_shader, frag_shader)

# view_mat seems to be position of eye
view_mat = Mat4.from_translation(Vec3(x=0, y=0, z=-400))
proj_mat = Mat4.orthogonal_projection(left=0, right=1280,
                                      bottom=0, top=720,
                                      z_near=0.1, z_far=1000)

vp = proj_mat @ view_mat

program['vp'] = vp

# create the translation matrix
translate_mat = Mat4.from_translation(vector=Vec3(x=640, y=360, z=0))

program['model'] = translate_mat

batch = pyglet.graphics.Batch()

# Vertices are defined (ref wikipedia)
vertices = [
    1, 0, 0,
    0, 1, 0,
    0, 0, 1,

    -1, 0, 0,
    0, -1, 0,
    0, 0, -1
]

# vertex 0 is opposite vertex 3
# Others vertices (all on x=0 plane) cycle thru 1, 2, 4, 5

indices_blu = [
    0, 1, 2,
    3, 5, 4
]
indices_ora = [
    0, 2, 4,
    3, 1, 5
]
indices_red = [
    0, 5, 1,
    3, 4, 2
]
indices_yel = [
    0, 4, 5,
    3, 2, 1
]
indices_edge = [
    0, 1,  0, 2,  0, 4,  0, 5,
    3, 1,  3, 2,  3, 4,  3, 5,
    1, 2,  2, 4,  4, 5,  5, 1,
]
vertices_cube = [
    -1, -1, -1,
    -1, -1,  1,
    -1,  1,  1,
    -1,  1, -1,

    1, -1, -1,
    1, -1,  1,
    1,  1,  1,
    1,  1, -1
]

indices_cube = [
    0, 1,  1, 2,  2, 3,  3, 0,      # only edges
    4, 5,  5, 6,  6, 7,  7, 4,
    0, 4,  1, 5,  2, 6,  3, 7,

    0, 6,  1, 7,  2, 4,  3, 5,      # main diagonals

    0, 2,  1, 3,  4, 6,  5, 7,      # face diagonals
    0, 5,  1, 6,  2, 7,  3, 4,
    0, 7,  1, 4,  2, 5,  3, 6
]

# Colours
# octahedron faces
colors_blu = (0, 0, 200, 255) * 6
colors_ora = (255, 127, 0, 255) * 6
colors_red = (200, 0, 0, 255) * 6
colors_yel = (200, 200, 0, 255) * 6
# octahedron edges
colors_whi = (255, 255, 255, 255) * 6
# cube edges
colors_grn = (30, 240, 0, 255) * 8

# # Scale up the vertices
vertices = [v * 200 for v in vertices]
vertices_cube = [v * 200 for v in vertices_cube]

# blue face batch
program.vertex_list_indexed(
    6,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_blu,
    vertices=('f', vertices),
    colors=('Bn', colors_blu)
)
# orange face batch
program.vertex_list_indexed(
    6,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_ora,
    vertices=('f', vertices),
    colors=('Bn', colors_ora)
)
# red face batch
program.vertex_list_indexed(
    6,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_red,
    vertices=('f', vertices),
    colors=('Bn', colors_red)
)
# yellow face batch
program.vertex_list_indexed(
    6,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_yel,
    vertices=('f', vertices),
    colors=('Bn', colors_yel)
)

# octahedron edges
program.vertex_list_indexed(
    6,
    GL_LINES,
    batch=batch,
    indices=indices_edge,
    vertices=('f', vertices),
    colors=('Bn', colors_whi)
)
# cube edges
program.vertex_list_indexed(
    8,
    GL_LINES,
    batch=batch,
    indices=indices_cube,
    vertices=('f', vertices_cube),
    colors=('Bn', colors_grn)
)


@window.event
def on_draw():
    window.clear()
    batch.draw()


angle = 0


def update(dt: float):
    global angle
    angle += dt * 0.5
    # upload the combined model matrix to the vertex shader model uniform
    rotate_mat_x = Mat4.from_rotation(angle=angle, vector=Vec3(x=1, y=0, z=0))
    rotate_mat_y = Mat4.from_rotation(angle=angle, vector=Vec3(x=0, y=1, z=0))
    rotate_mat_z = Mat4.from_rotation(angle=angle, vector=Vec3(x=0, y=0, z=1))
    model_mat = translate_mat @ rotate_mat_x @ rotate_mat_y @ rotate_mat_z
    program['model'] = model_mat


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
