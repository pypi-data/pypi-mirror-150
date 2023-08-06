# Lagrange

<p>This command is used to construct a LagrangeMultiplier constraint
handler, which enforces the constraints by introducing Lagrange
multiplies to the system of equation. The following is the command to
construct a plain constraint handler:</p>

```tcl
constraints Lagrange < $alphaS $alphaM >
```
<hr />
<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-variable">alphaS</code></p></td>
<td><p>$\alpha_S$ factor on singe points.
optional, default = 1.0</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">alphaM</code></p></td>
<td><p>$\alpha_M$ factor on multi-points,
optional default = 1.0;</p></td>
</tr>
</tbody>
</table>
<hr />
<p>NOTES:</p>
<ul>
<li>The Lagrange multiplier method introduces new unknowns to the system
of equations. The diagonal part of the system corresponding to these new
unknowns is 0.0. This ensure that the system IS NOT symmetric positive
definite.</li>
</ul>
<hr />

## Theory

<hr />
<p>Code Developed by: <span style="color:blue"> fmk
</span></p>
