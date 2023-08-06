from eulith_web3.erc20 import TokenSymbol
from eulith_web3.eulith_web3 import EulithWeb3
from eulith_web3.signing import construct_signing_middleware, LocalSigner
from eulith_web3.trezor import TrezorSigner

EULITH_REFRESH_TOKEN='eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJzdWIiOiJsaWJ0ZXN0IiwiZXhwIjoxODQ0Njc0NDA3MzcwOTU1MTYxNSwic291cmNlX2hhc2giOiIqIiwic2NvcGUiOiJBUElSZWZyZXNoIn0.G87Tv9LwLH8SRgjlVKIAPk1pdavVS0xwz3fuB7lxP0Et-pPM7ojQkjC1zlC7zWYUdh9p3GvwX_ROfgSPJsw-Qhw'

if __name__ == '__main__':
    ts = TrezorSigner()
    faucet = LocalSigner('4d5db4107d237df6a3d58ee5f70ae63d73d7658d4026f2eefd2f204c81682cb7')

    ew3 = EulithWeb3("http://localhost:7777/v0", EULITH_REFRESH_TOKEN, construct_signing_middleware(ts))
    ew3.default_confirmations = 0

    faucet_ew3 = EulithWeb3("http://localhost:7777/v0", EULITH_REFRESH_TOKEN, construct_signing_middleware(faucet))

    send_eth_tx = {
        'from': faucet.address,
        'to': ts.address,
        'value': 2000000000000000000,
    }

    # r = faucet_ew3.eth.send_transaction(send_eth_tx)
    # print(r.hex())

    ew3.v0.submit_enable_module_signature(faucet.address, ts)

