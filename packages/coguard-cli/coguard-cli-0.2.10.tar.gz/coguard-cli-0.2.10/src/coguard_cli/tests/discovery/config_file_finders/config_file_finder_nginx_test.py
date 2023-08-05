"""
Tests for the functions in the ConfigFileFinderNginx class
"""

import unittest
import unittest.mock
from coguard_cli.discovery.config_file_finders.config_file_finder_nginx \
    import ConfigFileFinderNginx

class TestConfigFileFinderNginx(unittest.TestCase):
    """
    The class for testing the ConfigFileFinderNginx module
    """

    def test_get_service_name(self):
        """
        Tests that the correct service name is being returned.
        """
        self.assertEqual(ConfigFileFinderNginx().get_service_name(), "nginx")

    def test_check_for_config_files_in_standard_location_not_existing(self):
        """
        This checks for the standard location test and sees if the file is
        existent or not.
        """
        with unittest.mock.patch(
                "os.path.exists",
                new_callable=lambda: lambda location: False):
            config_file_finder_nginx = ConfigFileFinderNginx()
            self.assertIsNone(config_file_finder_nginx.check_for_config_files_in_standard_location(
                "foo"
            ))

    def test_check_for_config_files_in_standard_location_existing(self):
        """
        This checks for the standard location test and sees if the file is
        existent or not.
        """
        with unittest.mock.patch(
                "os.path.lexists",
                new_callable=lambda: lambda location: True), \
             unittest.mock.patch(
                 ("coguard_cli.discovery.config_file_finders.config_file_"
                  "finder_nginx.ConfigFileFinderNginx._create_temp_"
                  "location_and_manifest_entry"),
                 new_callable=lambda: lambda a, b, c: ({"foo": "bar"}, "/etc/bar")
             ):
            config_file_finder_nginx = ConfigFileFinderNginx()
            result = config_file_finder_nginx.check_for_config_files_in_standard_location(
                "foo"
            )
            self.assertIsNotNone(result)
            self.assertEqual(result[0], {"foo": "bar"})
            self.assertEqual(result[1], "/etc/bar")

    def test_check_for_config_files_filesystem_search_not_existing(self):
        """
        This checks for the standard location test and sees if the file is
        existent or not.
        """
        with unittest.mock.patch(
                "os.walk",
                new_callable=lambda: lambda location: [("etc", [], ["bla.txt"])]):
            config_file_finder_nginx = ConfigFileFinderNginx()
            result = config_file_finder_nginx.check_for_config_files_filesystem_search(
                "foo"
            )
            self.assertListEqual(result, [])

    def test_check_for_config_files_filesystem_search_existing(self):
        """
        This checks for the standard location test and sees if the file is
        existent or not.
        """
        with unittest.mock.patch(
                "os.walk",
                new_callable=lambda: lambda location: [("etc", [], ["nginx.conf"])]), \
                unittest.mock.patch(
                    ("coguard_cli.discovery.config_file_finders.config_file_"
                     "finder_nginx.ConfigFileFinderNginx._create_temp_"
                     "location_and_manifest_entry"),
                    new_callable=lambda: lambda a, b, c: ({"foo": "bar"}, "/etc/bar")
                ):
            config_file_finder_nginx = ConfigFileFinderNginx()
            result = config_file_finder_nginx.check_for_config_files_filesystem_search(
                "foo"
            )
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0][0], {"foo": "bar"})
            self.assertEqual(result[0][1], "/etc/bar")

    def test_create_temp_location_and_manifest_entry(self):
        """
        Testing the creation of temporary locations and manifest entries.
        """
        def new_callable(prefix="/tmp"):
            return "/tmp/foo"
        with unittest.mock.patch(
                'tempfile.mkdtemp',
                new_callable=lambda: new_callable), \
             unittest.mock.patch(
                 'shutil.copy'
             ), \
             unittest.mock.patch(
                 'os.makedirs'
             ), \
             unittest.mock.patch(
                 ("coguard_cli.discovery.config_file_finders."
                  "extract_include_directives")
             ), \
             unittest.mock.patch(
                 'os.path.exists',
                 new_callable=lambda: lambda x: True
             ):
            config_file_finder_nginx = ConfigFileFinderNginx()
            result = config_file_finder_nginx._create_temp_location_and_manifest_entry(
                '/',
                '/nginx.conf'
            )
            self.assertEqual(result[1], "/tmp/foo")
            self.assertEqual(result[0]["serviceName"], "nginx")

    def test_check_call_command_in_container_no_entrypoint_or_cmd(self):
        """
        The function to test the attempted extraction of the nginx.conf
        location from call commands.
        """
        config_file_finder_nginx = ConfigFileFinderNginx()
        result = config_file_finder_nginx.check_call_command_in_container(
            "/",
            {
                "Config": {
                    "WorkingDir": ""
                }
            }
        )
        self.assertListEqual(result, [])

    def test_check_call_command_in_container(self):
        """
        The function to test the attempted extraction of the nginx.conf
        location from call commands.
        """
        with unittest.mock.patch(
                'builtins.open',
                unittest.mock.mock_open(read_data="nginx -c /etc/nginx.conf")), \
             unittest.mock.patch(
                 'os.path.exists',
                 new_callable = lambda: lambda x: True
             ), \
             unittest.mock.patch(
                 ("coguard_cli.discovery.config_file_finders.config_file_"
                  "finder_nginx.ConfigFileFinderNginx._create_temp_"
                  "location_and_manifest_entry"),
                 new_callable=lambda: lambda a, b, c: ({"foo": "bar"}, "/etc/bar")
             ):
            config_file_finder_nginx = ConfigFileFinderNginx()
            result = config_file_finder_nginx.check_call_command_in_container(
                "/",
                {
                    "Config": {
                        "Cmd": [
                            "/bin/sh",
                            "-c",
                            "npm start --prefix $HOME_FOLDER/build"
                        ],
                        "WorkingDir": "",
                        "Entrypoint": [
                            "/docker-entrypoint.sh"
                        ],
                    }
                }
            )
            self.assertEqual(result[0][0]["foo"], "bar")
            self.assertEqual(result[0][1], "/etc/bar")
