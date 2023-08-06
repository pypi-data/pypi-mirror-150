# Lagrange

This command is used to construct a `LagrangeMultiplier` constraint
handler, which enforces the constraints by introducing Lagrange
multiplies to the system of equation. The following is the command to
construct a plain constraint handler:

```tcl
constraints Lagrange <$alphaS $alphaM >
```

------------------------------------------------------------------------

  -------------- ------------------------------------------------------------
  **\$alphaS**   $\alpha_S$ factor on singe points. optional, default = 1.0
  **\$alphaM**   $\alpha_M$ factor on multi-points, optional default = 1.0;
  -------------- ------------------------------------------------------------

------------------------------------------------------------------------

NOTES:

-   The Lagrange multiplier method introduces new unknowns to the system
    of equations. The diagonal part of the system corresponding to these
    new unknowns is 0.0. This ensure that the system IS NOT symmetric
    positive definite.

------------------------------------------------------------------------

THEORY:

------------------------------------------------------------------------

Code Developed by: `<span style="color:blue">`{=html} fmk
`</span>`{=html}


## C++ Interface

```cpp
#include <analysis/handler/LagrangeConstraintHandler.h>

class LagrangeConstraintHandler:  public ConstraintHandler;
```

The LagrangeConstraintHandler class is a class which deals with both
single and multi point constraints using the Lagrange method. This is
done by, in addition to creating a `DOF_Group` object for each Node and an
FE_Element for each Element in the Domain, creating a LagrangeDOF_Group
object and either a LagrangeSP_FE or a LagrangeMP_FE object for each
constraint in the Domain. It is these objects that enforce the
constraints by modifying the tangent matrix and residual vector.



The integer `HANDLER_TAG_LagrangeConstraintHandler` (defined in
 `<classTags.h>`) is passed to the LagrangeConstraintHandler
constructor. Stores `alphaSP` and `alphaMP` which are needed to
construct the `LagrangeSP_FE` and `LagrangeMP_FE` objects in `handle()`.

### Destructor
Currently invokes `clearAll()`, this will change when `clearAll()` is
rewritten.

### Methods
Determines the number of FE_Elements and DOF_Groups needed from the
Domain (a one to one mappinging between Elements and FE_Elements,
SP_Constraints and LagrangeSP_FEs, MP_Constraints and LagrangeMP_FEs and
Nodes and DOF_Groups). Creates two arrays of pointers to store the
FE_Elements and DOF_Groups, returning a warning message and a $-2$ or
$-3$ if not enough memory is available for these arrays. Then the object
will iterate through the Nodes of the Domain, creating a `DOF_Group` for
each node and setting the initial id for each dof to $-2$ or $-3$ if the
node identifier is in *nodesToBeNumberedLast*. The object then iterates
through the Elements of the Domain creating a `FE_Element` for each
Element, if the Element is a Subdomain `setFE_ElementPtr()` is invoked
on the Subdomain with the new `FE_Element` as the argument. If not enough
memory is available for any `DOF_Group` or `FE_Element` a warning message is
printed and a $-4$ or $-5$ is returned. The object then iterates through
the SP_Constraints of the Domain creating a LagrangeSP_FE for each
constraint, using the Domain, the constraint and *alphaSP* as the
arguments in the constructor. The object then iterates through the
MP_Constraints of the Domain creating a LagrangeMP_FE for each
constraint, using the Domain, the constraint and *alphaMP* as the
arguments in the constructor. Finally the method returns the number of
degrees-of-freedom associated with the `DOF_Groups` in
`nodesToBeNumberedLast`.

```{.cpp}
virtual void clearAll(void) =0;
```
Currently this invokes delete on all the `FE_Element` and DOF_Group
objects created in `handle()` and the arrays used to store pointers to
these objects. FOR ANALYSIS INVOLVING DYNAMIC LOAD BALANCING, RE-MESHING
AND CONTACT THIS MUST CHANGE.

```cpp
int sendSelf(int commitTag, Channel &theChannel);
```
Sends in a Vector of size 2 *alphaSP* and *alphaMP*. Returns $0$ if
successful.

```cpp
int recvSelf(int commitTag, Channel &theChannel, FEM_ObjectBroker &theBroker);
```
Receives in a Vector of size 2 the values *alphaSP* and *alphaMP*.
Returns $0$ if successful.

