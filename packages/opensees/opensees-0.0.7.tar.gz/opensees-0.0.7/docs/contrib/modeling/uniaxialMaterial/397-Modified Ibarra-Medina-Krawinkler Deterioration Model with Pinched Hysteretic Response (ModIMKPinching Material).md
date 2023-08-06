---
description: Modified Ibarra-Medina-Krawinkler Deterioration Model with Pinched Hysteretic Response (ModIMKPinching Material)
...

# ModIMKPinching

<p>This command is used to construct a ModIMKPinching material. This
material simulates the modified Ibarra-Medina-Krawinkler deterioration
model with pinching hysteretic response. <a
href="NOTE:_before_you_use_this_material_make_sure_that_you_have_downloaded_the_latest_OpenSees_version."
title="wikilink">NOTE: before you use this material make sure that you
have downloaded the latest OpenSees version.</a> A youtube video
presents a summary of this model including the way to be used within
openSees (http://youtu.be/YHBHQ-xuybE).</p>

```tcl
uniaxialMaterial ModIMKPinching $matTag $K0 $as_Plus
        $as_Neg $My_Plus $My_Neg $FprPos $FprNeg $A_pinch $Lamda_S $Lamda_C
        $Lamda_A $Lamda_K $c_S $c_C $c_A $c_K $theta_p_Plus $theta_p_Neg
        $theta_pc_Plus $theta_pc_Neg $Res_Pos $Res_Neg $theta_u_Plus
        $theta_u_Neg $D_Plus $D_Neg
```

<hr />
<table>
<tbody>
<tr class="odd">
<td><code class="parameter-table-variable">matTag</code></td>
<td><p>integer tag identifying material</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">K0</code></td>
<td><p>elastic stiffness</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">as_Plus</code></td>
<td><p>strain hardening ratio for positive loading direction</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">as_Neg</code></td>
<td><p>strain hardening ratio for negative loading direction</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">My_Plus</code></td>
<td><p>effective yield strength for positive loading direction</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">My_Neg</code></td>
<td><p>effective yield strength for negative loading direction (Must be
defined as a negative value)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">FprPos</code></td>
<td><p>Ratio of the force at which reloading begins to force
corresponding to the maximum historic deformation demand (positive
loading direction)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">FprNeg</code></td>
<td><p>Ratio of the force at which reloading begins to force
corresponding to the absolute maximum historic deformation demand
(negative loading direction)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">A_Pinch</code></td>
<td><p>Ratio of reloading stiffness</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">Lamda_S</code></td>
<td><p>Cyclic deterioration parameter for strength deterioration
[E_t=Lamda_S*M_y, see Lignos and Krawinkler (2011); set Lamda_S = 0 to
disable this mode of deterioration]</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">Lamda_C</code></td>
<td><p>Cyclic deterioration parameter for post-capping strength
deterioration [E_t=Lamda_C*M_y, see Lignos and Krawinkler (2011); set
Lamda_C = 0 to disable this mode of deterioration]</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">Lamda_A</code></td>
<td><p>Cyclic deterioration parameter for accelerated reloading
stiffness deterioration [E_t=Lamda_A*M_y, see Lignos and Krawinkler
(2011); set Lamda_A = 0 to disable this mode of deterioration]</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">Lamda_K</code></td>
<td><p>Cyclic deterioration parameter for unloading stiffness
deterioration [E_t=Lamda_K*M_y, see Lignos and Krawinkler (2011); set
Lamda_K = 0 to disable this mode of deterioration]</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">c_S</code></td>
<td><p>rate of strength deterioration. The default value is
1.0.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">c_C</code></td>
<td><p>rate of post-capping strength deterioration. The default value is
1.0.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">c_A</code></td>
<td><p>rate of accelerated reloading deterioration. The default value is
1.0.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">c_K</code></td>
<td><p>rate of unloading stiffness deterioration. The default value is
1.0.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">theta_p_Plus</code></td>
<td><p>pre-capping rotation for positive loading direction (often noted
as plastic rotation capacity)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">theta_p_Neg</code></td>
<td><p>pre-capping rotation for negative loading direction (often noted
as plastic rotation capacity) (must be defined as a positive
value)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">theta_pc_Plus</code></td>
<td><p>post-capping rotation for positive loading direction</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">theta_pc_Neg</code></td>
<td><p>post-capping rotation for negative loading direction (must be
defined as a positive value)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">Res_Pos</code></td>
<td><p>residual strength ratio for positive loading direction</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">Res_Neg</code></td>
<td><p>residual strength ratio for negative loading direction (must be
defined as a positive value)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">theta_u_Plus</code></td>
<td><p>ultimate rotation capacity for positive loading
direction</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">theta_u_Neg</code></td>
<td><p>ultimate rotation capacity for negative loading direction (must
be defined as a positive value)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">D_Plus</code></td>
<td><p>rate of cyclic deterioration in the positive loading direction
(this parameter is used to create assymetric hysteretic behavior for the
case of a composite beam). For symmetric hysteretic response use
1.0.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">D_Neg</code></td>
<td><p>rate of cyclic deterioration in the negative loading direction
(this parameter is used to create assymetric hysteretic behavior for the
case of a composite beam). For symmetric hysteretic response use
1.0.</p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
</tbody>
</table>
<figure>
<img src="/OpenSeesRT/contrib/static/ModIMKDefinitionFigure.png" title="ModIMKDefinitionFigure.png"
width="700" alt="ModIMKDefinitionFigure.png" />
<figcaption aria-hidden="true">ModIMKDefinitionFigure.png</figcaption>
</figure>
<p><strong>Image from: Lignos and Krawinkler (2012)</strong></p>
<p>The deterioration model parameters can be calibrated based on actual
experimental data of RC beams in terms of load - displacement or moment
- rotation. Examples of such calibrations can be found in Lignos (2008)
and Lignos and Krawinkler (2012).</p>
<hr />
<p><strong>References</strong>:</p>
<table>
<tbody>
<tr class="odd">
<td><p><strong>[1]</strong></p></td>
<td><p>Lignos, D.G., Krawinkler, H. (2012). “Development and Utilization
of Structural Component Databases for Performance-Based Earthquake
Engineering", Journal of Structural Engineering, ASCE, doi:
10.1061/(ASCE)ST.1943-541X.0000646.</p></td>
</tr>
<tr class="even">
<td><p><strong>[2]</strong></p></td>
<td><p>Lignos, D.G., and Krawinkler, H. (2011). “Deterioration modeling
of steel components in support of collapse prediction of steel moment
frames under earthquake loading”, Journal of Structural Engineering,
ASCE, Vol. 137 (11), 1291-1302.</p></td>
</tr>
<tr class="odd">
<td><p><strong>[3]</strong></p></td>
<td><p>Lignos, D.G. and Krawinkler, H. (2012). “Sidesway collapse of
deteriorating structural systems under seismic excitations,” Rep.No.TB
177, The John A. Blume Earthquake Engineering Research Center, Stanford
University, Stanford, CA. [electronic version: <a
href="https://blume.stanford.edu/tech_reports">https://blume.stanford.edu/tech_reports</a>]</p></td>
</tr>
<tr class="even">
<td><p><strong>[4]</strong></p></td>
<td><p>Lignos, D.G. (2008). “Sidesway collapse of deteriorating
structural systems under seismic excitations,” Ph.D. Dissertation,
Department of Civil and Environmental Engineering, Stanford University,
Stanford, CA.</p></td>
</tr>
<tr class="odd">
<td><p><strong>[5]</strong></p></td>
<td><p>Ibarra L.F., and Krawinkler, H. (2005). “Global collapse of frame
structures under seismic excitations”, Rep. No. TB 152, The John A.
Blume Earthquake Engineering Center, Stanford University, Stanford, CA.
[electronic version: <a
href="https://blume.stanford.edu/tech_reports">https://blume.stanford.edu/tech_reports</a>]</p></td>
</tr>
<tr class="even">
<td><p><strong>[6]</strong></p></td>
<td><p>Ibarra L.F., Medina R. A., and Krawinkler H. (2005). “Hysteretic
models that incorporate strength and stiffness deterioration”,
Earthquake Engineering and Structural Dynamics, 34(12),
1489-1511.</p></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
</tr>
</tbody>
</table>
<p>Code Developed by : <span style="color:blue"> by Dr. Dimitrios
G. Lignos, McGill University </span></p>
