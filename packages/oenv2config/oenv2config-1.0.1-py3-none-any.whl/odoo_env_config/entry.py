"""

"""
import os
from typing import Callable, Dict, List, Set, Type

from . import api, mappers
from .section import (
    AddonsPathConfigSection,
    DatabaseOdooConfigSection,
    HttpOdooConfigSection,
    LimitOdooConfigSection,
    LoggerSection,
    MiscSection,
    ServerWideModuleConfigSection,
    TestOdooConfigSection,
    UpdateInstallSection,
    WorkersOdooConfigSection,
)

CONVERTER: Set[Type[api.EnvConverter]] = {
    AddonsPathConfigSection,
    DatabaseOdooConfigSection,
    HttpOdooConfigSection,
    LimitOdooConfigSection,
    LoggerSection,
    MiscSection,
    TestOdooConfigSection,
    UpdateInstallSection,
    ServerWideModuleConfigSection,
    WorkersOdooConfigSection,
}
MAPPER: Set[Callable[[api.Env], api.Env]] = {
    mappers.compatibility,
    mappers.clevercloud_postgresql,
    mappers.redis_session,
    mappers.clevercloud_cellar,
    mappers.queue_job,
}


def apply_mapper(env: api.Env) -> api.Env:
    """
    Apply the MAPPER on `env` and return a new `api.Env` without mutate `env`
    Args:
        env: The env to map

    Returns:
        A new `api.Env` with all MAPPER applied on.
    """
    curr_env = env.copy()
    for mapper in MAPPER:
        curr_env = mapper(curr_env)
    return curr_env


def apply_converter(env: api.Env) -> api.OdooCliFlag:
    """
    Apply the CONVERTER to extract the value of `env` and return all the Odoo args founded
    Args:
        env: The env to convert to OdooCliFlag

    Returns:
        All the args found by the CONVERTER
    """
    store_values = api.OdooCliFlag()
    for converter in CONVERTER:
        store_values.update(converter().init(env).to_values())
    return store_values


def env_to_odoo_args(extra_env: Dict[str, str] = None) -> List[str]:
    """
    Entrypoint of this library
    Convert [os.environ][os.environ] to a odoo args valid.
    See Also
         The env to args [converter][odoo_env_config.option_group]
         The speccific cloud [env mapper][odoo_env_config.env_mapper]
    Examples
         >>> import odoo
         >>> odoo.tools.config.parse_args(env_to_odoo_args())
         >>> odoo.tools.config.save()
    Returns:
         A list with args created from Env
    """
    curr_env = api.Env(os.environ)
    curr_env.update(extra_env or {})
    curr_env = apply_mapper(env=curr_env)
    store_values = apply_converter(curr_env)
    return api.dict_to_odoo_args(store_values)
