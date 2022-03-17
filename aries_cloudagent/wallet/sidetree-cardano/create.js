(async () => {
  const IonSdk = require('@decentralized-identity/ion-sdk');
  const request = require('request');
  const util = require('util');
  const requestPromise = util.promisify(request);

  const nodeURL = 'http://localhost:3000';
  //const nodeURL = 'https://testnet.sidetree-cardano.com/cardano';

  var x_update = process.argv[2];
  var y_update = process.argv[3];
  var docbase64 = process.argv[4];

  // Decode DID Document
  // const didDocument = JSON.parse(Buffer.from(docbase64, 'base64').toString());

  // UpdateKey = RecoveryKey
  updateKey = {
    publicJwk: {
      kty: 'EC', 
      crv: 'secp256k1', 
      x: x_update, 
      y: y_update
    }, 
  }
  const didDocument = {
    publicKeys: [
    {
        id: 'key-1',
        type: 'EcdsaSecp256k1VerificationKey2019',
        publicKeyJwk: {
            kty: 'EC',
            crv: 'secp256k1',
            x: '_5O3aMu92QVDucDWaFiu6xaEnkByG2SYMspeIWCOSUU',
            y: 'SJql7lhWHzoJY7fJvdxpOcCC2JMMnAnugYM9Gskm6q4'
            },
        purposes: ['authentication']
    }
    ],
    services: [
    {
        id: 'domain-1',
        type: 'LinkedDomains',
        serviceEndpoint: 'https://foo.example.com',
    }
    ]
}


  // Create the request body ready to be posted in /operations of Sidetree API
  const createRequest = await IonSdk.IonRequest.createCreateRequest({
    recoveryKey: updateKey.publicJwk,
    updateKey: updateKey.publicJwk,
    document: didDocument
  });

  // POST request body to Sidetree-Cardano node API
  const resp = await requestPromise({
    url: nodeURL + '/operations',
    method: 'POST',
    body: JSON.stringify(createRequest)
  });
  const respBody = JSON.parse(resp.body);
  console.log(respBody.didDocument.id);

})();
