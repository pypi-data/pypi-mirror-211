from typing import List

from typing_extensions import Self

from .. import api


class MiscSection(api.EnvConverter):
    def __init__(self):
        super().__init__()
        self.unaccent = False
        self.without_demo: List[str] = []
        self.stop_after_init = False
        self.save_config_file = False

    def init(self, curr_env: api.Env) -> Self:
        self.unaccent = curr_env.get_bool("UNACCENT", default=False)
        self.without_demo = curr_env.get_list("WITHOUT_DEMO")
        self.stop_after_init = curr_env.get_bool("STOP_AFTER_INIT")
        self.save_config_file = curr_env.get_bool("SAVE_CONFIG_FILE")
        return self

    def to_values(self) -> api.OdooCliFlag:
        flags = super().to_values()
        flags.set("unaccent", self.unaccent)
        flags.set("without-demo", ",".join(self.without_demo))
        flags.set("save", self.save_config_file)
        flags.set("stop-after-init", self.stop_after_init)
        return flags
