# KikuchiBearing

<p>This command is used to construct a KikuchiBearing element object,
which is defined by two nodes. This element consists of multiple shear
spring model (MSS) and multiple normal spring model (MNS).</p>

```tcl
element KikuchiBearing $eleTag $iNode $jNode
        -shape $shape -size $size $totalRubber
        < -totalHeight $totalHeight >
        -nMSS $nMSS -matMSS $matMSSTag
        < -limDisp $limDisp >
        -nMNS $nMNS -matMNS $matMNSTag 
        < -lambda $lambda > 
        < -orient < $x1 $x2 $x3 > $yp1 $yp2 $yp3 > 
        < -mass $m > 
        < -noPDInput > 
        < -noTilt > 
        < -adjustPDOutput $ci $cj > 
        < -doBalance $limFo $limFi $nIter >
```

<hr />
<table>
<tbody>
<tr class="odd">
<td><code class="parameter-table-variable">eleTag</code></td>
<td><p>unique element object tag</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">inode jnode</code></p></td>
<td><p>end nodes</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">shape</code></td>
<td><p>following shapes are available: <strong>round</strong>,
<strong>square</strong></p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">size</code></td>
<td><p>diameter (round shape), length of edge (square shape)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">totalRubber</code></td>
<td><p>total rubber thickness</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">totalHeight</code></td>
<td><p>total height of the bearing (defaulut: distance between iNode and
jNode)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">nMSS</code></td>
<td><p>number of springs in MSS = nMSS</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">matMSSTag</code></td>
<td><p>matTag for MSS</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">limDisp</code></td>
<td><p>minimum deformation to calculate equivalent coefficient of MSS
(see note 1)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">nMNS</code></td>
<td><p>number of springs in MNS = nMNS*nMNS (for round and square
shape)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">matMNSTag</code></td>
<td><p>matTag for MNS</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">lambda</code></td>
<td><p>parameter to calculate compression modulus distribution on MNS
(see note 2)</p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-variable">x1 x2 x3</code></p></td>
<td><p>vector components in global coordinates defining local
x-axis</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">yp1 yp2 yp3</code></p></td>
<td><p>vector components in global coordinates defining vector yp which
lies in the local x-y plane for the element</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">m</code></td>
<td><p>element mass</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-flag">-noPDInput</code></p></td>
<td><p>not consider P-Delta moment</p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-flag">-noTilt</code></p></td>
<td><p>not consider tilt of rigid link</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">ci cj</code></p></td>
<td><p>P-Delta moment adjustment for reaction force (default:
<code class="tcl-variable">ci</code>=0.5, <code class="tcl-variable">cj</code>=0.5)</p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-variable">limFo limFi nIter</code></p></td>
<td><p>tolerance of external unbalanced force (<code class="tcl-variable">limFo</code>),
tolorance of internal unbalanced force (<code class="tcl-variable">limFi</code>), number
of iterations to get rid of internal unbalanced force
(<code class="tcl-variable">nIter</code>)</p></td>
</tr>
</tbody>
</table>
<p>NOTES:</p>
<p>1) If <code class="tcl-variable">limdisp</code> is positive and the shear deformation
of MSS exceeds <code class="tcl-variable">limdisp</code>, this element calculates
equivalent coefficient to adjust force and stiffness of MSS. The
adjusted MSS force and stiffness reproduce the behavior of the
previously defined uniaxial material under monotonic loading in every
direction.</p>
<p>2) Recommended value is (D/t)*sqrt(3*G/K), where D, t, G and K are
size (for round and square shape), thickness, shear modulus and bulk
modulus of a rubber layer, respectively.</p>
<p>3) The valid queries to a KikuchiBearing element when creating an
ElementRecorder object are 'globalForce', 'localForce', 'basicForce',
'localDisplacement' and 'basicDeformation'.</p>
<figure>
<img src="/OpenSeesRT/contrib/static/KikuchiBearing_Model.png" title="KikuchiBearing_Model.png"
width="400" alt="KikuchiBearing_Model.png" />
<figcaption aria-hidden="true">KikuchiBearing_Model.png</figcaption>
</figure>
<hr />

## Examples

<p>element KikuchiBearing 1 1 2 -shape round -size 1.016 0.320 -nMSS 8
-matMSS 1 -nMNS 30 -matMNS 2</p>
<p><a href="Media:KikuchiBearing_Sample.tcl"
title="wikilink">KikuchiBearing_Sample.tcl</a>, <a
href="Media:KikuchiBearing_input_Z.tcl"
title="wikilink">KikuchiBearing_input_Z.tcl</a>, <a
href="Media:KikuchiBearing_input_X.tcl"
title="wikilink">KikuchiBearing_input_X.tcl</a></p>
<table>
<tbody>
<tr class="odd">
<td><p>case 1: P-Delta effect not considered (use -noPDInput -noTilt
option)</p></td>
</tr>
<tr class="even">
<td><p>case 2: P-Delta effect considered, uniform distribution of
compression modulus</p></td>
</tr>
<tr class="odd">
<td><p>case 3: P-Delta effect considered (use -lambda option)</p></td>
</tr>
</tbody>
</table>
<p><img 
  src="/OpenSeesRT/contrib/static/KikuchiBearing_ForceDeformation_case1_v2.png"
  title="KikuchiBearing_ForceDeformation_case1_v2.png" width="250"
  alt="KikuchiBearing_ForceDeformation_case1_v2.png" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img
  src="/OpenSeesRT/contrib/static/KikuchiBearing_ForceDeformation_case2_v2.png"
  title="KikuchiBearing_ForceDeformation_case2_v2.png" 
  width="250"
  alt="KikuchiBearing_ForceDeformation_case2_v2.png" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img
  src="/OpenSeesRT/contrib/static/KikuchiBearing_ForceDeformation_case3_v2.png"
  title="KikuchiBearing_ForceDeformation_case3_v2.png" width="250"
  alt="KikuchiBearing_ForceDeformation_case3_v2.png" /></p>

## References
<p>M. Kikuchi , I. D. Aiken and A. Kasalanati , "Simulation analysis for
the ultimate behavior of full-scale lead-rubber seismic isolation
bearings", <em>15th World Conference on Earthquake Engineering</em>, No.
1688, 2012.</p>
<hr />
<p>Code Developed by: <span style="color:blue"> mkiku
</span></p>
