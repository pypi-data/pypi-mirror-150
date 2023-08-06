# Steel4

<p>This command is used to construct a general uniaxial material
with combined kinematic and isotropic hardening and optional
non-symmetric behavior.</p>

```tcl
uniaxialMaterial Steel4 $matTag $f_y $E_0 < -asym >
  < -kin $b_k $R_0 $r_1 $r_2 < $b_kc $R_0c $r_1c $r_2c > >
  < -iso $b_i $rho_i $b_l $R_i $l_yp < $b_ic $rho_ic $b_lc $R_ic > >
  < -ult $f_u $R_u < $f_uc $R_uc > > 
  < -init $sig_init > 
  < -mem $cycNum >
```


<h2 id="parameters">Parameters</h2>
<table>
<tbody>
<tr class="odd">
<td><code class="parameter-table-variable">matTag</code></td>
<td><p>unique material object integer tag</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">f_y</code></td>
<td><p>yield strength (assumed identical in tension and
compression)</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">E_0</code></td>
<td><p>initial stiffness (Young's modulus)</p></td>
</tr>
<tr class="even">
<td><p><em>optional features:</em></p></td>
<td></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-flag">-kin</code></p></td>
<td><p>apply kinematic hardening</p></td>
</tr>
</tbody>
</table>
<p>&lt;blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p>colspan = "2" style="text-align: justify" | Kinematic hardening
is based on the Menegotto-Pinto model. The parameters and their use is
identical to those of the Steel02 material.</p></td>
<td><p>rowspan = "7" | <img src="/OpenSeesRT/contrib/static/Steel4_param_kin.png"
title="Steel4_param_kin.png" width="400"
alt="Steel4_param_kin.png" /></p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">b_k</code></td>
<td><p>hardening ratio (E_k/E_0)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">R_0</code></td>
<td><p>control the exponential transition from linear elastic to
hardening asymptote recommended values: <em>$R_0 = 20 $r_1 = 0.90 $r_2 =
0.15</em></p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-variable">r_1</code></p></td>
<td></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">r_2</code></p></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
</tr>
</tbody>
</table>
<p>&lt;/blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-flag">-iso</code></p></td>
<td><p>apply isotropic hardening</p></td>
</tr>
</tbody>
</table>
<p>&lt;blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p>colspan = "2" style="text-align: justify" | Isotropic hardening
increases the yield strength of the material. The applied increase is
calculated as a function of the accumulated plastic strain. The
following parameters control that function.</p></td>
<td><p>rowspan = "9" | <img src="/OpenSeesRT/contrib/static/Steel4_param_iso.png"
title="Steel4_param_iso.png" width="400"
alt="Steel4_param_iso.png" /></p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">b_i</code></td>
<td><p>initial hardening ratio (E_i/E_0)</p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">b_l</code></td>
<td><p>saturated hardening ratio (E_is/E_0)</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">rho_i</code></td>
<td><p>specifies the position of the intersection point between initial
and saturated hardening asymptotes</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">R_i</code></td>
<td><p>control the exponential transition from initial to saturated
asymptote</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">l_yp</code></td>
<td><p>length of the yield plateau in eps_y0 = f_y / E_0 units</p></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
</tr>
</tbody>
</table>
<p>&lt;/blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-flag">-ult</code></p></td>
<td><p>apply an ultimate strength limit</p></td>
</tr>
</tbody>
</table>
<p>&lt;blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p>colspan = "2" style="text-align: justify" | The ultimate strength
limit serves as an upper limit of material resistance. After the limit
is reached the material behaves in a perfectly plastic manner.
Exponential transition is provided from the kinematic hardening to the
perfectly plastic asymptote.</p></td>
<td><p>rowspan = "6" | <img src="/OpenSeesRT/contrib/static/Steel4_param_ult.png"
title="Steel4_param_ult.png" width="400"
alt="Steel4_param_ult.png" /></p></td>
</tr>
<tr class="even">
<td><p>colspan = "2" style="text-align: justify" | Note that isotropic
hardening is also limited by the ultimate strength, but the transition
from the isotropic hardening to the perfectly plastic asymptote is
instantaneous.</p></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">f_u</code></td>
<td><p>ultimate strength</p></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">R_u</code></td>
<td><p>control the exponential transition from kinematic hardening to
perfectly plastic asymptote</p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
</tbody>
</table>
<p>&lt;/blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-flag">-asym</code></p></td>
<td><p>assume non-symmetric behavior</p></td>
</tr>
</tbody>
</table>
<p>&lt;blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p>colspan = "2" style="text-align: justify" | If non-symmetric
behavior is assumed, material response under tension and compression
will be controlled by two different parameter sets. The normal
parameters control behavior under tension. Additional parameters shall
be specified to describe behavior under compression. The following
parameters are expected after the normal parameters when the options
below are used.</p></td>
<td><p>rowspan = "6" | <img src="/OpenSeesRT/contrib/static/Steel4_param_asymk.png"
title="Steel4_param_asymk.png" width="400"
alt="Steel4_param_asymk.png" /></p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-flag">-kin</code></p></td>
<td><p><em>$b_kc $R_0c $r_1c $r_2c</em></p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-flag">-iso</code></p></td>
<td><p><em>$b_ic $rho_ic $b_lc $R_ic</em></p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-flag">-ult</code></p></td>
<td><p><em>$f_uc $R_uc</em></p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
</tbody>
</table>
<p>&lt;/blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-flag">-init</code></p></td>
<td><p>apply initial stress</p></td>
</tr>
</tbody>
</table>
<p>&lt;blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p>colspan = "2" style="text-align: justify" | Initial stress is
assumed at 0 strain at the beginning of the loading process. The
absolute value of the initial stress is assumed to be less than the
yield strength of the material.</p></td>
<td><p>rowspan = "4" | <img src="/OpenSeesRT/contrib/static/Steel4_param_init.png"
title="Steel4_param_init.png" width="400"
alt="Steel4_param_init.png" /></p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">sig_init</code></td>
<td><p>initial stress value</p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
</tbody>
</table>
<p>&lt;/blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-flag">-mem</code></p></td>
<td><p>configure the load history memory</p></td>
</tr>
</tbody>
</table>
<p>&lt;blockquote&gt;</p>
<table>
<tbody>
<tr class="odd">
<td><p>colspan = "2" style="text-align: justify" | The load history
memory is a database of preceding load cycles. It is updated at every
load reversal point during the loading process. It is turned on by
default. Turning it off will reduce the memory consumption of
Steel4.</p></td>
<td><p>rowspan = "8" | <img src="/OpenSeesRT/contrib/static/Steel4_param_mem.png"
title="Steel4_param_mem.png" width="400"
alt="Steel4_param_mem.png" /></p></td>
</tr>
<tr class="even">
<td><p>colspan = "2" style="text-align: justify" | The available data on
preceding cycles is currently used to correct a typical error in the
Steel02 material. The error stems from the formulation of the
Menegotto-Pinto kinematic hardening model. It leads to overestimation of
the stress response after small unloading-reloading cycles. This
phenomenon is important, because the seismic response of structures
typically includes a large number of such small cycles. The error is
avoided by forcing the kinematic hardening component of the response to
converge to previous load cycles.</p></td>
<td></td>
</tr>
<tr class="odd">
<td><p>colspan = "2" style="text-align: justify" | The load history
memory can be used in the future to describe other characteristics of
the response that depend on preceding load cycles.</p></td>
<td></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
<tr class="odd">
<td><code class="parameter-table-variable">cycNum</code></td>
<td><p>expected number of half-cycles during the loading
process</p></td>
</tr>
<tr class="even">
<td></td>
<td><p>Efficiency of the material can be slightly increased by correctly
setting this value. The default value is <em>$cycNum = 50</em></p></td>
</tr>
<tr class="odd">
<td></td>
<td><p>Load history memory can be turned off by setting <em>$cycNum =
0</em>.</p></td>
</tr>
<tr class="even">
<td></td>
<td></td>
</tr>
</tbody>
</table>
<p>&lt;/blockquote&gt;</p>
<h2 id="examples">Examples</h2>
<p>Coming soon...</p>
<table>
<tbody>
<tr class="odd">
<td><p><strong>Author:</strong></p></td>
<td><p>Adam Zsarnóczay: zsarnoczay@vbt.bme.hu</p></td>
</tr>
</tbody>
</table>
