# Krylov-Newton Algorithm

<p>This command is used to construct a KrylovNewton algorithm object
which uses a Krylov subspace accelerator to accelerate the convergence
of the modified newton method. The command is of the following form:</p>

```tcl
algorithm KrylovNewton &lt;-iterate $tangIter&gt;
        &lt;-increment $tangIncr&gt; &lt;-maxDim $maxDim&gt;
```

<table>
<tbody>
<tr class="odd">
<td><p><code class="parameter-table-variable">tangIter</code></p></td>
<td><p>tangent to iterate on, options are current, initial, noTangent.
default is current.</p></td>
</tr>
<tr class="even">
<td><p><code class="parameter-table-variable">tangIncr</code></p></td>
<td><p>tangent to increment on, options are current, initial, noTangent.
default is current</p></td>
</tr>
<tr class="odd">
<td><p><code class="parameter-table-variable">maxDim</code></p></td>
<td><p>max number of iterations until the tangent is reformed and the
acceleration restarts (default = 3).</p></td>
</tr>
</tbody>
</table>
<hr />
<p>NOTES:</p>
<hr />
<p>REFERENCES:</p>
<p>Scott, M.H. and G.L. Fenves. "A Krylov Subspace Accelerated Newton
Algorithm: Application to Dynamic Progressive Collapse Simulation of
Frames." Journal of Structural Engineering, 136(5), May 2010. <a
href="http://dx.doi.org/10.1061/(ASCE)ST.1943-541X.0000143">DOI</a></p>
<hr />
<p>Code Developed by: <span style="color:blue"> Michael Scott,
Oregon State University </span></p>
