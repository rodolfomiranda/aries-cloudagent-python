"""EcdsaSecp256k1VerificationKey2019 suite."""

from datetime import datetime
from typing import Union

from ..crypto import _KeyPair as KeyPair

from .jws_linked_data_signature import JwsLinkedDataSignature


class EcdsaSecp256k1VerificationKey2019(JwsLinkedDataSignature):
    """EcdsaSecp256k1VerificationKey2019 suite."""

    signature_type = "EcdsaSecp256k1VerificationKey2019"

    def __init__(
        self,
        *,
        key_pair: KeyPair,
        proof: dict = None,
        verification_method: str = None,
        date: Union[datetime, str] = None,
    ):
        """Create new EcdsaSecp256k1VerificationKey2019 instance.

        Args:
            key_pair (KeyPair): Key pair to use. Must provide EdDSA signatures
            proof (dict, optional): A JSON-LD document with options to use for the
                `proof` node (e.g. any other custom fields can be provided here
                using a context different from security-v2).
            verification_method (str, optional): A key id URL to the paired public key.
            date (datetime, optional): Signing date to use.
        """
        super().__init__(
            signature_type=EcdsaSecp256k1VerificationKey2019.signature_type,
            algorithm="EcDSA",
            required_key_type="EcdsaSecp256k1VerificationKey2019",
            key_pair=key_pair,
            verification_method=verification_method,
            proof=proof,
            date=date,
        )
