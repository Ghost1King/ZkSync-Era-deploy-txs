import "@matterlabs/hardhat-zksync-deploy";
import "@matterlabs/hardhat-zksync-solc";
import "@matterlabs/hardhat-zksync-verify";

module.exports = {
  zksolc: {
    version: "1.3.13",
    compilerSource: "binary",
    settings: {},
    moduleResolution: "NodeNext",
  },
  defaultNetwork: "zkSyncMainnet",

  networks: {
    zkSyncMainnet: {
      url: "https://zksync.meowrpc.com",
      ethNetwork: "mainnet",
      zksync: true,
    },
  },
  solidity: {
    version: "0.8.17",
  },
};