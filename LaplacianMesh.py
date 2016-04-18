import sys
sys.path.append("S3DGLPy")
from PolyMesh import *
from Primitives3D import *
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import lsqr, cg, eigsh
import matplotlib.pyplot as plt
import scipy.io as sio

WEIGHT = 1.0 

##############################################################
##                  Laplacian Mesh Editing                  ##
##############################################################

#Purpose: To return a sparse matrix representing a Laplacian matrix with
#the graph Laplacian (D - A) in the upper square part and anchors as the
#lower rows
#Inputs: mesh (polygon mesh object), anchorsIdx (indices of the anchor points)
#Returns: L (An (N+K) x N sparse matrix, where N is the number of vertices
#and K is the number of anchors)
def getLaplacianMatrixUmbrella(mesh, anchorsIdx):
    N = mesh.VPos.shape[0] # N x 3
    K = anchorsIdx.shape[0]
    I = []
    J = []
    V = []

    # Build sparse Laplacian Matrix coordinates and values
    for i in range(N):
        neighbors = mesh.vertices[i].getVertexNeighbors()
        indices = map(lambda x: x.ID, neighbors)
        n = len(indices)
        I = I + ([i] * (n + 1)) # repeated row
        J = J + indices + [i] # column indices and this row
        V = V + ([-1] * n) + [n] # negative weights and row degree

    # augment Laplacian matrix with anchor weights  
    for i in range(K):
        I = I + [N + i]
        J = J + [anchorsIdx[i]]
        V = V + [WEIGHT] # default anchor weight
    
    L = sparse.coo_matrix((V, (I, J)), shape=(N+K, N)).tocsr()
    
    return L

#Purpose: To return a sparse matrix representing a laplacian matrix with
#cotangent weights in the upper square part and anchors as the lower rows
#Inputs: mesh (polygon mesh object), anchorsIdx (indices of the anchor points)
#Returns: L (An (N+K) x N sparse matrix, where N is the number of vertices
#and K is the number of anchors)
def getLaplacianMatrixCotangent(mesh, anchorsIdx):
    N = mesh.VPos.shape[0] # N x 3
    K = anchorsIdx.shape[0]
    I = []
    J = []
    V = []

    # Build sparse Laplacian Matrix coordinates and values
    for i in range(N):
        vertex = mesh.vertices[i]
        neighbors = vertex.getVertexNeighbors()
        indices = map(lambda x: x.ID, neighbors)
        weights = []
        n = len(indices)
        I = I + ([i] * (n + 1)) # repeated row
        J = J + indices + [i] # column indices and this row
        for j in range(n):
            neighbor = neighbors[j]
            edge = getEdgeInCommon(vertex, neighbor)
            faces = [edge.f1, edge.f2]
            cotangents = []

            for f in range(2):
                if faces[f]:
                    P = mesh.VPos[filter(lambda v: v not in [neighbor, vertex], faces[f].getVertices())[0].ID]
                    (u, v) = (mesh.VPos[vertex.ID] - P, mesh.VPos[neighbor.ID] - P)
                    cotangents.append(np.dot(u, v) / np.sqrt(np.sum(np.square(np.cross(u, v)))))

            weights.append(-0.5 * np.sum(cotangents)) # cotangent weights
            
        V = V + weights + [(-1 * np.sum(weights))] # n negative weights and row vertex sum

    # augment Laplacian matrix with anchor weights  
    for i in range(K):
        I = I + [N + i]
        J = J + [anchorsIdx[i]]
        V = V + [WEIGHT] # default anchor weight

    L = sparse.coo_matrix((V, (I, J)), shape=(N+K, N)).tocsr()

    return L

#Purpose: Given a mesh, to perform Laplacian mesh editing by solving the system
#of delta coordinates and anchors in the least squared sense
#Inputs: mesh (polygon mesh object), anchors (a K x 3 numpy array of anchor
#coordinates), anchorsIdx (a parallel array of the indices of the anchors)
#Returns: Nothing (should update mesh.VPos)
def solveLaplacianMesh(mesh, anchors, anchorsIdx, cotangent=True):
    N = mesh.VPos.shape[0] # N x 3
    K = anchorsIdx.shape[0]

    operator = (getLaplacianMatrixUmbrella, getLaplacianMatrixCotangent)

    L = operator[1](mesh, anchorsIdx) if cotangent else operator[0](mesh, anchorsIdx)
    delta = np.array(L.dot(mesh.VPos))
    
    # augment delta solution matrix with weighted anchors
    for i in range(K):
        delta[N + i, :] = WEIGHT * anchors[i, :]

    # update mesh vertices with least-squares solution
    for k in range(3):
        mesh.VPos[:, k] = lsqr(L, delta[:, k])[0]
    
    print "TODO"

#Purpose: Given a few RGB colors on a mesh, smoothly interpolate those colors
#by using their values as anchors and 
#Inputs: mesh (polygon mesh object), anchors (a K x 3 numpy array of anchor
#coordinates), anchorsIdx (a parallel array of the indices of the anchors)
#Returns: Nothing (should update mesh.VPos)
def smoothColors(mesh, colors, colorsIdx):
    N = mesh.VPos.shape[0]
    colors = np.zeros((N, 3)) #dummy values (all black)
    #TODO: Finish this
    return colors

#Purpose: Given a mesh, to smooth it by subtracting off the delta coordinates
#from each vertex, normalized by the degree of that vertex
#Inputs: mesh (polygon mesh object)
#Returns: Nothing (should update mesh.VPos)
def doLaplacianSmooth(mesh):
    print "TODO"
    #TODO: Finish this

#Purpose: Given a mesh, to sharpen it by adding back the delta coordinates
#from each vertex, normalized by the degree of that vertex
#Inputs: mesh (polygon mesh object)
#Returns: Nothing (should update mesh.VPos)
def doLaplacianSharpen(mesh):
    print "TODO"
    #TODO: Finish this

#Purpose: Given a mesh and a set of anchors, to simulate a minimal surface
#by replacing the rows of the laplacian matrix with the anchors, setting
#those "delta coordinates" to the anchor values, and setting the rest of the
#delta coordinates to zero
#Inputs: mesh (polygon mesh object), anchors (a K x 3 numpy array of anchor
#coordinates), anchorsIdx (a parallel array of the indices of the anchors)
#Returns: Nothing (should update mesh.VPos)
def makeMinimalSurface(mesh, anchors, anchorsIdx):
    print "TODO"
    #TODO: Finish this

##############################################################
##        Spectral Representations / Heat Flow              ##
##############################################################

#Purpose: Given a mesh, to compute first K eigenvectors of its Laplacian
#and the corresponding eigenvalues
#Inputs: mesh (polygon mesh object), K (number of eigenvalues/eigenvectors)
#Returns: (eigvalues, eigvectors): a tuple of the eigenvalues and eigenvectors
def getLaplacianSpectrum(mesh, K):
    #TODO: Finish this
    return (None, None)

#Purpose: Given a mesh, to use the first K eigenvectors of its Laplacian
#to perform a lowpass filtering
#Inputs: mesh (polygon mesh object), K (number of eigenvalues/eigenvectors)
#Returns: Nothing (should update mesh.VPos)
def doLowpassFiltering(mesh, K):
    print "TODO"
    #TODO: Finish this
    
#Purpose: Given a mesh, to simulate heat flow by projecting initial conditions
#onto the eigenvectors of the Laplacian matrix, and then to sum up the heat
#flow of each eigenvector after it's decayed after an amount of time t
#Inputs: mesh (polygon mesh object), eigvalues (K eigenvalues), 
#eigvectors (an NxK matrix of eigenvectors computed by your laplacian spectrum
#code), t (the time to simulate), initialVertices (indices of the verticies
#that have an initial amount of heat), heatValue (the value to put at each of
#the initial vertices at the beginning of time
#Returns: heat (a length N array of heat values on the mesh)
def getHeat(mesh, eigvalues, eigvectors, t, initialVertices, heatValue = 100.0):
    N = mesh.VPos.shape[0]
    heat = np.zeros(N) #Dummy value
    return heat #TODO: Finish this

#Purpose: Given a mesh, to approximate its curvature at some measurement scale
#by recording the amount of heat that stays at each vertex after a unit impulse
#of heat is applied.  This is called the "Heat Kernel Signature" (HKS)
#Inputs: mesh (polygon mesh object), K (number of eigenvalues/eigenvectors to use)
#t (the time scale at which to compute the HKS)
#Returns: hks (a length N array of the HKS values)
def getHKS(mesh, K, t):
    N = mesh.VPos.shape[0]
    hks = np.zeros(N) #Dummy value
    return hks #TODO: Finish this

##############################################################
##                Parameterization/Texturing               ##
##############################################################

#Purpose: Given 4 vertex indices on a quadrilateral, to anchor them to the 
#square and flatten the rest of the mesh inside of that square
#Inputs: mesh (polygon mesh object), quadIdxs (a length 4 array of indices
#into the mesh of the four points that are to be anchored, in CCW order)
#Returns: nothing (update mesh.VPos)
def doFlattening(mesh, quadIdxs):
    print "TODO"
    #TODO: Finish this

#Purpose: Given 4 vertex indices on a quadrilateral, to anchor them to the 
#square and flatten the rest of the mesh inside of that square.  Then, to 
#return these to be used as texture coordinates
#Inputs: mesh (polygon mesh object), quadIdxs (a length 4 array of indices
#into the mesh of the four points that are to be anchored, in CCW order)
#Returns: U (an N x 2 matrix of texture coordinates)
def getTexCoords(mesh, quadIdxs):
    N = mesh.VPos.shape[0]
    U = np.zeros((N, 2)) #Dummy value
    return U #TODO: Finish this

if __name__ == '__main__':
    print "TODO"
