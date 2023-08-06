# Modified Newton Algorithm

<p>This command is used to construct a ModifiedNewton algorithm object,
which uses the modified newton-raphson algorithm to solve the nonlinear
residual equation. The command is of the following form:</p>

```tcl
algorithm ModifiedNewton
        &lt;-initial&gt;
```

<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-flag">-initial</code></p></td>
<td><p>optional flag to indicate to use initial stiffness
iterations.</p></td>
</tr>
</tbody>
</table>
<hr />
<p>NOTES:</p>
<hr />

## Theory

<p>The theory for the ModifiedNewton method is similar to that for the
<a href="Newton_Algorithm" title="wikilink"> Newton-Raphson method</a>.
The difference is that the tangent at the initial guess is used in the
iterations, instead of the current tangent. The Modified Newmark method
is thus an iterative method in which, starting at a good initial guess
$U_0$ we keep iterating until &lt;math&gt;\Delta
U&lt;/math&gt; is small enough using the following:</p>

$$ \Delta U = - K_0^{-1}R(U_n),\!$$



$$ U_{n+1} = U_n + \Delta U\,\!$$


<p>where:</p>

$$K_0 = \frac{\partial R(U_0)}{\partial U}\,\!$$


<p>The advantage of this method over the regular Newton method, is that
the system Jacobian is formed only once at the start of the step and
factored only once if a direct solver is used. The drawback of this
method is that it requires more iterations than Newton's method.</p>
<p>note: when -initial flag is provided $K_0$ is
Jacobian from undeformed configuration.</p>
<hr />
<p>Code Developed by: <span style="color:blue"> fmk
</span></p>
