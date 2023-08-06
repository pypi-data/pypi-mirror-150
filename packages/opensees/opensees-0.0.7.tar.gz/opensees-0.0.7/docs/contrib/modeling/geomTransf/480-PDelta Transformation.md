# PDelta

This command is used to construct the P-Delta Coordinate
Transformation (PDeltaCrdTransf) object, which performs a linear
geometric transformation of beam stiffness and resisting force from the
basic system to the global coordinate system, considering second-order
P-Delta effects. 
>NOTE: $P$ - $\Delta$ effects do not include $P$ - 
$\delta$ effects.

<p>For a two-dimensional problem:</p>

```tcl
geomTransf PDelta $transfTag < -jntOffset $dXi $dY $dXj $dYj>
```
<p>For a three-dimensional problem:</p>

```tcl
geomTransf PDelta $transfTag $vecxzX $vecxzY $vecxzZ
        < -jntOffset $dXi $dYi $dZi $dXj $dYj $dZj >
```
<hr />
<table>
<tbody>
<tr class="odd">
<td><code class="parameter-table-variable">transfTag</code></td>
<td><p>integer tag identifying transformation</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">vecxzX vecxzY vecxzZ</code></p></td>
<td><p>X, Y, and Z components of vecxz, the vector used to define the
local x-z plane of the local-coordinate system. The local y-axis is
defined by taking the cross product of the vecxz vector and the
x-axis.</p>
<p>These components are specified in the global-coordinate system X,Y,Z
and define a vector that is in a plane parallel to the x-z plane of the
local-coordinate system.</p>
<p>These items need to be specified for the three-dimensional
problem.</p></td>
</tr>
<tr class="odd">
<td><p><code>dXi dYi dZi</code></p></td>
<td><p>joint offset values -- offsets specified with respect to the
global coordinate system for element-end node i (the number of arguments
depends on the dimensions of the current model). The offset vector is
oriented from node i to node j as shown in a figure below.
(optional)</p></td>
</tr>
<tr class="even">
<td><p><code>dXj dYj dZj</code></p></td>
<td><p>joint offset values -- offsets specified with respect to the
global coordinate system for element-end node j (the number of arguments
depends on the dimensions of the current model). The offset vector is
oriented from node j to node i as shown in a figure below.
(optional)</p></td>
</tr>
</tbody>
</table>
<p>The element coordinate system is specified as follows:</p>
<p>The x-axis is the axis connecting the two element nodes; the y- and
z-axes are then defined using a vector that lies on a plane parallel to
the local x-z plane -- vecxz. The local y-axis is defined by taking the
cross product of the vecxz vector and the x-axis. The z-axis by taking
the cross-product of x and y vectors. The section is attached to the
element such that the y-z coordinate system used to specify the section
corresponds to the y-z axes of the element.</p>
<figure>
<img src="/OpenSeesRT/contrib/static/ElementOrentation.gif" title="ElementOrentation.gif"
alt="ElementOrentation.gif" />
<figcaption aria-hidden="true">ElementOrentation.gif</figcaption>
</figure>
<figure>
<img src="/OpenSeesRT/contrib/static/RigidElementOffsets.gif" title="RigidElementOffsets.gif"
alt="RigidElementOffsets.gif" />
<figcaption aria-hidden="true">RigidElementOffsets.gif</figcaption>
</figure>
<hr />

## Examples

<figure>
<img src="/OpenSeesRT/contrib/static/ElementCrossSection.png" title="ElementCrossSection.png"
alt="ElementCrossSection.png" />
<figcaption aria-hidden="true">ElementCrossSection.png</figcaption>
</figure>

<figure>
<img src="/OpenSeesRT/contrib/static/ElementOrientation.png" title="ElementOrientation.png"
alt="ElementOrientation.png" />
<figcaption aria-hidden="true">ElementOrientation.png</figcaption>
</figure>

<figure>
<img src="/OpenSeesRT/contrib/static/ElementVectors.png" title="ElementVectors.png"
alt="ElementVectors.png" />
<figcaption aria-hidden="true">ElementVectors.png</figcaption>
</figure>

```tcl
# Element 1 : tag 1 : vecxZ = zaxis
geomTransf PDelta 1 0 0 -1</p>

# Element 2 : tag 2 : vecxZ = y axis
geomTransf PDelta 2 0 1 0
```

<p>Code Developed by: <span style="color:blue"> Remo Magalhaes de
Souza </span></p>
<p>Images Developed by: <span style="color:blue"> Silvia Mazzoni
</span></p>
