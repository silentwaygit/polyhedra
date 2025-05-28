import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
# from pyglet.gl import GL_LINES
from pyglet.gl import GL_TRIANGLES, GL_DEPTH_TEST
from pyglet.gl import glClearColor, glEnable, glLineWidth
from pyglet.math import Mat4, Vec3
from math import sqrt
# from math import  pi


""" DODECAHEDRON """
""" Filled faces - 3 blue, 3 orange, 3 red, 3 yellow """

window = pyglet.window.Window(1280, 720, caption="DODECAHEDRON")
glEnable(GL_DEPTH_TEST)
glLineWidth(10)
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
vertices = [
    -1, -1, -1,                 # vertex 0
    1, -1, -1,
    1,  1, -1,
    -1,  1, -1,

    -1, -1,  1,                 # 4
    1, -1,  1,
    1,  1,  1,                  # 6 top edge
    -1,  1,  1,                 # 7 top edge

    0, -(1+h), -(1-h2),         # 8
    0, -(1+h),  (1-h2),         # 9
    0,  (1+h),  (1-h2),
    0,  (1+h), -(1-h2),

    -(1+h), -(1-h2), 0,         # 12
    -(1+h),  (1-h2), 0,
    (1+h),  (1-h2), 0,
    (1+h), -(1-h2), 0,

    -(1-h2), 0, -(1+h),
    -(1-h2), 0,  (1+h),
    (1-h2), 0,  (1+h),
    (1-h2), 0, -(1+h)           # vertex 19
]

# pentagon faces subdivided into trangles
indices_blu = [
    0,  8,  9,  9, 4, 0, 0, 4, 12,          # blu
    13, 7, 10, 10, 11, 13, 13, 11, 3,       # blu
    19, 2, 14, 14, 15, 19, 19, 15, 1,       # blu
]
indices_ora = [
    0, 12, 13, 13, 3, 0, 0, 3, 16,          # ora
    8,  1, 15, 15, 5,  8, 8, 5,  9,         # ora
    17, 18, 6, 6, 10, 17, 17, 10, 7,        # ora
]
indices_red = [
    12, 4, 17, 17, 7, 12, 12, 7, 13,        # red
    16, 3, 11, 11, 2, 16, 16, 2, 19,        # red
    15, 14, 6, 6, 18, 15, 15, 18, 5,        # red
]
indices_yel = [
    0, 16, 19, 19, 1, 0, 0, 1,  8,          # yel
    9,  5, 18, 18, 17, 9, 9, 17, 4,         # yel
    11, 10, 6, 6, 14, 11, 11, 14, 2         # yel
]
indices_blk_line = [
    # bottom blu poly, clockw. "outermost net pentagon"
    0, 12, 12, 4, 4, 9, 9, 8, 8, 0,     # (9, 8) is bottom-most "gutter-ridge"
    # top edge - roof ridge - shared by 2 roof-slopes, one yel + one blu
    11, 10,
    # rest of top roof poly yel, clockw. "centre of net"
    11, 2, 2, 14, 14, 6, 6, 10,
    # rest of top roof poly blu, clockw.
    10, 7, 7, 13, 13, 3, 3, 11,
    # sloping poly ora under roof, clockw.
    6, 18, 18, 17, 17, 7,       # (18, 17) is horizontal at y=0
    # sloping poly red under roof, clockw.
    3, 16, 16, 19, 19, 2,       # (16, 19) is horizontal at y=0
    # four vertical walls: 2 under blu roof poly + 2 under yel roof poly
    # rest of ora poly under blu roof poly, clockw.
    13, 12, 12, 0, 0, 16,       # (13, 12) is vertical.
    #                             (12, 0) is duplicate in blu bottom
    # rest of red poly under blu roof
    17, 4,                      # (4, 12) is duplicate in blue bottom,
    # rest of red poly under yel roof poly, clockw.
    14, 15, 15, 5, 5, 18,        # (15, 14) is vertical
    # rest of blu poly under yel roof
    19, 1, 1, 15,
    # last two bits of ora poly sharing (9,8) gutter
    1, 8, 9, 5
    # TODO check eack line drawn only once
]

# Just some colours
colors_blu = (0, 0, 200, 255) * 20
colors_ora = (255, 127, 0, 255) * 20
colors_red = (200, 0, 0, 255) * 20
colors_yel = (200, 200, 0, 255) * 20
colors_blk = (0, 0, 0, 255) * 20


# # Scale up the vertices
vertices = [v * 100 for v in vertices]

# blue face batch
program.vertex_list_indexed(
    20,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_blu,
    vertices=('f', vertices),
    colors=('Bn', colors_blu)
)
# orange face batch
program.vertex_list_indexed(
    20,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_ora,
    vertices=('f', vertices),
    colors=('Bn', colors_ora)
)
# red face batch
program.vertex_list_indexed(
    20,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_red,
    vertices=('f', vertices),
    colors=('Bn', colors_red)
)
# yellow face batch
program.vertex_list_indexed(
    20,
    GL_TRIANGLES,
    batch=batch,
    indices=indices_yel,
    vertices=('f', vertices),
    colors=('Bn', colors_yel)
)
# program.vertex_list_indexed(
#     20,
#     GL_LINES,
#     batch=batch,
#     indices=indices_blk_line,
#     vertices=('f', vertices),
#     colors=('Bn', colors_blk)
# )


@window.event
def on_draw():
    window.clear()
    batch.draw()


angle = 0


def update(dt: float):
    global angle
    angle += dt
    # angle = pi/2.0
    # upload the combined model matrix to the vertex shader model uniform
    rotate_mat = Mat4.from_rotation(angle=angle,
                                    vector=Vec3(x=0, y=1, z=0))
    model_mat = translate_mat @ rotate_mat
    program['model'] = model_mat


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
