# Plain

<p>This command is used to construct a Plain constraint handler. A plain
constraint handler can only enforce homogeneous single point constraints
(fix command) and multi-point constraints constructed where the
constraint matrix is equal to the identity (equalDOF command). The
following is the command to construct a plain constraint handler:</p>

```tcl
constraints Plain
```
<hr />
<p>NOTES:</p>
<ul>
<li>As mentioned, this constraint handler can only enforce homogeneous
single point constraints (fix command) and multi-pont constraints where
the constraint matrix is equal to the identity (equalDOF command).</li>
</ul>
<hr />
<p>Code Developed by: <span style="color:blue"> fmk
</span></p>
