# Load Control

<p>This command is used to construct a LoadControl integrator
object.</p>

```tcl
integrator LoadControl $lambda &lt;$numIter $minLambda
        $maxLambda&gt;
```
<hr />
<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-variable">lambda</code></p></td>
<td><p>the load factor increment
&lt;math&gt;\lambda&lt;/math&gt;</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">numIter</code></p></td>
<td><p>the number of iterations the user would like to occur in the
solution algorithm. Optional, default = 1.0.</p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-variable">minLambda</code></p></td>
<td><p>the min stepsize the user will allow. optional, defualt =
$\lambda_{min} = \lambda$</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">maxLambda</code></p></td>
<td><p>the max stepsize the user will allow. optional, default =
$\lambda_{max} = \lambda$</p></td>
</tr>
</tbody>
</table>
<hr />
<p>NOTES:</p>
<ol>
<li>The change in applied loads that this causes depends on the active
load patterns (those load patterns not set constant) and the loads in
the load patterns. If the only active loads acting on the domain are in
load patterns with a Linear time series with a factor of 1.0, this
integrator is the same as the classical load control method.</li>
<li>The optional arguments are supplied to speed up the step size in
cases where convergence is too fast and slow down the step size in cases
where convergence is too slow.</li>
</ol>
<hr />

## Examples

<p>integrator LoadControl 0.1;</p>
<hr />

## Theory

<p>In Load Control the time in the domain is set to $t +
\lambda_{t+1}$ where,</p>
<dl>
<dt></dt>
<dd>

$$\lambda_{t+1} = \max \left ( \lambda_{min}, \min \left (
\lambda_{max}, \frac{\text{numIter}}{\text{lastNumIter}} \lambda_{t}
\right ) \right ) $$

</dd>
</dl>
<hr />
<p>Code Developed by: <span style="color:blue">fmk</span></p>
