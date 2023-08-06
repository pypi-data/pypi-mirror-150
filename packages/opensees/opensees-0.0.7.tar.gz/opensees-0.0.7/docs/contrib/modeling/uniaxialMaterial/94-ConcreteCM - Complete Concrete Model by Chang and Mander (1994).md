---
description: Complete Concrete Model by Chang and Mander (1994)
...

# ConcreteCM

<p><strong>Developed and Implemented by:</strong></p>
<p><a href="mailto:kkolozvari@fullerton.edu"><span style="color:blue"> Kristijan Kolozvari</span>
<span style="color:black"></a>, California State University, Fullerton</p>
<p><span style="color:blue"> Kutay Orakcal&lt;span
style="color:black"&gt;, Bogazici University, Istanbul, Turkey</p>
<p><span style="color:blue"> John Wallace&lt;span
style="color:black"&gt;, Univeristy of California, Los Angeles</p>
<p>This command is used to construct a uniaxialMaterial
<strong>ConcreteCM</strong> (Kolozvari et al., 2015), which is a
uniaxial hysteretic constitutive model for concrete developed by Chang
and Mander (1994). This model is a refined, rule-based, generalized, and
non-dimensional constitutive model that allows calibration of the
monotonic and hysteretic material modeling parameters, and can simulate
the hysteretic behavior of confined and unconfined, ordinary and
high-strength concrete, in both cyclic compression and tension (Figure
1). The model addresses important behavioral features, such as
continuous hysteretic behavior under cyclic compression and tension,
progressive stiffness degradation associated with smooth unloading and
reloading curves at increasing strain values, and gradual crack closure
effects. Details of the model are available in the report by Chang and
Mander (1994).</p>
<figure>
<img src="/OpenSeesRT/contrib/static/ConcreteCM_0.png"
title="Figure 1. Hysteretic Constitutive Model for Concrete by Chang and Mander (1994)"
width="500"
alt="Figure 1. Hysteretic Constitutive Model for Concrete by Chang and Mander (1994)" />
<figcaption aria-hidden="true">Figure 1. Hysteretic Constitutive Model
for Concrete by Chang and Mander (1994)</figcaption>
</figure>
<p>The Chang and Mander (1994) model successfully generates continuous
hysteretic stress-strain relationships with slope continuity for
confined and unconfined concrete in both compression and tension. The
compression envelope curve of the model is defined by the initial
tangent slope, (E&lt;sub class="subscript"&gt;c&lt;/sub&gt;), the peak
coordinate (&lt;math&gt;\epsilon&lt;/math&gt;'&lt;sub
class="subscript"&gt;c&lt;/sub&gt;, f'&lt;sub
class="subscript"&gt;c&lt;/sub&gt;), a parameter (r&lt;sub
class="subscript"&gt;c&lt;/sub&gt;) from Tsai’s (1988) equation defining
the shape of the envelope curve, and a parameter
(&lt;math&gt;\epsilon&lt;/math&gt;&lt;sup
class="superscript"&gt;-&lt;/sup&gt;&lt;sub
class="subscript"&gt;cr&lt;/sub&gt;) to define normalized (with respect
to $\epsilon$'&lt;sub
class="subscript"&gt;c&lt;/sub&gt;) strain where the envelope curve
starts following a straight line, until zero compressive stress is
reached at the spalling strain, $\epsilon$&lt;sub
class="subscript"&gt;sp&lt;/sub&gt;. These parameters can be controlled
based on specific experimental results for a refined calibration of the
compression envelope (Figure 2). Chang and Mander (1994) proposed
empirical relationships for parameters E&lt;sub
class="subscript"&gt;c&lt;/sub&gt;,
&lt;math&gt;\epsilon&lt;/math&gt;'&lt;sub
class="subscript"&gt;c&lt;/sub&gt;, and r&lt;sub
class="subscript"&gt;c&lt;/sub&gt; for unconfined concrete with
compressive strength f'&lt;sub class="subscript"&gt;c&lt;/sub&gt;, based
on review of previous research. Parameters f'&lt;sub
class="subscript"&gt;c&lt;/sub&gt;,
&lt;math&gt;\epsilon&lt;/math&gt;'&lt;sub
class="subscript"&gt;c&lt;/sub&gt;, E&lt;sub
class="subscript"&gt;c&lt;/sub&gt;, r&lt;sub
class="subscript"&gt;c&lt;/sub&gt;, and
&lt;math&gt;\epsilon&lt;/math&gt;&lt;sup
class="superscript"&gt;-&lt;/sup&gt;&lt;sub
class="subscript"&gt;cr&lt;/sub&gt; can also be calibrated to represent
the stress-strain behavior of confined concrete in compression, to
follow the constitutive relationships for confined concrete proposed by
Mander et al (1988) or similar.</p>
<figure>
<img src="/OpenSeesRT/contrib/static/ConcreteCM_1.png"
title="Figure 2. Compression and Tension Envelope Curves" width="500"
alt="Figure 2. Compression and Tension Envelope Curves" />
<figcaption aria-hidden="true">Figure 2. Compression and Tension
Envelope Curves</figcaption>
</figure>
<p>The shape of the tension envelope curve in the model is the same as
that of the compression envelope; however, the tension envelope curve is
shifted to a new origin that is based on the unloading strain from the
compression envelope (Figure 2). As well, the strain ductility
experienced previously on the compression envelope is also reflected on
the tension envelope. The parameters associated with the tension
envelope curve include the tensile strength of concrete (f&lt;sub
class="subscript"&gt;t&lt;/sub&gt;), the monotonic strain at tensile
strength ( $\epsilon_\textrm{t}$ ), a parameter (r&lt;sub
class="subscript"&gt;t&lt;/sub&gt;) from Tsai’s (1988) equation defining
the shape of the tension envelope curve, and a parameter
(&lt;math&gt;\epsilon&lt;/math&gt;&lt;sup
class="superscript"&gt;+&lt;/sup&gt;&lt;sub
class="subscript"&gt;cr&lt;/sub&gt;) to define normalized (with respect
to $\epsilon$&lt;sub
class="subscript"&gt;t&lt;/sub&gt;) strain where the tension envelope
curve starts following a straight line, until zero tensile stress is
reached at a strain of $\epsilon$&lt;sub
class="subscript"&gt;crk&lt;/sub&gt;. These parameters can also be
controlled and calibrated based on specific experimental results or
empirical relations proposed by other researchers (e.g., Belarbi and
Hsu, 1994) to model the behavior of concrete in tension and the tension
stiffening phenomenon. Concrete experiencing tension stiffening can be
considered not to crack completely; that is, a large value for parameter
&lt;math&gt;\epsilon&lt;/math&gt;&lt;sup
class="superscript"&gt;+&lt;/sup&gt;&lt;sub
class="subscript"&gt;cr&lt;/sub&gt; (e.g., 10000) can be defined.</p>
<p>Source: /usr/local/cvs/OpenSees/SRC/material/uniaxial/</p>
<hr />
<p><strong>Input Format:</strong></p>

```tcl
uniaxialMaterial ConcreteCM $mattag $fpcc $epcc $Ec $rc
        $xcrn $ft $et $rt $xcrp &lt;-GapClose $gap&gt;
```


<table>
<tbody>
<tr class="odd">
<td><code class="parameter-table-variable">mattag</code></td>
<td><p>Unique <em>uniaxialMaterial</em> tag</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">fpcc</code></td>
<td><p>Compressive strength (f'&lt;sub
class="subscript"&gt;c&lt;/sub&gt;)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">epcc</code></td>
<td><p>Strain at compressive strength
(&lt;math&gt;\epsilon&lt;/math&gt;'&lt;sub
class="subscript"&gt;c&lt;/sub&gt;)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">Ec</code></td>
<td><p>Initial tangent modulus (E&lt;sub
class="subscript"&gt;c&lt;/sub&gt;)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">rc</code></td>
<td><p>Shape parameter in Tsai’s equation defined for compression
(r&lt;sub class="subscript"&gt;c&lt;/sub&gt;)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">xcrn</code></td>
<td><p>Non-dimensional critical strain on compression envelope
(&lt;math&gt;\epsilon&lt;/math&gt;&lt;sup
class="superscript"&gt;-&lt;/sup&gt;&lt;sub
class="subscript"&gt;cr&lt;/sub&gt;, where the envelope curve starts
following a straight line)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">ft</code></td>
<td><p>Tensile strength (f&lt;sub
class="subscript"&gt;t&lt;/sub&gt;)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">et</code></td>
<td><p>Strain at tensile strength
( $\epsilon_\textrm{t}$ )</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">rt</code></td>
<td><p>Shape parameter in Tsai’s equation defined for tension (r&lt;sub
class="subscript"&gt;t&lt;/sub&gt;)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">xcrp</code></td>
<td><p>Non-dimensional critical strain on tension envelope
(&lt;math&gt;\epsilon&lt;/math&gt;&lt;sup
class="superscript"&gt;+&lt;/sup&gt;&lt;sub
class="subscript"&gt;cr&lt;/sub&gt;, where the envelope curve starts
following a straight line - large value [e.g., 10000] recommended when
tension stiffening is considered)</p></td>
</tr>
<tr class="odd">
<td><p><strong>&lt;-GapClose $gap&gt;</strong></p></td>
<td><p><strong>gap</strong> = 0, less gradual gap closure (default);
<strong>gap</strong> = 1, more gradual gap closure</p></td>
</tr>
</tbody>
</table>
<hr />
<p><strong>Example:</strong></p>
<p>uniaxialMaterial ConcreteCM 1 -6.2 -0.0021 4500 7 1.035 0.30 0.00008
1.2 10000</p>
<p>Example of hysteretic stress-strain history generated by the model
code is illustrated in Figure 3.</p>
<figure>
<img src="/OpenSeesRT/contrib/static/ConcreteCM_2.png"
title="Figure 3. Concrete Stress-Strain Behavior" width="500"
alt="Figure 3. Concrete Stress-Strain Behavior" />
<figcaption aria-hidden="true">Figure 3. Concrete Stress-Strain
Behavior</figcaption>
</figure>
<hr />
<p><strong>Discussion:</strong></p>
<p>An optional input parameter <strong>gap</strong> is introduced in the
<strong>ConcreteCM</strong> model implemented in OpenSees for providing
the users with the opportunity to control the intensity of gap closure
in the stress-strain behavior of concrete, which in-turn influences the
level of pinching in the lateral load-displacement behavior of a RC
wall. The original Chang and Mander (1994) model adopts a non-zero
tangent stiffness at zero stress level upon unloading from the tension
envelope, which is represented by gap = 1 in
<strong>ConcreteCM</strong>. Using <strong>gap</strong> = 0 (default)
produces less gradual gap closure, since it assumes zero tangent
stiffness at zero stress level upon unloading from the tension envelope,
and is suitable for most analyses. Figure 4 illustrates the effect of
plastic stiffness upon unloading from tension envelope (E&lt;sup
class="superscript"&gt;+&lt;/sup&gt;&lt;sub
class="subscript"&gt;pl&lt;/sub&gt;) on crack closure, i.e. use of more
gradual (<strong>gap</strong> = 1) or less gradual (<strong>gap</strong>
= 0) gap closure. The effect of parameter <strong>gap</strong> on
predictions of flexural behavior of a RC wall is illustrated in Example
1 of <a
href="http://opensees.berkeley.edu/wiki/index.php/MVLEM_-_Multiple-Vertical-Line-Element-Model_for_RC_Walls"><strong>MVLEM</strong></a>
element.</p>
<figure>
<img src="/OpenSeesRT/contrib/static/ConcreteCM_3.png"
title="Figure 4. Effect of Plastic Stiffness upon Unloading from Tension Envelope (Epl+) on Crack Closure"
width="500"
alt="Figure 4. Effect of Plastic Stiffness upon Unloading from Tension Envelope (Epl+) on Crack Closure" />
<figcaption aria-hidden="true">Figure 4. Effect of Plastic Stiffness
upon Unloading from Tension Envelope (Epl+) on Crack
Closure</figcaption>
</figure>
<p>Constitutive stress-strain concrete behavior is also implemented in
OpenSees in uniaxialMaterial <a
href="http://opensees.berkeley.edu/wiki/index.php/Concrete07_%E2%80%93_Chang_%26_Mander%E2%80%99s_1994_Concrete_Model"><strong>Cocnrete07</strong></a>.
However, <strong>ConcreteCM</strong> incorporates sophisticated
unloading/reloading rules defined originally by Chang and Mander (1994),
as opposed to <strong>Concrete07</strong> that adopts simplified
hysteretic rules. Comparison between stress-strain response predicted
using <strong>ConcreteCM</strong> and <strong>Concrete07</strong> is
shown in Figure 5.</p>
<figure>
<img src="/OpenSeesRT/contrib/static/ConcreteCMvsConcrete07.png"
title="Figure 5. Comparison of ConcreteCM and Concrete07" width="500"
alt="Figure 5. Comparison of ConcreteCM and Concrete07" />
<figcaption aria-hidden="true">Figure 5. Comparison of ConcreteCM and
Concrete07</figcaption>
</figure>
<hr />

<p><strong>References:</strong></p>
<p>1) Belarbi H. and Hsu T.C.C. (1994), “Constitutive Laws of Concrete
in Tension and Reinforcing Bars Stiffened by Concrete”, ACI Structural
Journal, V. 91, No. 4, pp. 465-474.</p>
<p>2) Chang, G.A. and Mander, J.B. (1994), “Seismic Energy Based Fatigue
Damage Analysis of Bridge Columns: Part I - Evaluation of Seismic
Capacity”, NCEER Technical Report No. NCEER-94-0006, State University of
New York, Buffalo.</p>
<p>3) Kolozvari K., Orakcal K., and Wallace J. W. (2015). "Shear-Flexure
Interaction Modeling of reinforced Concrete Structural Walls and Columns
under Reversed Cyclic Loading", Pacific Earthquake Engineering Research
Center, University of California, Berkeley, <a
href="http://peer.berkeley.edu/publications/peer_reports/reports_2015/webPEER-2015-12-kolozvari.pdf">PEER
Report No. 2015/12</a></p>
<p>4) Mander J.B., Priestley M.J.N., and Park R. (1988). “Theoretical
Stress-Strain Model for Confined Concrete”, ASCE Journal of Structural
Engineering, V. 114, No. 8, pp. 1804-1826.</p>
<p>5) Orakcal K.(2004), "Nonlinear Modeling and Analysis of Slender
Reinforced Concrete Walls", PhD Dissertation, Department of Civil and
Environmental Engineering, University of California, Los Angeles.</p>
<p>6) Tsai W.T. (1988), “Uniaxial Compressional Stress-Strain Relation
of Concrete”, ASCE Journal of Structural Engineering, V. 114, No. 9, pp.
2133-2136.</p>
