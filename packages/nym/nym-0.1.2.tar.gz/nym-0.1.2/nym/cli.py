"""Cli script for nym."""
import sys
import time

import click

from nym import fast, slow


@click.command()
def main(args=None):
    """Console script for nym."""
    click.echo("Running fib(33)...")

    start = time.time()
    python_ret = slow.fib(33)
    python_time = time.time() - start

    restart = time.time()
    nim_ret = fast.fib(33)
    nim_time = time.time() - restart

    print("====================================")
    print(f"python ret: {python_ret}")
    print(f"python elapsed time : {python_time}")

    print(f"nim ret: {nim_ret}")
    print(f"nim elapsed time    : {nim_time}")

    print("====================================")
    times_faster = round(python_time / nim_time, 3)
    print(f"nim fib implementation is {times_faster}x faster than python's!")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
