""" Organization for katt@defn.sh """

import fogg.aws
from cdktf import App, TerraformStack
from constructs import Construct
from imports.aws import AwsProvider  # type: ignore


class KattStack(TerraformStack):
    """cdktf Stack for an organization with accounts, sso."""

    def __init__(self, scope: Construct, namespace: str):
        super().__init__(scope, namespace)

        self.providers()

        self.organization()

    def providers(self):
        """AWS provider in a region with SSO."""
        sso_region = "us-west-2"

        AwsProvider(self, "aws", region=sso_region)

    def organization(self):
        """Make an Organization with accounts, sso"""
        org = "katt"
        domain = "defn.sh"
        accounts = [
            "org",
            "net",
            "log",
            "lib",
            "ops",
            "sec",
            "hub",
            "pub",
            "dev",
            "dmz",
        ]

        fogg.aws.organization(self, org, domain, accounts)

def main():
    app = App()
    KattStack(app, "default")

    app.synth()
