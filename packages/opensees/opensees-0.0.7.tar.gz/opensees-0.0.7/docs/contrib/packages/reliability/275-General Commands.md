# General Commands

<p>:;&lt;h2&gt;<a href="reliability_Command"
title="wikilink">reliability Command</a>&lt;/h2&gt;</p>
<dl>
<dt></dt>
<dd>
This command creates the reliability domain in which the sensitivity,
reliability and optimization components are kept. This
</dd>
<dd>
reliability domain is parallel to the finite element (FE) domain in
OpenSees. Currently, the commands for stand-alone sensitivity :analysis
(e.g., sensitivityIntegrator, sensitivityAlgorithm) are set in the
reliability domain only and, thus, the ‘reliability’
</dd>
</dl>

```tcl
reliability
```
<p>&lt;h2&gt;<a href="parameter_Command" title="wikilink">parameter
Command</a>&lt;/h2&gt;</p>
<dl>
<dt></dt>
<dd>
In DDM-based FE response sensitivity analysis, the sensitivity
parameters can be material,
</dd>
<dd>
geometry or discrete loading parameters. Each parameter should be
defined as:
</dd>
</dl>

```tcl
parameter $tag &lt;specific object
        arguments&gt;
```
<p>&lt;h2&gt;<a href="addToParameter_Command"
title="wikilink">addToParameter Command</a>&lt;/h2&gt;</p>
<dl>
<dt></dt>
<dd>
In case that more objects (e.g., element, section) are mapped to an
existing parameter, the following command can be used to
</dd>
<dd>
relate these additional objects to the specific parameter:
</dd>
</dl>

```tcl
addToParameter $tag &lt;specific object
        arguments&gt;
```
<p>&lt;h2&gt;<a href="updateParameter_Command"
title="wikilink">updateParameter Command</a>&lt;/h2&gt;</p>
<dl>
<dt></dt>
<dd>
Once the parameters in FE model are defined, their value can be updated:
</dd>
</dl>

```tcl
updateParameter $tag $newValue
```
<p>&lt;h2&gt;<a href="sensitivityIntegrator_Command"
title="wikilink">sensitivityIntegrator Command</a>&lt;/h2&gt;</p>
<dl>
<dt></dt>
<dd>
For static analysis, the only option currently available is the
following, which must be defined before the ‘analysis’ command.
</dd>
</dl>

```tcl
sensitivityIntegrator -static
```
<dl>
<dt></dt>
<dd>
For the dynamic case, currently only the Newmark algorithm is available.
Two command need to be used together:
</dd>
</dl>

```tcl
integrator NewmarkWithSensitivity $gamma
        $beta
```
<dl>
<dt></dt>
<dd>

</dd>
</dl>

```tcl
sensitivityIntegrator -definedAbove
```
<dl>
<dt></dt>
<dd>
Currently, ‘-definedAbove’ is the only option available in OpenSees.
This means that the same integration scheme (i.e.,
</dd>
<dd>
‘NewmarkWithSensitivity’) is used to perform both response and response
sensitivity analysis.
</dd>
</dl>
<p>&lt;h2&gt;<a href="sensitivityAlgorithm_Command"
title="wikilink">sensitivityAlgorithm Command</a>&lt;/h2&gt;</p>
<dl>
<dt></dt>
<dd>
The most general command is the following, which computes the response
sensitivity at each time/load step, after the response
</dd>
<dd>
has converged.
</dd>
</dl>

```tcl
sensitivityAlgorithm -computeAtEachStep
```
<dl>
<dt></dt>
<dd>
In those cases in which the sensitivity computation does not need to be
performed at each step (e.g., for linear elastic systems : subjected to
static pushover analysis), the sensitivity computation may be performed
only at the time/load steps required by
</dd>
<dd>
user:
</dd>
</dl>

```tcl
sensitivityAlgorithm -computeByCommand
```
<dl>
<dt></dt>
<dd>
However, before using the ‘-computeByCommand’ option, it is the user’s
responsibility to make sure that the response
</dd>
<dd>
sensitivities computation is not needed at each time/load step. For
example, in case of incremental nonlinear FE analysis or
</dd>
<dd>
dynamic analysis, using the ‘-computeByCommand’ option will produce
wrong sensitivity results.
</dd>
</dl>
<p>&lt;h2&gt;<a href="recorder_Commands" title="wikilink">recorder
Commands</a>&lt;/h2&gt;</p>
<dl>
<dt></dt>
<dd>
To record the nodal response and response sensitivity, the most commonly
used format is:
</dd>
</dl>

```tcl
recorder Node -file disp29.out -time -node 29 -dof 1
        &lt;-precision 16 &gt; disp
```

<table>
<tbody>
<tr class="odd">
<td><p><strong>recorder Node -file ddm29G1.out -time -node 29 -dof 1
"sensitivity 1"</strong></p></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr class="odd">
<td><p><strong>recorder Node -file ddm29G1.out -time -node 29 -dof 1
"velSensitivity 1"</strong></p></td>
</tr>
</tbody>
</table>

```tcl
recorder Node -file ddm29G1.out -time -node 29 -dof 1
        "accSensitivity 1"
```
<dl>
<dt></dt>
<dd>
The above ‘recorder’ commands (extended for recording response
sensitivities) save into files (with the file name defined after : the
command ‘-file’) the responses and response sensitivities of the node 29
along the first degree of freedom (dof) direction. : Response quantities
can be ‘disp’ (displacements), ‘vel’ (velocities) and ‘acc’
(accelerations). Response sensitivities are
</dd>
<dd>
denoted by a string in double quotes and containing the response
quantity identifier (i.e., “sensitivity” for displacements,
</dd>
<dd>
“velSensitivity” for velocities and “accSensitivity” for accelerations)
and the sensitivity parameter specified by the parameter : tag ( in this
example the tag is 1).
</dd>
</dl>
<dl>
<dt></dt>
<dd>
The command ‘-precision’ is optional, and allows users to change the
number of digits used to record into file the response
</dd>
<dd>
and/or response sensitivities. This command is particularly useful when
the finite difference method is used to verify/validate : DDM-based FE
response sensitivities, since high accuracy in the results may be
needed.
</dd>
</dl>
<dl>
<dt></dt>
<dd>
The user may also get responses and response sensitivities directly
using the following Tcl commands:
</dd>
</dl>
<table>
<tbody>
<tr class="odd">
<td><p><strong>nodeDisp 29 1</strong></p></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr class="odd">
<td><p><strong>nodeVel 29 1</strong></p></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr class="odd">
<td><p><strong>nodeAccel 29 1</strong></p></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr class="odd">
<td><p><strong>sensNodeDisp 29 1 2</strong></p></td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr class="odd">
<td><p><strong>sensNodeVel 29 1 2</strong></p></td>
</tr>
</tbody>
</table>

```tcl
sensNodeAccel 29 1 2
```
<dl>
<dt></dt>
<dd>
These commands return the responses of the node 29 along the first dof,
and their response sensitivities with respect to the
</dd>
<dd>
parameter with tag 2
</dd>
</dl>
