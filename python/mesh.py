import maya.OpenMaya as om
import pymel.core as pm


class Mesh(object):
    """ Mesh """
    def __init__(self, faces):
        self.faces = faces

    def build(self, merge=True, tolerance=0.001):
        fn = om.MFnMesh()

        # Get Vertex List
        vertices = []
        for face in self.faces:
            for vertex in face.vertices:
                if vertex not in vertices:
                    vertices.append(vertex)

        vertexArray = om.MFloatPointArray()
        [vertexArray.append(v.MFloatPoint) for v in vertices]

        count = om.MIntArray()
        [count.append(int(len(f.vertices))) for f in self.faces]

        connections = om.MIntArray()
        for face in self.faces:
            for vertex in face.vertices:
                connections.append(vertices.index(vertex))

        fn.create(len(vertices), len(self.faces), vertexArray, count, connections)




class Face(object):
    """ Face of an object.  Stores Vertex in counter clockwise for outward normals"""
    def __init__(self, vertices):
        self.vertices = vertices
    
    def build(self, merge=True, tolerance=0.001):
        fn = om.MFnMesh()
        faceArray = om.MPointArray()
        faceArray.setLength(len(self.vertices))
        for i in range(len(self.vertices)):
            print self.vertices[i]
            faceArray.set(self.vertices[i].MPoint, i)
        fn.addPolygon(faceArray, merge, tolerance)

    
class Vertex(object):
    """Stores point position."""
    def __init__(self, *args):
        if len(args) == 1:
            self.position = args[0]
        else:
            self.position = [args[0], args[1], args[2]]
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2]
        self.MPoint = om.MPoint(self.x, self.y, self.z)
        self.MFloatPoint = om.MFloatPoint(self.x, self.y, self.z)

    def __eq__(self, other):
        if self.position == other.position:
            return True
        else:
            return False



def meshFromSelected():
    mesh = pm.PyNode('pCubeShape1')

    faces = []

    for i in range(mesh.numFaces()):
        vertices = [Vertex(pm.xform(v, q=1, ws=1, t=1)) for v in mesh.f[i].connectedVertices()]
        faces.append(Face(vertices))

    m = Mesh(faces)
    m.build()



meshFromSelected()


#
# vertices = []
# vertices.append(Vertex(10, 0, 0))
# vertices.append(Vertex(0, 1.98, 0))
# vertices.append(Vertex(0, 0, 1))
# vertices.append(Vertex(1, 1, 15))
#
# f1 = Face(vertices[:3])
# f2 = Face(vertices[1:])
#
# m = Mesh([f1, f2])
# m.build()

