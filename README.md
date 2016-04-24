# laplacian-meshes

Please view this README rendered by GitHub at https://github.com/bmershon/laplacian-meshes

*All images, words, and code contained in this repository may be reproduced so long as the original author is given credit (Chris Tralie and Brooks Mershon).*

This assignment was completed as part of a course in 3D Digital Geometry (Math 290) taken at Duke University during Spring 2016. The course was taught by [Chris Tralie](http://www.ctralie.com/).

## Laplacian Mesh Editing

### Laplacian Matrix

The Laplacian operator is encoded as a sparse matrix **L**, with anchor rows appended to encode the weights of the anchor vertices (which may be manually moved, hence the name Laplacian *editing*).

### Cotangent Weights

Rather than using equal weights for each neighboring vertex in the Laplacian operator, we can attempt to correct for irregular mesh resolutions by using [Cotangent Weights](http://www.ctralie.com/Teaching/COMPSCI290/Assignments/Group3_LaplacianMesh/).

*Homer's arms are raised by placing an anchor at a vertex on a finger tip that has been displaced vertically. A small handful of anchors placed symmetrically about his body help to restrict edits to his arms. Cotangent weighting is used here.*

<img src="img/homer.png" width="49%">
<img src="img/homer-arms-raised.png" width="49%">

## Color Interpolation

<img src="img/teapot-coloring.png" width="100%">

## Laplacian Smoothing and Sharpening

### Smoothing (Umbrella Weighting)

*We can smooth the teapot by iteratively pulling each vertex closer to the centroid of its neighbors.*

<img src="img/teapot-smooth-0.png" width="24.5%">
<img src="img/teapot-smooth-1.png" width="24.5%">
<img src="img/teapot-smooth-2.png" width="24.5%">
<img src="img/teapot-smooth-3.png" width="24.5%">

### Sharpening (Umbrella Weighting)

*We can sharpen the teapot by iteratively pulling each vertex farther away from the centroid of its neighbors. Self-intersection can cetainly be made worse, as a single iteration of sharpening performed on the teapot demonstrates.*

<img src="img/teapot-sharpen-0.png" width="49%">
<img src="img/teapot-sharpen-1.png" width="49%">
