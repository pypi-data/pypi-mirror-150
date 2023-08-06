# Plane Stress Material

<p>This command is used to construct a plane-stress material wrapper
which converts any three-dimensional material into a plane stress
material via static condensation.</p>

```tcl
nDMaterial PlaneStress $matTag
        $threeDtag
```
<hr />
<table>
<tbody>
<tr class="odd">
<td><code class="parameter-table-variable">matTag</code></td>
<td><p>integer tag identifying material</p></td>
</tr>
<tr class="even">
<td><code class="parameter-table-variable">otherTag</code></td>
<td><p>tag of perviously defined 3d ndMaterial material</p></td>
</tr>
</tbody>
</table>
<p>The material formulations for the PlaneStress object are ""Plane
Stress"</p>
<hr />
<p>Code Developed by: <span style="color:blue"> Ed Love
</span></p>
