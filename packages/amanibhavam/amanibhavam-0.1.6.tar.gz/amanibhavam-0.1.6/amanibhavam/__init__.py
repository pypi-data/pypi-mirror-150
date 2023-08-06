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


class AwsOrganizationStack(TerraformStack):
    """cdktf Stack for an organization with accounts, sso."""

    def __init__(self, scope: Construct, namespace: str, org: str, domain: str, region: str):
        super().__init__(scope, namespace)

        self.awsProviders(region)

        self.awsOrganization(org, domain)

    def awsProviders(self, region):
        """AWS provider in a region with SSO."""
        sso_region = region

        AwsProvider(self, "aws", region=sso_region)

    def awsOrganization(self, org, domain):
        """Make an Organization with accounts, sso"""
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
