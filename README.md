# FindRootsAndInverseValues

In analysis, the task is often to find roots of functions $f$, i.e. solve the equation $f(x) = 0$. 
One such method for this purpose is the [bisection algorithm](https://en.wikipedia.org/wiki/Bisection_method), which is based on the [intermediate value theorem](https://en.wikipedia.org/wiki/Intermediate_value_theorem). The script can only find **one** root of a function, and the root is searched over a compact set $[a, b]$. 

In addition, with the bisection method, the inverse value of a function at a point $y$ can be found, i.e. $f^{-1}(y)$. For this, note that 
$$x = f^{-1}(y) \Leftrightarrow f(x) = y \Leftrightarrow y - f(x) = 0,$$
so finding $f^{-1}(y)$ can be boiled down to solving a root problem. 

## Usage
The script `bisection.py` hardcodes the function $f$ in the function `function(x: Union[float, np.ndarray])`, however, $f$ can obviously be easily changed. 
