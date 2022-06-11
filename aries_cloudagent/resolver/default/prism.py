"""PRISM DID Resolver."""

import subprocess

from typing import Pattern

from pydid import DID, DIDDocument, NonconformantDocument

from ...config.injection_context import InjectionContext
from ...core.profile import Profile
from ...messaging.valid import DIDPrism

from ..base import (
    BaseDIDResolver,
    DIDNotFound,
    ResolverError,
    ResolverType,
)
from aries_cloudagent.admin.server import LOGGER
from ...wallet.util import  bytes_to_b58


class PrismDIDResolver(BaseDIDResolver):
    """PRISM DID Resolver."""

    def __init__(self):
        """Initialize PRISM DID Resolver."""
        super().__init__(ResolverType.NATIVE)

    async def setup(self, context: InjectionContext):
        """Perform required setup for ADA DID resolution."""

    @property
    def supported_did_regex(self) -> Pattern:
        """Return supported_ada_regex of PRISM DID Resolver."""
        return DIDPrism.PATTERN


    async def _resolve(self, profile: Profile, did: str) -> dict:
        """Resolve did:prism DIDs."""
        #  Validate DIDDoc with pyDID
        didget = subprocess.check_output(["java", "-jar" ,"./aries_cloudagent/wallet/prism/wal-cli-1.0.1-SNAPSHOT-all.jar", "resolve-prism-did", did, "-w3c"]).decode('utf-8')[:-1]
        if didget.split("\n",2)[1] == "DID document":
            try:
                did_doc = DIDDocument.from_json(didget.split("\n",2)[2])
                return did_doc.serialize()
            except Exception as err:
                raise ResolverError(
                    "Response was incorrectly formatted"
                ) from err
        else:
            raise DIDNotFound(f"No document found for {did}")
        raise ResolverError(
            "Could not find doc for {}: {}".format(did, await response.text())
        )


        
