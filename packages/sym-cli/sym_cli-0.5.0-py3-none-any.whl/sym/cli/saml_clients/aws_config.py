import os
from configparser import ConfigParser
from functools import cached_property
from pathlib import Path
from typing import Iterator, Tuple

from boto3 import setup_default_session
from sym.shared.cli.helpers.contexts import push_env
from sym.shared.cli.helpers.keywords_to_options import Argument

from sym.cli.helpers.boto import get_identity

from ..decorators import command_require_bins, intercept_errors, run_subprocess
from ..errors import InvalidResource
from ..helpers.params import Profile
from .saml_client import SAMLClient

# The docs say that the credentials file is for sensitive values like actual access keys etc
# and the config file for less sensitive things like role names, SSO configs.
AwsConfigPath = Path(os.getenv("AWS_CONFIG_FILE", Path.home() / ".aws" / "config"))


class AwsConfig(SAMLClient):
    binary = "aws"
    option_value = "aws-config"
    priority = 0
    setup_help = f"Set up your profile in `{str(AwsConfigPath)}`."

    resource: str
    options: "GlobalOptions"

    def __init__(self, resource: str, *, options: "GlobalOptions") -> None:
        super().__init__(resource, options=options)
        # Make the default session use our AWS profile so we don't need to manage sessions in
        # whatever other call chains there are to get AWS creds
        setup_default_session(profile_name=resource)

    @classmethod
    def _read_creds_config(cls):
        config = ConfigParser(strict=False)
        if AwsConfigPath.exists():
            config.read(AwsConfigPath)
        return config

    @classmethod
    def validate_resource(cls, resource: str):
        config = cls._read_creds_config()
        return config.has_section(cls._profile_name(resource))

    @cached_property
    def _section(self):
        config = self.__class__._read_creds_config()
        return config[self.__class__._profile_name(self.resource)]

    @classmethod
    def _profile_name(cls, resource: str):
        return f"profile {resource}"

    def raise_if_invalid(self):
        if self.__class__.validate_resource(self.resource):
            return
        raise InvalidResource(
            self.resource, self.__class__._read_creds_config().sections()
        )

    # Returning an empty dict here because we set up a default boto session above, so no need
    # for creds here
    def get_creds(self):
        return {}

    @intercept_errors()
    @run_subprocess
    @command_require_bins(binary)
    def _exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
        with push_env("AWS_PROFILE", self.resource):
            yield (*args, opts)

    def is_setup(self) -> bool:
        return AwsConfigPath.exists()

    def _ensure_config(self, profile: Profile) -> ConfigParser:
        return ConfigParser(strict=False)

    def _ensure_session(self, *, force: bool):
        if not force and not self._creds_expiring():
            return
        get_identity(self)

    def get_profile(self):
        return Profile(
            display_name=self.resource,
            region=self._section.get("region"),
            arn=self._section.get("x_principal_arn"),
            ansible_bucket=self._section.get("x_sym_ansible_bucket"),
        )

    def send_analytics_event(self):
        pass
