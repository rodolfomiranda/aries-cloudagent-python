(async () => {
    const IonSdk = require('@decentralized-identity/ion-sdk');
    const request = require('request');
    const util = require('util');
    const requestPromise = util.promisify(request);
  
    const nodeURL = 'http://localhost:3000';
    //const nodeURL = 'https://testnet.sidetree-cardano.com/cardano';
    var didSuffix = process.argv[2];
    var x_old = process.argv[3];
    var y_old = process.argv[4];
    var d_old = process.argv[5];
    var x_new = process.argv[6];
    var y_new = process.argv[7];
    var docbase64 = process.argv[8];
  
    // Decode DID Document
    const didDocument = JSON.parse(Buffer.from(docbase64, 'base64').toString());
  
    // UpdateKey = RecoveryKey
    updateKeyOld = {
      publicJwk: {
        kty: 'EC', 
        crv: 'secp256k1', 
        x: x_old, 
        y: y_old
      }, 
      privateJwk: {
        kty: 'EC',
        crv: 'secp256k1',
        d: d_old,
        x: x_old, 
        y: y_old
      }
    }

    updateKeyNew = {
        publicJwk: {
          kty: 'EC', 
          crv: 'secp256k1', 
          x: x_new, 
          y: y_new
        }, 
        privateJwk: {
          kty: 'EC',
          crv: 'secp256k1',
          d: d_new,
          x: x_new, 
          y: y_new
        }
      }
  
  
    // Create the request body ready to be posted in /operations of Sidetree API

    const recoveryRequest = await IonSdk.IonRequest.createRecoverRequest({
        didSuffix: didSuffix,
        signer: IonSdk.LocalSigner.create(updateKeyOld.privateJwk),
        recoveryPublicKey: updateKeyOld.publicJwk,
        nextRecoveryPublicKey: updateKeyNew.publicJwk,
        nextUpdatePublicKey: updateKeyNew.publicJwk,
        document: didDocument
      });
  
    // POST request body to Sidetree-Cardano node API
    const resp = await requestPromise({
      url: nodeURL + '/operations',
      method: 'POST',
      body: JSON.stringify(recoveryRequest)
    });
    const respBody = JSON.parse(resp.body);
    console.log(respBody.didDocument.id);
  
  })();
  