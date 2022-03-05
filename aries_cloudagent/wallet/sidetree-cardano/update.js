(async () => {
    const IonSdk = require('@decentralized-identity/ion-sdk');
    const request = require('request');
    const util = require('util');
    const requestPromise = util.promisify(request);
  
    const nodeURL = 'http://localhost:3000';
    //const nodeURL = 'https://testnet.sidetree-cardano.com/cardano';
    var didSuffix = process.argv[2];
    var x = process.argv[3];
    var y = process.argv[4];
    var d = process.argv[5];
    var olddocbase64 = process.argv[6];
    var docbase64 = process.argv[7];
  
    // Decode DID Document
    const olddidDocument = JSON.parse(Buffer.from(olddocbase64, 'base64').toString());
    const didDocument = JSON.parse(Buffer.from(docbase64, 'base64').toString());
  
    // UpdateKey = RecoveryKey
    updateKey = {
      publicJwk: {
        kty: 'EC', 
        crv: 'secp256k1', 
        x: x, 
        y: y
      }, 
      privateJwk: {
        kty: 'EC',
        crv: 'secp256k1',
        d: d,
        x: x, 
        y: y
      }
    }

    // TODO  create update operations based on old and new document
    const updateOperation = {
        idsOfPublicKeysToRemove: ['key-1'],
        publicKeysToAdd: [
          {
            id: 'key-2',
            type: 'EcdsaSecp256k1VerificationKey2019',
            publicKeyJwk: newAuthnKeys.publicJwk,
            purposes: ['authentication']
          }
        ],
        idsOfServicesToRemove: ['domain-1'],
        servicesToAdd: [{
          id: 'some-service-2',
          type: 'SomeServiceType',
          serviceEndpoint: 'http://www.example.com'
        }]
      };
  
  
    // Create the request body ready to be posted in /operations of Sidetree API


    const updateRequest = await IonSdk.IonRequest.createUpdateRequest({
        didSuffix: didSuffix,
        updatePublicKey: updateKey.publicJwk,
        nextUpdatePublicKey: updateKey.publicJwk, // it's recommended to change that key on each update
        signer: IonSdk.LocalSigner.create(updateKey.privateJwk),
        idsOfServicesToRemove: updateOperation.idsOfServicesToRemove,
        servicesToAdd: updateOperation.servicesToAdd,
        idsOfPublicKeysToRemove: updateOperation.idsOfPublicKeysToRemove,
        publicKeysToAdd: updateOperation.publicKeysToAdd
      });

  
    // POST request body to Sidetree-Cardano node API
    const resp = await requestPromise({
      url: nodeURL + '/operations',
      method: 'POST',
      body: JSON.stringify(updateRequest)
    });
    const respBody = JSON.parse(resp.body);
    console.log(respBody.didDocument.id);
  
  })();
  