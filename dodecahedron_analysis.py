from math import sqrt

""" DODECAHEDRON """

# Regular dodecahedron built on golden ratio (ref wikipedia.com/dodecahedron)
h = 2.0 / (1.0 + sqrt(5.0))                 # approx 0.618
h2 = h * h

# phi = (1.0 + sqrt(5.0)) / 2.0
# h is 1/phi
# h is phi-1
# h2 is 2-phi
# print(h, h2, phi, phi - 1, 2 - phi)

# Vertices are defined (ref wikipedia)
vertices = [
    -1, -1, -1,                 # vertex 0
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
    (1-h2), 0, -(1+h)           # vertex 19
]

vertex_count = len(vertices) // 3

for index in range(vertex_count):
    x = vertices[index * 3]
    y = vertices[index * 3 + 1]
    z = vertices[index * 3 + 2]
    print(index, x, y, z)

# distances = []
adjcnt = []
square = []
golden = []
minor = []
other = []
v1 = 8
for v2 in range(vertex_count):
    x2 = (vertices[v1 * 3] - vertices[v2 * 3]) ** 2
    y2 = (vertices[v1 * 3 + 1] - vertices[v2 * 3 + 1]) ** 2
    z2 = (vertices[v1 * 3 + 2] - vertices[v2 * 3 + 2]) ** 2
    dist = sqrt(x2 + y2 + z2) / 2.
    description = ""
    if 0 == dist:
        description = "VERTEX"
    elif 0.999 < dist < 1.001:
        description = "adjacent"
    elif 1.414 < dist < 1.415:
        description = "square"
    elif 0.618 < dist < 0.619:
        description = "minor"
    elif 1.618 < dist < 1.619:
        description = "golden"
    else:
        description = "other"

    if description == "adjacent":
        adjcnt.append(v2)
    if description == "square":
        square.append(v2)
    if description == "golden":
        golden.append(v2)
    if description == "minor":
        minor.append(v2)
    if description == "other":
        other.append(v2)

    print(v1, v2, dist, description)
print("VERTEX:", v1)
print("Adjcnt:", adjcnt)
print("square:", square)
print("golden:", golden)
print("minor :", minor)
print("other :", other)
