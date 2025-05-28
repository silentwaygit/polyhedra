import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_LINES
from pyglet.gl import GL_TRIANGLES, GL_DEPTH_TEST, GL_POINTS
from pyglet.gl import glClearColor, glEnable, glPointSize, glLineWidth
from pyglet.math import Mat4, Vec3
from math import sqrt


""" ICOSAHEDRON """
""" Three golden ratio rectangles, vertices and coloured edges """

# Vertices at corners of three mutually perpendicular golden ratio rectangles.
# 20 external equilateral triangles on these same vertices.

window = pyglet.window.Window(1280, 720, caption="ICOSAHEDRON")
glEnable(GL_DEPTH_TEST)
# set window background colour
glClearColor(1.0, 1.0, 1.0, 1.0)
glPointSize(10)
glLineWidth(0.3)

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

# icosahedron built on golden ratio
g = (1.0 + sqrt(5.0)) / 2.0                 # approx 1.618
# g = 1.61803399
h = 1.0

# Vertices are defined by 3 orthogonal golden ratio rectangles
rx = (0., -h, -g,
      0., -h,  g,
      0.,  h,  g,
      0.,  h, -g)
ry = (-g, 0., -h,
      g, 0., -h,
      g, 0.,  h,
      -g, 0.,  h)
rz = (-h, -g, 0.,
      -h,  g, 0.,
      h,  g, 0.,
      h, -g, 0.)

# Each rectangle is drawn as 2 triangles
indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           8, 9, 10, 10, 11, 8]

# Each rectangle has its own colour: red, green, and blue assign to 4 vertices
colors_x = (255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255)
colors_y = (0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255, 0, 255)
colors_z = (0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255)

black_color = (0, 0, 0, 255) * 12

# Concatenate the rectangle vertex colours
colors = colors_x + colors_y + colors_z
# Concatenate the vertices
vertices = rx + ry + rz

# for index1 in range(12):
#     for index2 in range(12):
#         i1 = index1 * 3
#         i2 = index2 * 3
#         if index1 != index2:
#             dx = vertices[i1] - vertices[i2]
#             dy = vertices[i1 + 1] - vertices[i2 + 1]
#             dz = vertices[i1 + 2] - vertices[i2 + 2]
#             dd = dx * dx + dy * dy + dz * dz
#             if dd < 4.3:
#                 print((index1, index2, dd))

indices_external = [0, 3, 4, 0, 3, 5, 0, 5, 11, 0, 4, 8, 0, 8, 11,
                    1, 2, 6, 1, 2, 7, 1, 6, 11, 1, 7, 8, 1, 8, 11,
                    2, 6, 10, 2, 7, 9, 2, 9, 10,
                    3, 4, 9, 3, 5, 10, 3, 9, 10,
                    4, 7, 8, 4, 7, 9,
                    5, 6, 10, 5, 6, 11]

indices_lines = [
    2, 10, 10,  6,  6, 2,  2, 9,   2, 7,
    2,  1, 10,  5, 10, 3, 10, 9,   9, 3,
    9,  4,  9,  7,  1, 6,  1, 11,  1, 8,
    1,  7,  6, 11,  6, 5,  5, 11,  5, 0,
    5,  3,  3,  0,  3, 4,  7,  4,  7, 8,
    8,  0,  0,  4,  4, 8,  8, 11, 11, 0
]

# indices += indices_external

# Scale up the vertices
vertices = [v * 100 for v in vertices]

program.vertex_list_indexed(12,
                            GL_TRIANGLES,
                            batch=batch,
                            indices=indices,
                            vertices=('f', vertices),
                            colors=('Bn', colors)
                            )

program.vertex_list(
    12,
    GL_POINTS,
    batch=batch,
    vertices=('f', vertices),
    colors=('Bn', black_color)
)
program.vertex_list_indexed(
    12,
    GL_LINES,
    batch=batch,
    indices=indices_lines,
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
