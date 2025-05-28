import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
# from pyglet.gl import GL_LINES
from pyglet.gl import GL_TRIANGLES, GL_DEPTH_TEST
from pyglet.gl import glClearColor, glEnable
from pyglet.math import Mat4, Vec3
from math import sqrt


""" DODECAHEDRON """

window = pyglet.window.Window(1280, 720, caption="DODECAHEDRON")
glEnable(GL_DEPTH_TEST)
# set window background colour
glClearColor(1.0, 1.0, 1.0, 1.0)

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
# liist of vertices repeated four times, to separate colours
vertices = [
    -1, -1, -1,
    1, -1, -1,
    1,  1, -1,
    -1,  1, -1,

    -1, -1,  1,
    1, -1,  1,
    1,  1,  1,
    -1,  1,  1,

    0, -(1+h), -(1-h2),
    0, -(1+h),  (1-h2),
    0,  (1+h),  (1-h2),
    0,  (1+h), -(1-h2),

    -(1+h), -(1-h2), 0,
    -(1+h),  (1-h2), 0,
    (1+h),  (1-h2), 0,
    (1+h), -(1-h2), 0,

    -(1-h2), 0, -(1+h),
    -(1-h2), 0,  (1+h),
    (1-h2), 0,  (1+h),
    (1-h2), 0, -(1+h),


    -1, -1, -1,
    1, -1, -1,
    1,  1, -1,
    -1,  1, -1,

    -1, -1,  1,
    1, -1,  1,
    1,  1,  1,
    -1,  1,  1,

    0, -(1+h), -(1-h2),
    0, -(1+h),  (1-h2),
    0,  (1+h),  (1-h2),
    0,  (1+h), -(1-h2),

    -(1+h), -(1-h2), 0,
    -(1+h),  (1-h2), 0,
    (1+h),  (1-h2), 0,
    (1+h), -(1-h2), 0,

    -(1-h2), 0, -(1+h),
    -(1-h2), 0,  (1+h),
    (1-h2), 0,  (1+h),
    (1-h2), 0, -(1+h),


    -1, -1, -1,
    1, -1, -1,
    1,  1, -1,
    -1,  1, -1,

    -1, -1,  1,
    1, -1,  1,
    1,  1,  1,
    -1,  1,  1,

    0, -(1+h), -(1-h2),
    0, -(1+h),  (1-h2),
    0,  (1+h),  (1-h2),
    0,  (1+h), -(1-h2),

    -(1+h), -(1-h2), 0,
    -(1+h),  (1-h2), 0,
    (1+h),  (1-h2), 0,
    (1+h), -(1-h2), 0,

    -(1-h2), 0, -(1+h),
    -(1-h2), 0,  (1+h),
    (1-h2), 0,  (1+h),
    (1-h2), 0, -(1+h),


    -1, -1, -1,
    1, -1, -1,
    1,  1, -1,
    -1,  1, -1,

    -1, -1,  1,
    1, -1,  1,
    1,  1,  1,
    -1,  1,  1,

    0, -(1+h), -(1-h2),
    0, -(1+h),  (1-h2),
    0,  (1+h),  (1-h2),
    0,  (1+h), -(1-h2),

    -(1+h), -(1-h2), 0,
    -(1+h),  (1-h2), 0,
    (1+h),  (1-h2), 0,
    (1+h), -(1-h2), 0,

    -(1-h2), 0, -(1+h),
    -(1-h2), 0,  (1+h),
    (1-h2), 0,  (1+h),
    (1-h2), 0, -(1+h)
]

# indices = [
#     0,  8,  9,  4, 12,
#     0, 12, 13,  3, 16,
#     0, 16, 19,  1,  8,

#     8,  1, 15,  5,  9,
#     12, 4, 17, 7, 13,
#     16, 3, 11, 2, 19,

#     9, 5, 18, 17, 4,
#     13, 7, 10, 11, 3,
#     19, 2, 14, 15, 1,

#     15, 14, 6, 18, 5,
#     17, 18, 6, 10, 7,
#     11, 10, 6, 14, 2
# ]
# indices = [
#     0,  8,  9,  9, 4, 0, 0, 4, 12,          # blu
#     0, 12, 13, 13, 3, 0, 0, 3, 16,          # ora
#     0, 16, 19, 19, 1, 0, 0, 1,  8,          # yel

#     8,  1, 15, 15, 5,  8, 8, 5,  9,         # ora
#     12, 4, 17, 17, 7, 12, 12, 7, 13,        # red
#     16, 3, 11, 11, 2, 16, 16, 2, 19,        # red

#     9,  5, 18, 18, 17, 9, 9, 17, 4,         # yel
#     13, 7, 10, 10, 11, 13, 13, 11, 3,       # blu
#     19, 2, 14, 14, 15, 19, 19, 15, 1,       # blu

#     15, 14, 6, 6, 18, 15, 15, 18, 5,        # red
#     17, 18, 6, 6, 10, 17, 17, 10, 7,        # ora
#     11, 10, 6, 6, 14, 11, 11, 14, 2         # yel
# ]
# TODO add 20 to ora, 40 to red, 60 to yel
# TODO redo colors 0 to 19 blu, 20 to 39 ora etc
indices = [
    0,  8,  9,  9, 4, 0, 0, 4, 12,          # blu
    13, 7, 10, 10, 11, 13, 13, 11, 3,       # blu
    19, 2, 14, 14, 15, 19, 19, 15, 1,       # blu

    20, 32, 33, 33, 23, 20, 20, 23, 36,     # ora
    28,  21, 35, 35, 25,  28, 28, 25,  29,  # ora
    37, 38, 26, 26, 30, 37, 37, 30, 27,     # ora

    52, 44, 57, 57, 47, 52, 52, 47, 53,     # red
    56, 43, 51, 51, 42, 56, 56, 42, 59,     # red
    55, 54, 46, 46, 58, 55, 55, 58, 45,     # red

    60, 76, 79, 79, 61, 60, 60, 61,  68,    # yel
    69,  65, 78, 78, 77, 69, 69, 77, 64,    # yel
    71, 70, 66, 66, 74, 71, 71, 74, 62      # yel
]
# for index1 in range(20):
#     for index2 in range(20):
#         i1 = index1 * 3
#         i2 = index2 * 3
#         if index1 != index2:
#             dx = vertices[i1] - vertices[i2]
#             dy = vertices[i1 + 1] - vertices[i2 + 1]
#             dz = vertices[i1 + 2] - vertices[i2 + 2]
#             dd = dx * dx + dy * dy + dz * dz
#             if dd < 1.6:
#                 print((index1, index2, dd))

# Just some colours
colors_blu = (
    0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255,
    0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255,
    0, 0, 255, 255, 0, 0, 255, 255)
colors_ora = (
    255, 127, 0, 255, 255, 127, 0, 255, 255, 127, 0, 255, 255, 127, 0, 255,
    255, 127, 0, 255, 255, 127, 0, 255, 255, 127, 0, 255, 255, 127, 0, 255,
    255, 127, 0, 255, 255, 127, 0, 255
)
colors_red = (
    255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255,
    255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255,
    255, 0, 0, 255, 255, 0, 0, 255
)
colors_yel = (
    255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255,
    255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255,
    255, 255, 0, 255, 255, 255, 0, 255
)
# need 20 of each color
colors = colors_blu + colors_blu + colors_ora + colors_ora \
    + colors_red + colors_red + colors_yel + colors_yel

# # Scale up the vertices
vertices = [v * 100 for v in vertices]

program.vertex_list_indexed(80,
                            GL_TRIANGLES,
                            batch=batch,
                            indices=indices,
                            vertices=('f', vertices),
                            colors=('Bn', colors)
                            )


@window.event
def on_draw():
    window.clear()
    batch.draw()


angle = 0


def update(dt: float):
    global angle
    angle += dt
    # upload the combined model matrix to the vertex shader model uniform
    rotate_mat = Mat4.from_rotation(angle=angle,
                                    vector=Vec3(x=0.707, y=0.707, z=0))
    model_mat = translate_mat @ rotate_mat
    program['model'] = model_mat


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
