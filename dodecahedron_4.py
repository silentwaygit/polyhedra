import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
# from pyglet.gl import GL_LINES
from pyglet.gl import (GL_DEPTH_TEST,       # GL_POINTS,
                       GL_LINES)
# from pyglet.gl import GL_TRIANGLES, GL_LINES
# from pyglet.gl import GL_POINT_SIZE
from pyglet.gl import glClearColor, glEnable, glLineWidth, glPointSize
from pyglet.math import Mat4, Vec3
from math import sqrt


""" DODECAHEDRON """
""" Five embedded cube frames - colour """

window = pyglet.window.Window(1280, 720, caption="DODECAHEDRON")
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
# pentagon faces
indices = [
    0,  8,  9,  4, 12,        # blu
    0, 12, 13,  3, 16,        # ora
    0, 16, 19,  1,  8,        # red

    8,  1, 15,  5,  9,        # ora
    12, 4, 17, 7, 13,         # red
    16, 3, 11, 2, 19,         # red

    9, 5, 18, 17, 4,          # yel
    13, 7, 10, 11, 3,         # blu
    19, 2, 14, 15, 1,         # blu

    15, 14, 6, 18, 5,         # red
    17, 18, 6, 10, 7,         # ora
    11, 10, 6, 14, 2          # yel
]

# embedded cubes
red_cube_indices = [
    0, 1, 1, 2, 2, 3, 3, 0,
    4, 5, 5, 6, 6, 7, 7, 4,
    0, 4, 1, 5, 2, 6, 3, 7
]
grn_cube_indices = [
    13, 17, 17,  6,  6, 11, 11, 13,
    0,   9,  9, 15, 15, 19, 19,  0,
    13,  0, 17,  9,  6, 15, 11, 19
]
blu_cube_indices = [
    15, 2,  2, 10, 10, 18, 18, 15,
    8, 16, 16, 13, 13,  4,  4,  8,
    15, 8, 10, 13,  2, 16, 18,  4
]
ora_cube_indices = [
    12, 17, 17,  5,  5,  8,  8, 12,
    3,  10, 10, 14, 14, 19, 19,  3,
    12,  3, 17, 10,  5, 14,  8, 19
]
yel_cube_indices = [
    16, 1, 1, 9, 9, 12, 12, 16,
    11, 14, 14, 18, 18, 7, 7, 11,
    16, 11, 1, 14, 9, 18, 12, 7
]

# Just some colours
red_colors = (255, 0, 0, 255) * 20
grn_colors = (0, 255, 0, 255) * 20
blu_colors = (0, 0, 255, 255) * 20
ora_colors = (255, 127, 0, 255) * 20
yel_colors = (255, 255, 0, 255) * 20


# # print coords of vertex[ico]
# ico = 12
# print(ico, ": ",
#       vertices[3 * ico],vertices[3 * ico + 1], vertices[3 * ico + 2])
# ico = 14
# print(ico, ": ",
#       vertices[3 * ico], vertices[3 * ico + 1], vertices[3 * ico + 2])

# # vertex distance calculation fr vertex[v_dist]
# v_dist = 18
# count_vertices = 20
# for index1 in range(v_dist, v_dist + 1):
#     for index2 in range(count_vertices):
#         i1 = index1 * 3
#         i2 = index2 * 3
#         if index1 != index2:
#             dx = vertices[i1] - vertices[i2]
#             dy = vertices[i1 + 1] - vertices[i2 + 1]
#             dz = vertices[i1 + 2] - vertices[i2 + 2]
#             dd = dx * dx + dy * dy + dz * dz
#             if 3.9 < dd < 4.1:
#                 print((index1, index2, dd))

# # Scale up the vertices
vertices = [v * 100 for v in vertices]


program.vertex_list_indexed(
    20,
    GL_LINES,
    batch=batch,
    indices=red_cube_indices,
    vertices=('f', vertices),
    colors=('Bn', red_colors)
)
program.vertex_list_indexed(
    20,
    GL_LINES,
    batch=batch,
    indices=grn_cube_indices,
    vertices=('f', vertices),
    colors=('Bn', grn_colors)
)
program.vertex_list_indexed(
    20,
    GL_LINES,
    batch=batch,
    indices=blu_cube_indices,
    vertices=('f', vertices),
    colors=('Bn', blu_colors)
)
program.vertex_list_indexed(
    20,
    GL_LINES,
    batch=batch,
    indices=ora_cube_indices,
    vertices=('f', vertices),
    colors=('Bn', ora_colors)
)
program.vertex_list_indexed(
    20,
    GL_LINES,
    batch=batch,
    indices=yel_cube_indices,
    vertices=('f', vertices),
    colors=('Bn', yel_colors)
)

# label = pyglet.text.Label(
#     'X', font_name='Times New Roman', font_size=36,
#     color=(250, 0, 0, 255),
#     x=vertices[0]+640, y=vertices[1]+360, z=vertices[2],
#     # x=window.width//2, y=window.height//2,
#     anchor_x='center', anchor_y='center'
#     #   batch=batch
# )

# program.vertex_list_indexed(
#     20,
#     GL_LINES,
#     batch=batch,
#     indices=cube_indices,
#     vertices=('f', vertices),
#     colors=('Bn', colors)
# )


@window.event
def on_draw():
    window.clear()
    batch.draw()


angle = 0


def update(dt: float):
    global angle
    angle += dt
    # upload the combined model matrix to the vertex shader model uniform
    rotate_y_mat = Mat4.from_rotation(angle=angle, vector=Vec3(x=0, y=1, z=0))
    rotate_x_mat = Mat4.from_rotation(angle=angle, vector=Vec3(x=1, y=0, z=0))
    model_mat = translate_mat @ rotate_y_mat @ rotate_x_mat
    program['model'] = model_mat


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
