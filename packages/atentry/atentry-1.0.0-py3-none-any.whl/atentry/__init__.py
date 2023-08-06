"""The `atentry` module contains a simple decorator for signaling the presence of a `main` function."""
from typing import Callable, Optional


def entry(func: Callable[[], Optional[int]]) -> Callable[[], Optional[int]]:
    """`@entry` decorator. Used to signal the presence of a `main` function.

    ## Examples

    ### Simple example:

    ```python
    from atentry import entry

    @entry
    def main():
        print("Hello, world!")
    ```

    ### Using a return value:

    ```python
    from atentry import entry

    @entry
    def main() -> int:
        print("Hello, world!")
        return 128 # Program exit code
    ```

    ## Reasoning

    This decorator exists to replace the traditional `if __name__ == "__main__"` pattern.
    No real value is gained from this new method, it simply offers an alternative.

    The example snippet implemented the traditional way would be:

    ```python
    import sys

    def main() -> int:
        print("Hello, world!")
        return 128

    if __name__ == "__main__":
        sys.exit(main())
    ```

    ---

    Args:
        func (`Callable[[], Optional[int]]`): Main function. May return an exit code or nothing.

    Returns:
        `Callable[[], Optional[int]]`: Passthrough of the main function
    """    

    # If the file `func` is defined in is `__main__` then we can call it here
    if func.__module__ == "__main__":

        # Call the function and keep track of what it returns
        ret_val = func()

        # If we got a return value, we need to import `sys` to signal the exit code to the host
        if ret_val is not None:
            import sys
            sys.exit(ret_val)

    # Pass through the function
    return func
