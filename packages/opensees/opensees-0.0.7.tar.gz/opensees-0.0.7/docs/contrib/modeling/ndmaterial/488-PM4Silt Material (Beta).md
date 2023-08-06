# PM4Silt Material (Beta)

<ul>
<li><strong>This page has been moved to the new <a
href="https://opensees.github.io/OpenSeesDocumentation/user/manual/material/ndMaterials/PM4Silt.html">OpenSees
documentation site</a></strong></li>
</ul>
<p>This command is used to construct a 2-dimensional PM4Silt
material.</p>

```tcl
nDMaterial PM4Silt $matTag $S_u $Su_Rat $G_o $h_po $Den
        &lt;$Su_factor $Patm $nu $nG $h0 $eInit $lambda $phicv $nb_wet $nb_dry
        $nd $Ado $ru_max $zmax $cz $ce $Cgd $ckaf $m_m
        $CG_consol&gt;
```

<table>
<tbody>
<tr class="odd">
<td><code class="parameter-table-variable">matTag</code></td>
<td><p>integer tag identifying material</p></td>
</tr>
<tr class="even">
<td><p><strong>Primary</strong>:</p></td>
<td></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">S_u</code></td>
<td><p>Undrained shear strength</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">Su_Rat</code></td>
<td><p>Undrained shear strength ratio. If both S_u and Su_Rat values are
specified, the value of S_u is used.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">G_o</code></td>
<td><p>Shear modulus constant</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">h_po</code></td>
<td><p>Contraction rate parameter</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">Den</code></td>
<td><p>Mass density of the material</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">Su_factor</code></td>
<td><p><em>Optional</em>, Undrained shear strength reduction
factor</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">P_atm</code></td>
<td><p><em>Optional</em>, Atmospheric pressure</p></td>
</tr>
<tr class="even">
<td><p><strong>Secondary</strong>:</p></td>
<td></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">nu</code></td>
<td><p><em>Optional</em>, Poisson's ratio. Default value is
0.3.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">nG</code></td>
<td><p><em>Optional</em>, Shear modulus exponent. Default value is
0.75.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">h0</code></td>
<td><p><em>Optional</em>, Variable that adjusts the ratio of plastic
modulus to elastic modulus. Default value is 0.5.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">eInit</code></td>
<td><p><em>Optional</em>, Initial void ratios. Default value is
0.90.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">lambda</code></td>
<td><p><em>Optional</em>, The slope of critical state line in e-ln(p)
space. Default value is 0.060.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">phicv</code></td>
<td><p><em>Optional</em>, Critical state effective friction angle.
Default value is 32 degrees.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">nb_wet</code></td>
<td><p><em>Optional</em>, Bounding surface parameter for loose of
critical state conditions, 1.0 &amp;ge; $nb_wet &amp;ge; 0.01. Default
value is 0.8.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">nb_dry</code></td>
<td><p><em>Optional</em>, Bounding surface parameter for dense of
critical state conditions, $nb_dry &amp;ge; 0. Default value is
0.5.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">nd</code></td>
<td><p><em>Optional</em>, Dilatancy surface parameter $nd &amp;ge; 0.
Default value is 0.3.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">Ado</code></td>
<td><p><em>Optional</em>, Dilatancy parameter. Default value is
0.8.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">ru_max</code></td>
<td><p><em>Optional</em>, Maximum pore pressure ratio based on
p'.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">z_max</code></td>
<td><p><em>Optional</em>, Fabric-dilatancy tensor parameter</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">cz</code></td>
<td><p><em>Optional</em>, Fabric-dilatancy tensor parameter. Default
value is 100.0.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">ce</code></td>
<td><p><em>Optional</em>, Variable that adjusts the rate of strain
accumulation in cyclic loading</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">cgd</code></td>
<td><p><em>Optional</em>, Variable that adjusts degradation of elastic
modulus with accumulation of fabric. Default value is 3.0.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">ckaf</code></td>
<td><p><em>Optional</em>, Variable that controls the effect that
sustained static shear stresses have on plastic modulus. Default value
is 4.0.</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">m_m</code></td>
<td><p><em>Optional</em>, Yield surface constant (radius of yield
surface in stress ratio space). Default value is 0.01.</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">CG_consol</code></td>
<td><p><em>Optional</em>, Reduction factor of elastic modulus for
reconsolidation. $CG_consol &amp;ge; 1. Default value is 2.0.</p></td>
</tr>
</tbody>
</table>
<p>The material formulation for the PM4Silt object is "PlaneStrain"</p>
<hr />
<p>Code Developed by: <span style="color:blue">Long Chen, <a
href="https://www.ce.washington.edu/people/faculty/arduinop">Pedro
Arduino, U Washington</a></span></p>
<hr />
<h2 id="notes">Notes</h2>
<ul>
<li>Valid Element Recorder queries are
<ul>
<li><strong>stress</strong>, <strong>strain</strong></li>
<li><strong>alpha</strong> (or <strong>backstressratio</strong>) for
&lt;math&gt;\mathbf{\alpha}&lt;/math&gt;</li>
<li><strong>fabric</strong> for $\mathbf{z}$</li>
<li><strong>alpha_in</strong> (or <strong>alphain</strong>) for
&lt;math&gt;\mathbf{\alpha_{in}}&lt;/math&gt;</li>
</ul></li>
</ul>
<p>e.g. recorder Element -eleRange 1 $numElem -time -file stress.out
stress</p>
<ul>
<li>Elastic or Elastoplastic response could be enforced by</li>
</ul>
<dl>
<dt></dt>
<dd>
<dl>
<dt></dt>
<dd>
{|
</dd>
</dl>
</dd>
</dl>
<p>|Elastic: ||updateMaterialStage -material $matTag -stage 0 |-
|Elastoplastic: ||updateMaterialStage -material $matTag -stage 1 |}</p>
<ul>
<li>If default values are used for secondary parameters, the model must
be initialized after elastic gravity stage by</li>
</ul>
<p>setParameter -value 0 -ele $elementTag FirstCall $matTag</p>
<ul>
<li>Post-shake reconsolidation can be activated by</li>
</ul>
<p>setParameter -value 1 -ele $elementTag Postshake $matTag</p>
<h2 id="example">Example</h2>
<p>&lt;table border=1 width=600&gt; &lt;tr&gt; &lt;td width=90&gt;<a
href="PM4Silt-Example_1" title="wikilink">Example 1</a> &lt;/td&gt;</p>
<p>&lt;td&gt;2D undrained monotonic direct simple shear test using one
element&lt;/td&gt; &lt;/tr&gt; &lt;tr&gt; &lt;td&gt;<a
href="PM4Silt-Example_2" title="wikilink">Example 2</a>&lt;/td&gt;
&lt;td&gt;2D undrained cyclic direct simple shear test using one
element&lt;/td&gt; &lt;/tr&gt;</p>
<p>&lt;/table&gt;</p>
<h2 id="references">References</h2>
<p>R.W.Boulanger, K.Ziotopoulou. "PM4Silt(Version 1): A Silt Plasticity
Model for Earthquake Engineering Applications". Report No. UCD/CGM-18/01
2018</p>
