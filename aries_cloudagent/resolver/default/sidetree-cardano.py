"""Sidetree-Cardano DID Resolver."""

import urllib.parse
import json

from typing import Pattern

import aiohttp

from pydid import DID, DIDDocument, NonconformantDocument

from ...config.injection_context import InjectionContext
from ...core.profile import Profile
from ...messaging.valid import DIDAda

from ..base import (
    BaseDIDResolver,
    DIDNotFound,
    ResolverError,
    ResolverType,
)


class AdaDIDResolver(BaseDIDResolver):
    """ADA DID Resolver."""

    def __init__(self):
        """Initialize ADA DID Resolver."""
        super().__init__(ResolverType.NATIVE)

    async def setup(self, context: InjectionContext):
        """Perform required setup for ADA DID resolution."""

    @property
    def supported_did_regex(self) -> Pattern:
        """Return supported_ada_regex of ADA DID Resolver."""
        return DIDAda.PATTERN


    async def _resolve(self, profile: Profile, did: str) -> dict:
        """Resolve did:ada DIDs."""
        # url = 'https://testnet.sidetree-cardano.com/identifiers/' + did
        url = 'http://localhost:3000/identifiers/' + did
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    try:
                        # TODO BAD TRICK HERE
                        # search all controller="" and change to id -> fix in new version of sidetree
                        # parse @context and remove non string element -> not contemplated on pydid
                        # can subclass DIDDoccumentRoot from pydid
                        sidetree_doc = await response.json()
                        print( sidetree_doc['didDocument'])
                        sidetree_doc['didDocument']['@context'].pop(1)
                        sidetree_doc['didDocument']['verificationMethod'][0]['controller'] = sidetree_doc['didDocument']['id']
                        # Validate DIDDoc with pyDID
                        did_doc = DIDDocument.from_json(json.dumps(sidetree_doc['didDocument']))
                        return did_doc.serialize()
                    except Exception as err:
                        raise ResolverError(
                            "Response was incorrectly formatted"
                        ) from err
                if response.status == 404:
                    raise DIDNotFound(f"No document found for {did}")
                raise ResolverError(
                    "Could not find doc for {}: {}".format(did, await response.text())
                )
        
