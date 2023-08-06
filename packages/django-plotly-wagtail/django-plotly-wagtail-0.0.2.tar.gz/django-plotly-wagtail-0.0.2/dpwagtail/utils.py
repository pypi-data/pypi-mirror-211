"""
Utility functions
"""


def form_instance_builders(InstanceBuilder):
    """Create and add instance builders.

    The model is passed in, and not imported, so this function can
    be executed from a view.
    """

    items = {'Trivial no-arguments': {'args': {}},
             }

    res = []
    for name, kwargs in items.items():
        if InstanceBuilder.objects.filter(name=name).count() > 0:
            res.append((name, 0))
        else:
            ib = InstanceBuilder(name=name,
                                 **kwargs)
            ib.save()
            res.append((name, 1))
    return res
