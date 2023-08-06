from __future__ import annotations
from jax import config
config.update("jax_debug_nans", True)
import zodiax


# Paths
paths = [
    'param',
    'b.param',
    ['param', 'b.param'],
]


def test_boolean_filter(create_base):
    pytree = create_base()
    for path in paths:
        zodiax.tree.boolean_filter(pytree, path)


def test_set_array(create_base):
    pytree = create_base()
    for path in paths:
        zodiax.tree.set_array(pytree, path)