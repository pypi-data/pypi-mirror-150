# PressureDependMultiYield-Example 6

<table>
<tbody>
<tr class="odd">
<td><p>&lt;center&gt;<strong>Dry single BbarBrick element with pressure
dependent material</strong>&lt;/center&gt;</p></td>
</tr>
</tbody>
</table>
<h2 id="input_file">Input File</h2>
<p>&lt;syntaxhighlight lang="tcl"&gt;</p>
<ol>
<li>dry single BbarBrick element with pressure dependent material.</li>
<li>subjected to 1D sinusoidal base shaking</li>
</ol>
<p>wipe set friction 31.40 ;#friction angle set phaseTransform 26.50
;#phase transformation angle set E1 93178.4 ;#Young's modulus set
poisson1 0.40 ; set G1 [expr $E1/(2*(1+$poisson1))] ; set B1 [expr
$E1/(3*(1-2*$poisson1))] ; set gamma 0.600 ;# Newmark integration
parameter</p>
<p>set dt 0.01 ;# time step for analysis, does not have to be the same
as accDt. set numSteps 1600 ;# number of time steps set rhoS 2.00 ;#
saturated mass density set rhoF 0.00 ;# fluid mass density set
densityMult 1. ;# density multiplier</p>
<p>set Bfluid 2.2e6 ;# fluid shear modulus set fluid1 1 ;# fluid
material tag set solid1 10 ;# solid material tag</p>
<p>set accMul 4 ;# acceleration multiplier set pi 3.1415926535 ; set
inclination 0;</p>
<p>set massProportionalDamping 0.0 ; set
InitStiffnessProportionalDamping 0.001;</p>
<p>set bUnitWeightX [expr
($rhoS-0.0)*9.81*sin($inclination/180.0*$pi)*$densityMult] ;# Total unit
weight in X direction set bUnitWeightY 0.0 ;# buoyant unit weight in Y
direction set bUnitWeightZ [expr
-($rhoS-$rhoF)*9.81*cos($inclination/180.0*$pi)] ;# buoyant unit weight
in Z direction</p>
<p>set ndm 3 ;# space dimension</p>
<p>model BasicBuilder -ndm $ndm -ndf $ndm</p>
<p>nDMaterial PressureDependMultiYield $solid1 $ndm [expr
$rhoS*$densityMult] $G1 $B1 $friction 0.1 80 0.5 \ $phaseTransform 0.17
0.4 10 10 0.015 1.0 ;# 27 0.6 0 0 0 101 0.630510273</p>
<p>node 1 0.00000 0.0000 0.00000 node 2 0.00000 0.0000 1.00000 node 3
0.00000 1.0000 0.00000 node 4 0.00000 1.0000 1.00000 node 5 1.00000
0.0000 0.00000 node 6 1.00000 0.0000 1.00000 node 7 1.00000 1.0000
0.00000 node 8 1.00000 1.0000 1.00000</p>
<p>element bbarBrick 1 1 5 7 3 2 6 8 4 $solid1 $bUnitWeightX
$bUnitWeightY $bUnitWeightZ</p>
<p>updateMaterialStage -material $solid1 -stage 0</p>
<p>fix 1 1 1 1 0 0 0 fix 2 0 1 0 0 0 0 fix 3 1 1 1 0 0 0 fix 4 0 1 0 0 0
0 fix 5 1 1 1 0 0 0 fix 6 0 1 0 0 0 0 fix 7 1 1 1 0 0 0 fix 8 0 1 0 0 0
0</p>
<ol>
<li>equalDOF</li>
<li>tied nodes around</li>
</ol>
<p>equalDOF 2 4 1 3 equalDOF 2 6 1 3 equalDOF 2 8 1 3</p>
<p>set nodeList {} for {set i 1} {$i &lt;= 8 } {incr i 1} { lappend
nodeList $i }</p>
<p>set elementList {} for {set i 1} {$i &lt;= 1 } {incr i 1} { lappend
elementList $i }</p>
<ol>
<li>GRAVITY APPLICATION (elastic behavior)</li>
<li>create the SOE, ConstraintHandler, Integrator, Algorithm and
Numberer</li>
</ol>
<p>system ProfileSPD test NormDispIncr 1.D-10 25 2 constraints
Transformation integrator LoadControl 1 1 1 1 algorithm Newton numberer
RCM analysis Static analyze 2</p>
<ol>
<li>switch the material to plastic</li>
</ol>
<p>updateMaterialStage -material $solid1 -stage 1 updateMaterials
-material $solid1 bulkModulus [expr $G1*2/3.];</p>
<p>analyze 2</p>
<p>setTime 0.0 ;# reset time, otherwise reference time is not zero for
time history analysis wipeAnalysis</p>
<ol>
<li><ol>
<li>create recorders ##############################</li>
</ol></li>
</ol>
<p>eval "recorder Node -file allNodesDisp.out -time -node $nodeList -dof
1 2 3 -dT 0.01 disp" eval "recorder Node -file allNodesAcce.out -time
-node $nodeList -dof 1 2 3 -dT 0.01 accel" eval "recorder Element -ele
$elementList -time -file stress1.out -dT 0.01 material 1 stress" eval
"recorder Element -ele $elementList -time -file strain1.out -dT 0.01
material 1 strain" eval "recorder Element -ele $elementList -time -file
stress5.out -dT 0.01 material 5 stress" eval "recorder Element -ele
$elementList -time -file strain5.out -dT 0.01 material 5 strain" eval
"recorder Element -ele $elementList -file backbone.out -dT 1000 material
1 backbone 80 100 200 300"</p>
<ol>
<li><ol>
<li>create dynamic time history analysis ##################</li>
</ol></li>
</ol>
<p>pattern UniformExcitation 1 1 -accel "Sine 0 10 1 -factor $accMul"
rayleigh $massProportionalDamping 0.0 $InitStiffnessProportionalDamping
0. integrator Newmark $gamma [expr pow($gamma+0.5, 2)/4] constraints
Penalty 1.e18 1.e18 ;# can't combine with test NormUnbalance test
NormDispIncr 1.0e-10 25 0 ;# can't combine with constraints Lagrange</p>
<ol>
<li>algorithm Newton ;# tengent is updated at each iteration</li>
</ol>
<p>algorithm ModifiedNewton ;# tengent is updated at the begining of
each time step not each iteration system ProfileSPD ;# Use sparse
solver. Next numberer is better to be Plain. numberer Plain ;# method to
map between between equation numbers of DOFs analysis VariableTransient
;# splitting time step requires VariableTransient</p>
<ol>
<li><ol>
<li>perform the Analysis and record time used #############</li>
</ol></li>
</ol>
<p>set startT [clock seconds] analyze $numSteps $dt [expr $dt/64] $dt 15
set endT [clock seconds] puts "Execution time: [expr $endT-$startT]
seconds." &lt;/syntaxhighlight&gt;</p>
<h2 id="matlab_plotting_file">MATLAB Plotting File</h2>
<p>&lt;syntaxhighlight lang="matlab"&gt; clear all;</p>
<p>a1=load('allNodesAcce.out'); d1=load('allNodesDisp.out');
s1=load('stress1.out'); e1=load('strain1.out'); s5=load('stress5.out');
e5=load('strain5.out');</p>
<p>fs=[0.5, 0.2, 4, 6]; accMul = 4;</p>
<p>%integration point 1 p-q po=(s1(:,2)+s1(:,3)+s1(:,4))/3; for
i=1:size(s1,1) qo(i)=(s1(i,2)-s1(i,3))^2 + (s1(i,3)-s1(i,4))^2
+(s1(i,2)-s1(i,4))^2 + 6.0* s1(i,5)^2 + 6.0* s1(i,6)^2 + 6.0* s1(i,7)^2;
qo(i)=sign(s1(i,7))*1/3.0*qo(i)^0.5; end figure(1); clf; %integration
point 1 stress-strain subplot(2,1,1), plot(e1(:,7),s1(:,7),'r'); title
('Integration point 1 shear stress \tau_x_y VS. shear strain
\epsilon_x_y'); xLabel('Shear strain \epsilon_x_y'); yLabel('Shear
stress \tau_x_y (kPa)');</p>
<p>subplot(2,1,2), plot(-po,qo,'r'); title ('Integration point 1
confinement p VS. deviatoric q relation'); xLabel('confinement p
(kPa)'); yLabel('q (kPa)'); set(gcf,'paperposition',fs);
saveas(gcf,'SS_PQ1','jpg');</p>
<p>%integration point 5 p-q po=(s5(:,2)+s5(:,3)+s5(:,4))/3; for
i=1:size(s5,1) qo(i)=(s5(i,2)-s5(i,3))^2 + (s5(i,3)-s5(i,4))^2
+(s5(i,2)-s5(i,4))^2 + 6.0* s5(i,5)^2 + 6.0* s5(i,6)^2 + 6.0* s5(i,7)^2;
qo(i)=sign(s5(i,7))*1/3.0*qo(i)^0.5; end</p>
<p>figure(4); clf; %integration point 5 stress-strain subplot(2,1,1),
plot(e5(:,7),s5(:,7),'r'); title ('Integration point 5 shear stress
\tau_x_y VS. shear strain \epsilon_x_y'); xLabel('Shear strain
\epsilon_x_y'); yLabel('Shear stress \tau_x_y (kPa)');</p>
<p>subplot(2,1,2), plot(-po,qo,'r'); title ('Integration point 5
confinement p VS. deviatoric q relation'); xLabel('confinement p
(kPa)'); yLabel('q (kPa)'); set(gcf,'paperposition',fs);
saveas(gcf,'SS_PQ5','jpg');</p>
<p>figure(2); clf; %node 3 displacement relative to node 1
subplot(2,1,1),plot(d1(:,1),d1(:,5),'r'); title ('Lateral displacement
at element top'); xLabel('Time (s)'); yLabel('Displacement (m)');
set(gcf,'paperposition',fs); saveas(gcf,'D','jpg');</p>
<p>s=accMul*sin(0:pi/50:20*pi); s=[s';zeros(1000,1)];
s1=interp1(0:0.01:20,s,a1(:,1));</p>
<p>figure(3); clf; %node 3 acceleration
subplot(2,1,1),plot(a1(:,1),s1+a1(:,5),'r'); title ('Lateral
acceleration at element top'); xLabel('Time (s)'); yLabel('Acceleration
(m/s^2)'); set(gcf,'paperposition',fs); saveas(gcf,'A','jpg');</p>
<p>&lt;/syntaxhighlight&gt;</p>
<h2 id="displacement_output_file">Displacement Output File</h2>
<figure>
<img src="/OpenSeesRT/contrib/static/PD_Ex13Disp.png" title="PD_Ex13Disp.png"
alt="PD_Ex13Disp.png" />
<figcaption aria-hidden="true">PD_Ex13Disp.png</figcaption>
</figure>
<h2 id="stress_strain_output_file">Stress-Strain Output File</h2>
<figure>
<img src="/OpenSeesRT/contrib/static/PD_Ex13SS_PQ13.png" title="PD_Ex13SS_PQ13.png"
alt="PD_Ex13SS_PQ13.png" />
<figcaption aria-hidden="true">PD_Ex13SS_PQ13.png</figcaption>
</figure>
<h2 id="acceleration_output_file">Acceleration Output File</h2>
<figure>
<img src="/OpenSeesRT/contrib/static/PD_Ex13Accel.png" title="PD_Ex13Accel.png"
alt="PD_Ex13Accel.png" />
<figcaption aria-hidden="true">PD_Ex13Accel.png</figcaption>
</figure>
<hr />
<p>Return to: </p>
