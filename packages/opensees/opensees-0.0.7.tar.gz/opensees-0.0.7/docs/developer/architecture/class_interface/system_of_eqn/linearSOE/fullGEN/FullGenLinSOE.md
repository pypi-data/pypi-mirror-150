# FullGenLinSOE

```cpp
#include<~/system_of_eqn/linearSOE/fullGEN/FullGenLinSOE.h>

class FullGenLinSOE: public LinearSOE
```

   MovableObject
   SystemOfEqn


`FullGenLinSOE` is class which is used to store a full general system. The
$A$ matrix is stored in a 1d double array with $n*n$ elements, where $n$
is the size of the system. $A_{i,j}$ is stored at location $(i + j*(n)$,
where $i$ and $j$ range from $0$ to $n-1$, i.e. C notation. 

For example, when $n=3$:

$$\left[
\begin{array}{ccc}
a_{0,0} & a_{0,1}  & a_{0,2}  \\
a_{1,0} & a_{1,1} & a_{1,2}  \\
a_{2,0} & a_{2,1} & a_{2,2} \\
\end{array}
\right]$$

is stored as:

$$\left[
\begin{array}{cccccccccccccccccccc}
a_{0,0} & a_{1,0}  & a_{2,0} & a_{0,1} & a_{1,1} & a_{2,1} &
a_{0,2} & a_{1,2} & a_{2,2}  \\
\end{array}
\right]$$

The $x$ and $b$ vectors are stored in 1d double arrays of length $n$. To
allow the solvers access to this data, the solvers that use this class
are all declared as friend classes.





\

The `solver` and a unique class tag (defined in  `<classTags.h>`) are
passed to the LinearSOE constructor. The system size is set to $0$ and
the matrix $A$ is marked as not having been factored. Invokes
`setLinearSOE(*this)` on the `solver`. No memory is allocated for the 3
1d arrays.

```cpp
FullGenLinSOE(int N, FullGenLinSolver &solver);
```
The `solver` and a unique class tag (defined in  `<classTags.h>`) are
passed to the LinearSOE constructor. The system size is set to $N$ and
the matrix $A$ is marked as not having been factored. Obtains memory
from the heap for the 1d arrays storing the data for $A$, $x$ and $b$
and stores the size of these arrays. If not enough memory is available
for these arrays a warning message is printed and the system size is set
to $0$. Invokes `setLinearSOE(\*this)`{.cpp} and `setSize()` on `solver`,
printing a warning message if `setSize()` returns a negative number.
Also creates Vector objects for $x$ and $b$ using the *(double \*,int)*
Vector constructor.

### Destructor

```cpp
~FullGenLinSOE();
```

Calls `delete` on any arrays created.

### Methods


```cpp
int setFullGEnSolver(FullGenLinSolver &newSolver);
```
Invokes `setLinearSOE(\*this)`{.cpp} on *newSolver*. If the system size is not
equal to $0$, it also invokes `setSize()` on *newSolver*, printing a
warning and returning $-1$ if this method returns a number less than
$0$. Finally it returns the result of invoking the LinearSOE classes
`setSolver()` method.


```cpp
int getNumEqn(void) =0;
```

A method which returns the current size of the system.

```cpp
int setSize(const Graph &theGraph);
```

The size of the system is determined by invoking `getNumVertex()` on
`theGraph`. If the old space allocated for the 1d arrays is not big
enough, it the old space is returned to the heap and new space is
allocated from the heap. Prints a warning message, sets size to $0$ and
returns a $-1$, if not enough memory is available on the heap for the 1d
arrays. If memory is available, the components of the arrays are zeroed
and $A$ is marked as being unfactored. If the system size has increased,
new Vector objects for $x$ and $b$ using the `(double \*,int)`{.cpp} Vector
constructor are created. Finally, the result of invoking `setSize()` on
the associated Solver object is returned.



```cpp
int addA(const Matrix &M, const ID &loc, doublefact = 1.0) =0;
```
First tests that *loc* and *M* are of compatible sizes; if not a warning
message is printed and a $-1$ is returned. The LinearSOE object then
assembles *fact* times the Matrix *M* into the matrix $A$. The Matrix is
assembled into $A$ at the locations given by the ID object *loc*, i.e.

$$a_{loc(i),loc(j)} += \texttt{fact} * M(i,j)$$
.

If the location specified is outside the range, i.e.
$(-1,-1)$ the corresponding entry in *M* is not added to $A$. If *fact*
is equal to $0.0$ or $1.0$, more efficient steps are performed. Returns
$0$.

```cpp
int addB(const Vector & V, const ID & loc, double fact = 1.0) =0;
```

First tests that *loc* and *V* are of compatible sizes; if not a warning
message is printed and a $-1$ is returned. The LinearSOE object then
assembles *fact* times the Vector *V* into the vector $b$. The Vector is
assembled into $b$ at the locations given by the ID object *loc*, i.e.
$b_{loc(i)} += fact * V(i)$. If a location specified is outside the
range, e.g. $-1$, the corresponding entry in *V* is not added to $b$. If
*fact* is equal to $0.0$, $1.0$ or $-1.0$, more efficient steps are
performed. Returns $0$.

```cpp
int setB(const Vector & V, double fact = 1.0) =0;
```

First tests that *V* and the size of the system are of compatible sizes;
if not a warning message is printed and a $-1$ is returned. The
LinearSOE object then sets the vector *b* to be *fact* times the Vector
*V*. If *fact* is equal to $0.0$, $1.0$ or $-1.0$, more efficient steps
are performed. Returns $0$.

```{.cpp}
void zeroA(void) =0;
```

Zeros the entries in the 1d array for $A$ and marks the system as not
having been factored.

```{.cpp}
void zeroB(void) =0;
```

Zeros the entries in the 1d array for $b$.

```{.cpp}
const Vector &getX(void) = 0;
```

Returns the Vector object created for $x$.

```{.cpp}
const Vector &getB(void) = 0;
```

Returns the Vector object created for $b$.

```{.cpp}
double normRHS(void) =0;
```

Returns the 2-norm of the vector $x$.

```{.cpp}
void setX(int loc, double value) =0;
```

If *loc* is within the range of $x$, sets $x(\texttt{loc}) = \texttt{value}$.

```cpp
int sendSelf(int commitTag, Channel &theChannel);
```
Returns $0$. The object does not send any data or connectivity
information as this is not needed in the framework design.

```cpp
int recvSelf(int commitTag, Channel &theChannel, FEM_ObjectBroker
```
Returns $0$. The object does not receive any data or connectivity
information as this is not needed in the framework's design.
