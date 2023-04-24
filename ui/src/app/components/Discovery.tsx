import { useState } from "react";
import {
  useAccount,
  useWaitForTransaction,
  useTransactionManager,
  useTransactions,
  useTransaction,
} from "@starknet-react/core";
import { useQuery } from "@apollo/client";
import {
  getDiscoveryByTxHash,
  getLatestDiscoveries,
} from "../hooks/graphql/queries";
import KeyboardControl, { ButtonData } from "./KeyboardControls";
import { NullDiscovery } from "../types";
import { NullAdventurer } from "../types";
import { useAdventurer } from "../context/AdventurerProvider";
import { TxActivity } from "./TxActivity";
import { DiscoveryDisplay } from "./DiscoveryDisplay";

interface DiscoveryProps {
  hash: any;
}

const Discovery = ({ hash }: DiscoveryProps) => {
  const { hashes } = useTransactionManager();

  const currentHash = hashes[hashes.length - 1];
  const currentTransaction = useTransaction({ hash: currentHash });

  const { adventurer, handleUpdateAdventurer } = useAdventurer();
  const { data, status, isLoading, error } = useWaitForTransaction({
    hash: currentHash,
    watch: true,
  });
  const formatAdventurer = adventurer ? adventurer.adventurer : NullAdventurer;

  const { data: latestDiscoveriesData, error: latestDiscoveriesError } =
    useQuery(getLatestDiscoveries, {
      variables: {
        adventurerId: formatAdventurer?.id,
      },
      pollInterval: 5000,
    });

  const latestDiscoveries = latestDiscoveriesData
    ? latestDiscoveriesData.discoveries
    : [];

  return (
    <div className="flex flex-col gap-5 m-auto">
      {(hash && data?.status != "ACCEPTED_ON_L2") ||
      (hash && data?.status != "ACCEPTED_ON_L1") ? (
        <TxActivity hash={hash} />
      ) : latestDiscoveries.length > 0 ? (
        <>
          <p className="text-xl">Recent discoveries:</p>
          <div className="flex flex-col gap-2 items-center">
            {latestDiscoveries.map((discovery: any, index: number) => (
              <div key={index}>
                <DiscoveryDisplay discoveryData={discovery} />
              </div>
            ))}
          </div>
        </>
      ) : (
        <p>You have not yet made any discoveries!</p>
      )}
    </div>
  );
};

export default Discovery;