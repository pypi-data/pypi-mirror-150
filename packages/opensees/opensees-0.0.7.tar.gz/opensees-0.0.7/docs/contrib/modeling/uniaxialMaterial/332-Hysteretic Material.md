# Hysteretic

<p>This command is used to construct a uniaxial bilinear hysteretic
material object with pinching of force and deformation, damage due to
ductility and energy, and degraded unloading stiffness based on
ductility.</p>

```tcl
uniaxialMaterial Hysteretic $matTag $s1p $e1p $s2p $e2p
        &lt;$s3p $e3p&gt; $s1n $e1n $s2n $e2n &lt;$s3n $e3n&gt; $pinchX $pinchY
        $damage1 $damage2 &lt;$beta&gt;
```

<hr />
<table>
<tbody>
<tr class="odd">
<td><code class="parameter-table-variable">matTag</code></td>
<td><p>integer tag identifying material</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">s1p e1p</code></p></td>
<td><p>stress and strain (or force &amp; deformation) at first point of
the envelope in the positive direction</p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-variable">s2p e2p</code></p></td>
<td><p>stress and strain (or force &amp; deformation) at second point of
the envelope in the positive direction</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">s3p e3p</code></p></td>
<td><p>stress and strain (or force &amp; deformation) at third point of
the envelope in the positive direction (optional)</p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-variable">s1n e1n</code></p></td>
<td><p>stress and strain (or force &amp; deformation) at first point of
the envelope in the negative direction</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">s2n e2n</code></p></td>
<td><p>stress and strain (or force &amp; deformation) at second point of
the envelope in the negative direction</p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-variable">s3n e3n</code></p></td>
<td><p>stress and strain (or force &amp; deformation) at third point of
the envelope in the negative direction (optional)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">pinchx</code></td>
<td><p>pinching factor for strain (or deformation) during
reloading</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">pinchy</code></td>
<td><p>pinching factor for stress (or force) during reloading</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">damage1</code></p></td>
<td><p>damage due to ductility: D1(mu-1)</p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-variable">damage2</code></p></td>
<td><p>damage due to energy: D2(Eii/Eult)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">beta</code></td>
<td><p>power used to determine the degraded unloading stiffness based on
ductility, mu-beta (optional, default=0.0)</p></td>
</tr>
</tbody>
</table>
<figure>
<img src="/OpenSeesRT/contrib/static/Hysteretic.gif" title="Hysteretic.gif" alt="Hysteretic.gif" />
<figcaption aria-hidden="true">Hysteretic.gif</figcaption>
</figure>
<figure>
<img src="/OpenSeesRT/contrib/static/Hysteretic2.png" title="Hysteretic2.png"
alt="Hysteretic2.png" />
<figcaption aria-hidden="true">Hysteretic2.png</figcaption>
</figure>
<p>NOTE:</p>
<ol>
<li>In cases $s3p &gt; $s2p and abs($s3n) &gt; abs($s2n), the envelope
of the hysteretic material after $e3p or $e3n follows the slope defined
by 2nd and 3rd point of the envelope.</li>
<li>In cases $s3p &lt;= $s2p and abs($s3n) &lt;= abs($s2n) the envelope
of the hysteretic material after $e3p or $e3n is a flat line with a
constant stress (or force) equal to $s3p or $s3n.</li>
</ol>
<hr />

## Examples

<p>Effects of Hysteretic-Material Parameters <a
href="http://opensees.berkeley.edu/OpenSees/manuals/usermanual/4052.htm">1</a></p>
<hr />
<p>Code Developed by: <span style="color:blue"> Michael Scott
(Oregon State University) &amp; Filip Filippou (UC Berkeley)
</span></p>
<p>Images Developed by: <span style="color:blue"> Silvia Mazzoni
</span></p>
