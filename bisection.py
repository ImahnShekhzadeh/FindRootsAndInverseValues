import time
from typing import Callable, Tuple, Union

import numpy as np


def function(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Function for which we find the root: $f(x) = x^3 - 2x - 5$.

    Args:
        x: Value(s) at which to evaluate the function.

    Returns:
        Numpy array or float with function evaluations for the provided `x`.

    """
    return (x - 2) ** 3


def check_strict_monotonicity(
    function: Callable, a: float = 0.0, b: float = 1.0
) -> bool:
    """Check whether `function` is strictly monotonically increasing or
    decreasing over the interval `[a, b]`.

    Args:
        function: Function to check for strict monotonicity.
        a: Left endpoint of the interval.
        b: Right endpoint of the interval.

    Returns:
        Boolean indicating whether `function` is strictly monotonically
        increasing or decreasing
    """
    if function(x=a) > function(x=b):
        print(
            f"Function `f` is strictly monotonically decreasing over the "
            f"interval {[a, b]}."
        )
        is_increasing = False
    elif function(x=a) < function(x=b):
        print(
            f"Function `f` is strictly monotonically increasing over the "
            f"interval {[a, b]}."
        )
        is_increasing = True
    else:
        raise ValueError(
            f"Function `f` is not strictly monotonic over the "
            f"interval {[a, b]}."
        )

    return is_increasing


def find_root(
    function: Callable,
    a: float = 0.0,
    b: float = 1.0,
    tolerance: float = 1e-6,
    is_increasing: bool = True,
    y: float = 0.0,
    run_time_limit: float = 60.0,
) -> Tuple[float, float, float]:
    """Find the root of the function using bisection method.

    Args:
        a: Left endpoint of the interval.
        b: Right endpoint of the interval.
        tolerance: Tolerance level for the root.
        is_increasing: Boolean indicating whether the function is strictly
            monotonically increasing or decreasing over the interval `[a, b]`.
        y: If we want to find the inverse value of `function` for `y`, we can
            do this by finding the root of the function `y - f(x)`.
        run_time_limit: If the algorithm runs for longer than this time limit,
            it will stop and return the current best estimate.

    Returns:
        Float with the root of the function, the required time to find the root
        and the function evaluation at the root.

    Raises:
        AssertionError: If the interval is not defined as `[a, b]` with
            `a < b`.
        AssertionError: If the tolerance is not a positive number.
    """
    start_time = time.perf_counter()

    assert a < b, "The interval must be defined as `[a, b]` with `a < b`."
    assert tolerance > 0, "The tolerance must be a positive number."

    is_increasing = check_strict_monotonicity(a=a, b=b, function=function)
    if y != 0.0:
        # We are searching for root of `y - function(x)`, so if `function(x)`
        # is strictly monotonically increasing, then `y - function(x)` is
        # strictly monotonically decreasing and vice versa.
        is_increasing = not is_increasing

    converged = False
    while not converged:
        # 1. Find the midpoint `c = (a + b) / 2`.
        c = (a + b) / 2
        # 2. Evaluate the function at the midpoint.
        if y == 0.0:
            # We are finding the root of `function`.
            func_midpoint = function(x=c)
        else:
            # We are finding the inverse value of `function` for `y`.
            func_midpoint = y - function(x=c)
        # 3. If the function value at the midpoint is close enough to zero, we
        # are done. Otherwise, if the function value at the midpoint is
        # positive, the root is in the left half of the interval, otherwise it
        # is in the right half of the interval.
        if abs(func_midpoint) <= tolerance:
            return c, time.perf_counter() - start_time, func_midpoint
        else:
            if is_increasing:
                if func_midpoint > 0:
                    b = c
                else:
                    a = c
            else:
                if func_midpoint > 0:
                    a = c
                else:
                    b = c
            converged = False

        if time.perf_counter() - start_time > run_time_limit:
            print(
                f"Time limit of {run_time_limit} s reached. "
                f"Returning current best estimate, which is {c}."
                f"\nFunction evaluation: {func_midpoint}."
            )

            return c, time.perf_counter() - start_time, func_midpoint


def find_inverse_value(
    function: Callable,
    y: float,
    a: float = 0.0,
    b: float = 1.0,
    tolerance: float = 1e-6,
    is_increasing: bool = True,
) -> Tuple[float, float]:
    """Find the inverse value of `function` using bisection method.
    This is done as described in
    https://math.stackexchange.com/questions/1440818/finding-the-inverse-of-a-function-using-bisection-method

    Args:
        y: Value for which to find the inverse value of `function`, i.e.
            `function^{-1}(y)`.
        --for the rest of the arguments, see `find_root`--

    Returns:
        Float with the inverse value of `function` for `y` and the required
        time to find the inverse value.
    """
    start_time = time.perf_counter()

    assert a <= y <= b, "The value `y` must be in the interval `[a, b]`."

    inverse_value, _, _ = find_root(
        function=function,
        a=a,
        b=b,
        tolerance=tolerance,
        is_increasing=is_increasing,
        y=y,
        run_time_limit=180.0,  # 3 minutes
    )

    return inverse_value, time.perf_counter() - start_time


def main() -> None:
    root, time_req_root, func_eval = find_root(
        function=function, a=-5.0, b=5.0, tolerance=1e-10
    )
    print(
        f"Found root at `x = {root}` in {round(time_req_root, 6)} s."
        f"\nFunction evaluation: {func_eval}.\n\n"
    )

    y = 3.0
    inverse, time_req_inverse = find_inverse_value(
        function=function, y=y, a=0.0, b=5.0, tolerance=1e-10
    )
    print(
        f"Found inverse value `f^(-1)(y={y}) = {round(inverse, 6)}` in "
        f"{round(time_req_inverse, 6)} s."
    )


if __name__ == "__main__":
    main()
