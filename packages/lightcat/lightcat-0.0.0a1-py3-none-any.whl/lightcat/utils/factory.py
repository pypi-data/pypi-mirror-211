__all__ = ["setup_object", "str_target_object"]

import logging
from typing import TypeVar, Union

from objectory import OBJECT_TARGET, factory

logger = logging.getLogger(__name__)

T = TypeVar("T")


def setup_object(obj_or_config: Union[T, dict]) -> T:
    r"""Sets up an object from its configuration.

    Args:
    ----
        obj_or_config: Specifies the object or its configuration.

    Returns:
    -------
        The instantiated object.

    Example usage:

    .. code-block:: pycon

       >>> from lightcat.utils import setup_object
       >>> linear = setup_object(
       ...     {"_target_": "torch.nn.Linear", "in_features": 4, "out_features": 6}
       ... )
       >>> linear
       Linear(in_features=4, out_features=6, bias=True)
       >>> setup_object(linear)  # Do nothing because the module is already instantiated
       Linear(in_features=4, out_features=6, bias=True)
    """
    if isinstance(obj_or_config, dict):
        logger.info(
            "Initializing an object from its configuration... "
            f"{str_target_object(obj_or_config)}"
        )
        obj_or_config = factory(**obj_or_config)
    return obj_or_config


def str_target_object(config: dict) -> str:
    r"""Gets a string that indicates the target object in the config.

    Args:
    ----
        config (dict): Specifies a config compatible with the
            ``objectory`` library. This dict is expected to have a
            key ``'_target_'`` to indicate the target object.

    Returns:
    -------
        str: A string with the target object.

    Example usage:

    .. code-block:: pycon

        >>> from lightcat.utils.factory import str_target_object
        >>> str_target_object({"_target_": "something.MyClass"})
        [_target_: something.MyClass]
        >>> str_target_object({})
        [_target_: N/A]
    """
    return f"[{OBJECT_TARGET}: {config.get(OBJECT_TARGET, 'N/A')}]"
