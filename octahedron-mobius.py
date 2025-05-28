import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_LINES
from pyglet.gl import GL_TRIANGLES, GL_DEPTH_TEST
from pyglet.gl import glClearColor, glEnable, glLineWidth
from pyglet.math import Mat4, Vec3


""" OCTAHEDRON """

window = pyglet.window.Window(1280, 720, caption="OCTAHEDRON - MOBIUS")
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

# Vertices are defined (ref wikipedia)
vertices = [
    1, 0, 0,
    0, 1, 0,
    0, 0, 1,

    -1, 0, 0,
    0, -1, 0,
    0, 0, -1
]

indices_blu = [
    0, 1, 2,
    3, 4, 5
]
indices_ora = [
    0, 2, 4,
    5, 3, 1
]
indices_red = [
    0, 3, 4,
    1, 2, 5
]
indices_yel = [
    0, 4, 1,
    2, 3, 5
]
indices_edge = [
    0, 1,  0, 2,  0, 3,  0, 4,
    1, 2,  2, 3,  3, 4,  4, 1,
    5, 1,  5, 2,  5, 3,  5, 4
]

# Just some colours
colors_blu = (0, 0, 200, 255) * 6
colors_ora = (255, 127, 0, 255) * 6
colors_red = (200, 0, 0, 255) * 6
colors_yel = (200, 200, 0, 255) * 6
colors_whi = (255, 255, 255, 255) * 6

# # Scale up the vertices
vertices = [v * 200 for v in vertices]

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
# # yellow face batch
# program.vertex_list_indexed(
#     6,
#     GL_TRIANGLES,
#     batch=batch,
#     indices=indices_yel,
#     vertices=('f', vertices),
#     colors=('Bn', colors_yel)
# )
# edges
program.vertex_list_indexed(
    6,
    GL_LINES,
    batch=batch,
    indices=indices_edge,
    vertices=('f', vertices),
    colors=('Bn', colors_whi)
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
