(async () => {
  const IonSdk = require('@decentralized-identity/ion-sdk');
  const randomBytes = require('randombytes');
  const ed25519 = require('@transmute/did-key-ed25519');
  const secp256k1 = require('@transmute/did-key-secp256k1');
  const request = require('request');
  const util = require('util');
  const requestPromise = util.promisify(request);

  const nodeURL = 'http://localhost:3000';
  //const nodeURL = 'https://testnet.sidetree-cardano.com/cardano';

  var x_update = process.argv.slice(2,3)[0];
  var y_update = process.argv.slice(3,4)[0];


  // Generate update and recovery keys for sidetree protocol
  // Should be stored somewhere, you'll need later for updates and recovery of your DID
  // const updateKey = await generateKeyPair('secp256k1'); // also supports Ed25519
  // console.log('Your update key:');
  // console.log(updateKey);
  // const recoveryKey = await generateKeyPair('secp256k1'); // also supports Ed25519
  // console.log('Your recovery key:');
  // console.log(recoveryKey);

  // Generate authentication key for the W3C DID Document
  // Should be stored somewhere, you'll need it later for your proofs
  const authnKeys = await generateKeyPair('secp256k1'); // also supports Ed25519
  // console.log('Your DID authentication key:');
  // console.log(authnKeys);

  // Create you rW3C DID document
  const didDocument = {
    publicKeys: [
      {
        id: 'key-1',
        type: 'EcdsaSecp256k1VerificationKey2019',
        publicKeyJwk: authnKeys.publicJwk,
        purposes: ['authentication']
      }
    ],
    services: [
      {
        id: 'domain-1',
        type: 'LinkedDomains',
        serviceEndpoint: 'https://foo.example.com'
      }
    ]
  };

  updateKey = {
    publicJwk: {
      kty: 'EC', 
      crv: 'secp256k1', 
      x: x_update, 
      y: y_update
    }, 
  }


  // Create the request body ready to be posted in /operations of Sidetree API
  const createRequest = await IonSdk.IonRequest.createCreateRequest({
    recoveryKey: updateKey.publicJwk,
    updateKey: updateKey.publicJwk,
    document: didDocument
  });
  //console.log('POST operation: ' + JSON.stringify(createRequest));

  // POST request body to Sidetree-Cardano node API
  const resp = await requestPromise({
    url: nodeURL + '/operations',
    method: 'POST',
    body: JSON.stringify(createRequest)
  });
  const respBody = JSON.parse(resp.body);
  //console.log(JSON.stringify(respBody));
  console.log(respBody.didDocument.id);

  // Helper function to generate keys
  // You can use your prefered key generator
  // type: secp256k1 | Ed25519
  async function generateKeyPair (type) {
    let keyGenerator = secp256k1.Secp256k1KeyPair;
    if (type === 'Ed25519') { keyGenerator = ed25519.Ed25519KeyPair; };
    const keyPair = await keyGenerator.generate({
      secureRandom: () => randomBytes(32)
    });
    const { publicKeyJwk, privateKeyJwk } = await keyPair.export({type:'JsonWebKey2020'});

    return {
      publicJwk: publicKeyJwk,
      privateJwk: privateKeyJwk
    };
  }

})();
