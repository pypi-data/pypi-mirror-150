# Transformation Method

<p>This command is used to construct a transformation constraint
handler, which enforces the constraints using the transformation method.
The following is the command to construct a transformation constraint
handler:</p>

```tcl
constraints Transformation
```

<hr />

<p>NOTES:</p>
<ul>
<li>The single-point constraints when using the transformation method
are done directly. The matrix equation is not manipulated to enforce
them, rather the trial displacements are set directly at the nodes at
the start of each analysis step.</li>
<li>Great care must be taken when multiple constraints are being
enforced as the transformation method does not follow constraints:</li>
</ul>
<p>1) If a node is fixed, constrain it with the fix command and not
equalDOF or other type of constraint.</p>
<p>2) If multiple nodes are constrained, make sure that the retained
node is not constrained in any other constraint.</p>
<p>And remember if a node is constrained to multiple nodes in your model
it probably means you have messed up.</p>
<hr />

## Theory

<hr />
<p>Code Developed by: <span style="color:blue"> fmk
</span></p>
