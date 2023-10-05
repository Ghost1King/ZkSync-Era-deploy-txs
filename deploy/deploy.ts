import fs from "fs";
import { utils, Wallet } from "zksync-web3";
import * as ethers from "ethers";
import { HardhatRuntimeEnvironment } from "hardhat/types";
import { Deployer } from "@matterlabs/hardhat-zksync-deploy";

const PRIV_KEY = fs.readFileSync(".secret").toString();

export default async function (hre: HardhatRuntimeEnvironment) {
  console.log(`Running deploy script for your contract`);

  const wallet = new Wallet(PRIV_KEY);

  const deployer = new Deployer(hre, wallet);
  const artifact = await deployer.loadArtifact("EtherDeposit");

  const contract = await deployer.deploy(artifact, []);
  console.log("constructor args:" + contract.interface.encodeDeploy([]));

  const contractAddress = contract.address;
  console.log(`${artifact.contractName} was deployed to ${contractAddress}`);
}