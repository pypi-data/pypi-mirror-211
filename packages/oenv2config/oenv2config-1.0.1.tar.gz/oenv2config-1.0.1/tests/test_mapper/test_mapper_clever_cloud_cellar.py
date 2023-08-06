import unittest

from odoo_env_config import api
from odoo_env_config.mappers import clevercloud_cellar
from tests._decorators import MultiOdooVersion


class TestCleverCloudMapperCellar(unittest.TestCase):
    def _test_priority(self, key, to_map, expected):
        result = clevercloud_cellar(api.Env(to_map))
        self.assertEqual(6, len(result.keys()))
        self.assertEqual(
            expected, result[key], "Value of key [%s] is not expected '%s' result : '%s'" % (key, expected, result[key])
        )
        for key_result, value in result.items():
            if key_result == "S3_FILESTORE_REGION" and key != key_result:
                self.assertEqual("fr-par", value)
                continue

    @MultiOdooVersion.with_args
    def test_map_cellar(self, version):
        host = "my-host.com"
        secret_key = "SECRET_KEY"
        key_id = "KEY_ID"
        region = "fr-par"
        result = clevercloud_cellar(
            api.Env(
                {
                    "ODOO_VERSION": str(version),
                    "CELLAR_ADDON_HOST": host,
                    "CELLAR_ADDON_KEY_SECRET": secret_key,
                    "CELLAR_ADDON_KEY_ID": key_id,
                    "CELLAR_ADDON_REGION": region,
                }
            )
        )
        self.assertEqual(9, len(result.keys()))

    @MultiOdooVersion.with_args
    def test_host(self, version):
        """
        Host definition argument are mapped to S3_... corresponding parameters
        """
        host = "my-host.com"
        secret_key = "SECRET_KEY"
        key_id = "KEY_ID"
        region = "fr-par"
        result = clevercloud_cellar(
            api.Env(
                {
                    "ODOO_VERSION": str(version),
                    "CELLAR_ADDON_HOST": host,
                    "CELLAR_ADDON_KEY_SECRET": secret_key,
                    "CELLAR_ADDON_KEY_ID": key_id,
                    "CELLAR_ADDON_REGION": region,
                }
            )
        )
        self.assertEqual(9, len(result.keys()), "mapper has added 4 parameters S3_FILESTORE_HOST, S3_...")
        self.assertEqual(host, result["S3_FILESTORE_HOST"])
        self.assertEqual(secret_key, result["S3_FILESTORE_SECRET_KEY"])
        self.assertEqual(key_id, result["S3_FILESTORE_ACCESS_KEY"])
        self.assertEqual(region, result["S3_FILESTORE_REGION"])

    @MultiOdooVersion.with_args
    def test_priority(self, version):
        """
        Test que les variables mapper sont prioritaires si elles existent
        """

        host = "my-host.com"
        secret_key = "SECRET_KEY"
        key_id = "KEY_ID"
        region = "fr-par"
        origin = "_origin"
        result = clevercloud_cellar(
            api.Env(
                {
                    "ODOO_VERSION": str(version),
                    "CELLAR_ADDON_HOST": host,
                    "S3_FILESTORE_HOST": host + origin,
                    "S3_FILESTORE_SECRET_KEY": secret_key + origin,
                    "CELLAR_ADDON_KEY_SECRET": secret_key,
                    "S3_FILESTORE_ACCESS_KEY": key_id + origin,
                    "CELLAR_ADDON_KEY_ID": key_id,
                    "S3_FILESTORE_REGION": region + origin,
                    "CELLAR_ADDON_REGION": region,
                }
            )
        )
        self.assertEqual(9, len(result.keys()))
        self.assertEqual(host + origin, result["S3_FILESTORE_HOST"])
        self.assertEqual(secret_key + origin, result["S3_FILESTORE_SECRET_KEY"])
        self.assertEqual(key_id + origin, result["S3_FILESTORE_ACCESS_KEY"])
        self.assertEqual(region + origin, result["S3_FILESTORE_REGION"])

    @MultiOdooVersion.with_args
    def test_default_region(self, version):
        host = "my-host.com"
        secret_key = "SECRET_KEY"
        key_id = "KEY_ID"
        result = clevercloud_cellar(
            api.Env(
                {
                    "ODOO_VERSION": str(version),
                    "CELLAR_ADDON_HOST": host,
                    "CELLAR_ADDON_KEY_SECRET": secret_key,
                    "CELLAR_ADDON_KEY_ID": key_id,
                }
            )
        )
        self.assertEqual(8, len(result.keys()), "mapper has set S3_FILESTORE_ENABLE and generated 4 S3_xx parameter")
        self.assertEqual(host, result["S3_FILESTORE_HOST"])
        self.assertEqual(secret_key, result["S3_FILESTORE_SECRET_KEY"])
        self.assertEqual(key_id, result["S3_FILESTORE_ACCESS_KEY"])
        self.assertEqual("fr-par", result["S3_FILESTORE_REGION"], "internal default value has been used by mapper")

    @MultiOdooVersion.with_args
    def test_priority_s3_host(self, version):
        """
        Test the priority of the key
        S3_FILESTORE_HOST > CELLAR_ADDON_HOST
        """
        value1 = "value1"
        value2 = "value2"
        self._test_priority(
            key="S3_FILESTORE_HOST",
            to_map={
                "ODOO_VERSION": str(version),
                "S3_FILESTORE_HOST": value1,
                "CELLAR_ADDON_HOST": value2,
            },
            expected=value1,
        )
        self._test_priority(
            key="S3_FILESTORE_HOST",
            to_map={
                "ODOO_VERSION": str(version),
                # "S3_FILESTORE_HOST": value1,
                "CELLAR_ADDON_HOST": value2,
            },
            expected=value2,
        )

    @MultiOdooVersion.with_args
    def test_priority_s3_secret_key(self, version):
        """
        Test the priority of the key
        S3_FILESTORE_SECRET_KEY > CELLAR_ADDON_KEY_SECRET
        """
        value1 = "value1"
        value2 = "value2"
        self._test_priority(
            key="S3_FILESTORE_SECRET_KEY",
            to_map={
                "ODOO_VERSION": str(version),
                "S3_FILESTORE_SECRET_KEY": value1,
                "CELLAR_ADDON_KEY_SECRET": value2,
            },
            expected=value1,
        )
        self._test_priority(
            key="S3_FILESTORE_SECRET_KEY",
            to_map={
                "ODOO_VERSION": str(version),
                "CELLAR_ADDON_KEY_SECRET": value2,
            },
            expected=value2,
        )

    @MultiOdooVersion.with_args
    def test_priority_s3_acces_key(self, version):
        """
        Test the priority of the key
        S3_FILESTORE_ACCESS_KEY > CELLAR_ADDON_KEY_ID
        """
        value1 = "value1"
        value2 = "value2"
        self._test_priority(
            key="S3_FILESTORE_ACCESS_KEY",
            to_map={
                "ODOO_VERSION": str(version),
                "S3_FILESTORE_ACCESS_KEY": value1,
                "CELLAR_ADDON_KEY_ID": value2,
            },
            expected=value1,
        )
        self._test_priority(
            key="S3_FILESTORE_ACCESS_KEY",
            to_map={
                "ODOO_VERSION": str(version),
                "CELLAR_ADDON_KEY_ID": value2,
            },
            expected=value2,
        )

    @MultiOdooVersion.with_args
    def test_priority_s3_region(self, version):
        """
        Test the priority of the key
        S3_FILESTORE_REGION > CELLAR_ADDON_REGION
        """
        value1 = "value1"
        value2 = "value2"
        self._test_priority(
            key="S3_FILESTORE_REGION",
            to_map={
                "ODOO_VERSION": str(version),
                "S3_FILESTORE_REGION": value1,
                "CELLAR_ADDON_REGION": value2,
            },
            expected=value1,
        )
        self._test_priority(
            key="S3_FILESTORE_REGION",
            to_map={
                "ODOO_VERSION": str(version),
                "CELLAR_ADDON_REGION": value2,
            },
            expected=value2,
        )
