import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
# from pyglet.gl import GL_LINES
from pyglet.gl import (GL_DEPTH_TEST,
                       GL_TRIANGLES,
                       GL_LINES,        # GL_POINTS
                       )
# from pyglet.gl import GL_POINT_SIZE
from pyglet.gl import glClearColor, glEnable, glLineWidth, glPointSize
from pyglet.math import Mat4, Vec3
from math import sqrt


""" FIVE TETRAHEDRA """
""" Embedded tetrahedra, each having a different colour.
    Vertices of the tetrahedra have dodecahedral symmetry.
"""

window = pyglet.window.Window(1280, 720, caption="FIVE TERTAHEDRA")
glEnable(GL_DEPTH_TEST)
# set window background colour
glClearColor(1.0, 1.0, 1.0, 1.0)
glLineWidth(1)
glPointSize(10)


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
view_mat = Mat4.from_translation(Vec3(x=0, y=0, z=-200))
proj_mat = Mat4.orthogonal_projection(left=0, right=1280,
                                      bottom=0, top=720,
                                      z_near=0.1, z_far=1000)

vp = proj_mat @ view_mat

program['vp'] = vp

# create the translation matrix
translate_mat = Mat4.from_translation(vector=Vec3(x=640, y=360, z=0))

program['model'] = translate_mat

batch = pyglet.graphics.Batch()

# Regular dodecahedron built on golden ratio (ref wikipedia.com/dodecahedron)
h = 2.0 / (1.0 + sqrt(5.0))                 # approx 0.618
h2 = h * h

# Vertices are defined (ref wikipedia)
vertices = [
    -1, -1, -1,                 # vertex 0
    1, -1, -1,
    1,  1, -1,
    -1,  1, -1,                 # 3

    -1, -1,  1,                 # 4
    1, -1,  1,
    1,  1,  1,
    -1,  1,  1,                 # 7

    0, -(1+h), -(1-h2),         # 8
    0, -(1+h),  (1-h2),         # 9
    0,  (1+h),  (1-h2),
    0,  (1+h), -(1-h2),

    -(1+h), -(1-h2), 0,
    -(1+h),  (1-h2), 0,         # 13
    (1+h),  (1-h2), 0,
    (1+h), -(1-h2), 0,          # 15

    -(1-h2), 0, -(1+h),
    -(1-h2), 0,  (1+h),
    (1-h2), 0,  (1+h),
    (1-h2), 0, -(1+h)           # vertex 19
]

# embedded tetrahedra each having 4 faces
indices_red = [
    10, 19, 5,
    10, 19, 12,
    10, 5, 12,
    19, 5, 12
]
indices_blu = [
    2, 18, 13,
    2, 18, 8,
    2, 13, 8,
    18, 13, 8
]
indices_ora = [
    11, 15, 0,
    11, 15, 17,
    11, 0, 17,
    15, 0, 17
]
indices_yel = [
    14, 7, 16,
    14, 7, 9,
    14, 16, 9,
    16, 7, 9
]
indices_grn = [
    6, 3, 1,
    6, 3, 4,
    6, 1, 4,
    1, 3, 4
]

edge_indices = [
    10, 19, 10, 12, 10, 5, 5, 19, 19, 12, 12, 5,
    2, 18, 2, 13, 2, 8, 8, 13, 13, 18, 18, 8,
    11, 15, 11, 0, 11, 17, 17, 0, 0, 15, 15, 17,
    14, 7, 14, 16, 14, 9, 9, 16, 16, 7, 7, 9,
    6, 3, 6, 1, 6, 4, 4, 1, 1, 3, 3, 4
]


# Just some colours
red_colors = (255, 0, 0, 255) * 20
grn_colors = (0, 200, 0, 255) * 20
blu_colors = (0, 0, 255, 255) * 20
ora_colors = (255, 127, 0, 255) * 20
yel_colors = (255, 255, 0, 255) * 20

point_colors = (0, 0, 0, 255) * 20
edge_colors = (127, 127, 127, 255) * 20    # (255, 127, 127, 255) * 20

# # Scale up the vertices
vertices = [v * 100 for v in vertices]

program.vertex_list_indexed(
    20,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_red,
    vertices=('f', vertices),
    colors=('Bn', red_colors)
)
program.vertex_list_indexed(
    20,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_blu,
    vertices=('f', vertices),
    colors=('Bn', blu_colors)
)
program.vertex_list_indexed(
    20,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_ora,
    vertices=('f', vertices),
    colors=('Bn', ora_colors)
)
program.vertex_list_indexed(
    20,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_yel,
    vertices=('f', vertices),
    colors=('Bn', yel_colors)
)
program.vertex_list_indexed(
    20,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_grn,
    vertices=('f', vertices),
    colors=('Bn', grn_colors)
)

# edges
program.vertex_list_indexed(
    20,
    GL_LINES,
    batch=batch,
    indices=edge_indices,
    vertices=('f', vertices),
    colors=('Bn', edge_colors)
)

# # draw the vertices, all one colour
# program.vertex_list(
#     20,
#     GL_POINTS,
#     batch=batch,
#     vertices=('f', vertices),
#     colors=('Bn', point_colors)
# )


@window.event
def on_draw():
    window.clear()
    batch.draw()


angle = 0


def update(dt: float):
    global angle
    angle += dt
    # spin it around all axes
    rotate_x_mat = Mat4.from_rotation(angle=angle, vector=Vec3(x=1, y=0, z=0))
    rotate_y_mat = Mat4.from_rotation(angle=angle, vector=Vec3(x=0, y=1, z=0))
    rotate_z_mat = Mat4.from_rotation(angle=angle, vector=Vec3(x=0, y=0, z=1))
    # upload the combined model matrix to the vertex shader model uniform
    model_mat = translate_mat @ rotate_x_mat @ rotate_y_mat @ rotate_z_mat
    program['model'] = model_mat


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
