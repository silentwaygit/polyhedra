import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
# from pyglet.gl import GL_LINES
from pyglet.gl import (GL_DEPTH_TEST,
                       GL_TRIANGLES,
                       GL_LINES,
                       GL_POINTS)
# from pyglet.gl import GL_POINT_SIZE
from pyglet.gl import glClearColor, glEnable, glLineWidth, glPointSize
from pyglet.math import Mat4, Vec3
from math import sqrt


""" TEN TETRAHEDRA """
""" Embedded tetrahedra, each having a different colour.
    Vertices of the tetrahedra have dodecahedral symmetry.
"""

window = pyglet.window.Window(1280, 720, caption="TEN TETRAHEDRA")
glEnable(GL_DEPTH_TEST)
# set window background colour
glClearColor(1.0, 1.0, 1.0, 1.0)
glLineWidth(5)
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
# 2 sets of 5 tetrahedra - a right-hand set and a left-hand set
# pairs of faces: one from set 1 and one from set 2 are coplanar
# tetrahedra in set 1 are each drawn in a single colour
indices_A = [
    10, 19, 5,      # A
    11, 18, 1,
]
indices_B = [
    10, 19, 12,     # B
    2, 7, 0,
]
indices_C = [
    10, 5, 12,      # C
    6, 13, 9,
]
indices_D = [
    19, 5, 12,      # D
    15, 16, 4,
]
indices_E = [
    11, 15, 17,     # E
    2, 7, 5,
]
indices_F = [
    11, 15, 0,      # F
    14, 3, 8,
]
indices_G = [
    11, 17, 0,      # G
    10, 16, 4,
]
indices_H = [
    15, 17, 0,      # H
    18, 1, 12,
]
indices_J = [
    2, 18, 13,      # J
    14, 3, 17,
]
indices_K = [
    2, 18, 8,       # K
    6, 19, 9,
]
indices_L = [
    2, 13, 8,       # L
    11, 1, 12,
]
indices_M = [
    18, 13, 8,      # M
    7, 5, 0,
]
indices_N = [
    14, 7, 16,      # N
    6, 19, 13,
]
indices_P = [
    14, 7, 9,       # P
    10, 15, 4,
]
indices_Q = [
    14, 16, 9,      # Q
    2, 5, 0,
]
indices_R = [
    7, 16, 9,       # R
    3, 17, 8
]
indices_S = [
    6, 3, 1,        # S
    10, 15, 16
]
indices_T = [
    6, 3, 4,        # T
    11, 18, 12
]
indices_U = [
    6, 1, 4,        # U
    14, 17, 8
]
indices_V = [
    3, 1, 4,        # V
    19, 13, 9
]

indices_red = indices_A + indices_B + indices_C + indices_D
indices_blu = indices_E + indices_F + indices_G + indices_H
indices_ora = indices_J + indices_K + indices_L + indices_M
indices_yel = indices_N + indices_P + indices_Q + indices_R
indices_grn = indices_S + indices_T + indices_U + indices_V

edge_indices = [
    10, 19, 10, 12, 10, 5, 5, 19, 19, 12, 12, 5,
    2, 18, 2, 13, 2, 8, 8, 13, 13, 18, 18, 8,
    11, 15, 11, 0, 11, 17, 17, 0, 0, 15, 15, 17,
    14, 7, 14, 16, 14, 9, 9, 16, 16, 7, 7, 9,

    6, 3, 6, 1, 6, 4, 4, 1, 1, 3, 3, 4
]

dodecahedron_edge_indices = [
    10, 11, 11, 2, 2, 14, 14, 6, 6, 10,
    1, 15, 15, 5, 5, 18, 18, 17, 17, 7,
    7, 13, 13, 3, 3, 16, 16, 19, 19, 1,
    0, 12, 12, 4, 4, 9, 9, 8, 8, 0,
    1, 8, 5, 9, 17, 4, 13, 12, 16, 0,
    19, 2, 15, 14, 18, 6, 7, 10, 3, 11
]

# prep for drawing some axis indicators:
# red for x-axis, green for y-axis, and blu for z-axis
vertices_axes = [
    2, 0, 0, 2.5, 0, 0,     # x-axis marker
    0, 2, 0, 0, 2.5, 0,     # y-axis marker
    0, 0, 2, 0, 0, 2.5      # z-axis marker
]
indices_axes = [
    0, 1,
    2, 3,
    4, 5
]
color_axes = [
    255, 0, 0, 255, 255, 0, 0, 255,
    0, 255, 0, 255, 0, 255, 0, 255,
    0, 0, 255, 255, 0, 0, 255, 255
]


# Just some colours
red_colors = (255, 0, 0, 255) * 20
grn_colors = (0, 200, 0, 255) * 20
blu_colors = (0, 0, 255, 255) * 20
ora_colors = (255, 127, 0, 255) * 20
yel_colors = (240, 240, 0, 255) * 20

point_colors = (0, 0, 0, 255) * 20
edge_colors = (255, 127, 127, 255) * 20
whi_colors = (190, 190, 190, 255) * 20

# # Scale up the vertices
vertices = [v * 100 for v in vertices]
vertices_axes = [v * 100 for v in vertices_axes]

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
program.vertex_list_indexed(
    20,
    GL_LINES,
    batch=batch,
    indices=edge_indices,
    vertices=('f', vertices),
    colors=('Bn', edge_colors)
)
program.vertex_list_indexed(
    20,
    GL_LINES,
    batch=batch,
    indices=dodecahedron_edge_indices,
    vertices=('f', vertices),
    colors=('Bn', whi_colors)
)
program.vertex_list_indexed(
    6,
    GL_LINES,
    batch=batch,
    indices=indices_axes,
    vertices=('f', vertices_axes),
    colors=('Bn', color_axes)
)

# draw the cube edges, all one colours
program.vertex_list(
    20,
    GL_POINTS,
    batch=batch,
    vertices=('f', vertices),
    colors=('Bn', point_colors)
)


@window.event
def on_draw():
    window.clear()
    batch.draw()


angle = 0


def update(dt: float):
    global angle
    angle += dt
    # spin it around all axes
    rotate_x_mat = Mat4.from_rotation(angle=angle,
                                      vector=Vec3(x=1, y=0, z=0))
    rotate_y_mat = Mat4.from_rotation(angle=0.3*angle,
                                      vector=Vec3(x=0, y=1, z=0))
    rotate_z_mat = Mat4.from_rotation(angle=0.7*angle,
                                      vector=Vec3(x=0, y=0, z=1))
    # upload the combined model matrix to the vertex shader model uniform
    model_mat = translate_mat @ rotate_x_mat @ rotate_y_mat @ rotate_z_mat
    program['model'] = model_mat


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
