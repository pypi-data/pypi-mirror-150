""" Organization for katt@defn.sh """

import json
import os
from email import contentmanager

context = {
    "excludeStackIdFromLogicalIds": True,
    "allowSepCharsInLogicalIds": True
}
os.environ.setdefault("CDKTF_CONTEXT_JSON", json.dumps(context))

from cdktf import App, TerraformStack
from cdktf_cdktf_provider_aws import AwsProvider  # type: ignore
from constructs import Construct

import amanibhavam.fogg


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
            "dmz"
        ]

        amanibhavam.fogg.organization(self, org, domain, accounts)

def main():
    app = App()
    KattStack(app, "default")

    app.synth()
