# -*- coding: utf8 -*-
import unittest

from odoo_env_config import entry


class TestOdooConfig(unittest.TestCase):
    def test_no_config(self):
        config = entry.env_to_odoo_args()
        self.assertFalse(config)

    def test_args_database(self):
        db_host = "my-host.com"
        db_name = "my-db"
        db_port = str(5253)
        db_user = "my-user"
        db_password = "py-password"
        extra_env = {
            "POSTGRESQL_ADDON_DB": db_name,
            "POSTGRESQL_ADDON_HOST": db_host,
            "POSTGRESQL_ADDON_PORT": db_port,
            "POSTGRESQL_ADDON_USER": db_user,
            "POSTGRESQL_ADDON_PASSWORD": db_password,
        }
        args = entry.env_to_odoo_args(extra_env)
        self.assertSetEqual(
            {
                "--db_host=" + db_host,
                "--db_port=" + db_port,
                "--db_user=" + db_user,
                "--db_password=" + db_password,
                "--database=" + db_name,
            },
            set(args),
        )

    def test_args_direct_database(self):
        """
        Assert Mapper for direct acces postgres provide by clevercloud
        """
        db_host = "my-host.com"
        db_name = "my-db"
        db_port = str(5253)
        db_user = "my-user"
        db_password = "py-password"
        extra_env = {
            "POSTGRESQL_ADDON_DB": db_name,
            "POSTGRESQL_ADDON_DIRECT_HOST": db_host,
            "POSTGRESQL_ADDON_DIRECT_PORT": db_port,
            "POSTGRESQL_ADDON_USER": db_user,
            "POSTGRESQL_ADDON_PASSWORD": db_password,
        }
        args = entry.env_to_odoo_args(extra_env)
        self.assertSetEqual(
            {
                "--db_host=" + db_host,
                "--db_port=" + db_port,
                "--db_user=" + db_user,
                "--db_password=" + db_password,
                "--database=" + db_name,
            },
            set(args),
        )
