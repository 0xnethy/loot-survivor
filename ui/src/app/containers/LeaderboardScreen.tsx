import React, { useState } from "react";
import {
  getAdventurersInListByXp,
  getTopScores,
} from "../hooks/graphql/queries";
import { Button } from "../components/buttons/Button";
import { CoinIcon } from "../components/icons/Icons";
import Lords from "../../../public/lords.svg";
import LootIconLoader from "../components/icons/Loader";
import { useQueriesStore } from "../hooks/useQueryStore";
import useUIStore from "../hooks/useUIStore";
import useCustomQuery from "../hooks/useCustomQuery";
import { Score, Adventurer } from "../types";
import { useUiSounds, soundSelector } from "../hooks/useUiSound";
import KillAdventurer from "../components/actions/KillAdventurer";
import { useMediaQuery } from "react-responsive";

/**
 * @container
 * @description Provides the leaderboard screen for the adventurer.
 */
export default function LeaderboardScree() {
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [showKill, setShowKill] = useState(false);
  const itemsPerPage = 10;
  const [loading, setLoading] = useState(false);
  const { play: clickPlay } = useUiSounds(soundSelector.click);

  const setScreen = useUIStore((state) => state.setScreen);
  const setProfile = useUIStore((state) => state.setProfile);

  const handleRowSelected = async (adventurerId: number) => {
    setLoading(true);
    try {
      setProfile(adventurerId);
      setScreen("profile");
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const { data, isLoading, refetch } = useQueriesStore();

  useCustomQuery(
    "adventurersInListByXpQuery",
    getAdventurersInListByXp,
    {
      ids: data.topScoresQuery?.scores
        ? data.topScoresQuery?.scores.map((score: Score) => score.adventurerId)
        : [0],
    },
    false
  );

  const scores = data.adventurersInListByXpQuery?.adventurers
    ? data.adventurersInListByXpQuery?.adventurers
    : [];

  useCustomQuery("topScoresQuery", getTopScores, undefined, false);

  const isMobileDevice = useMediaQuery({
    query: "(max-device-width: 480px)",
  });

  if (isLoading.adventurersByXPQuery || loading)
    return (
      <div className="flex justify-center p-20 align-middle">
        <LootIconLoader />
      </div>
    );

  const adventurers = data.adventurersByXPQuery?.adventurers
    ? data.adventurersByXPQuery?.adventurers
    : [];

  const totalPages = Math.ceil(adventurers.length / itemsPerPage);

  const handleClick = (newPage: number): void => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  const displayAdventurers = adventurers?.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  let previousGold = -1;
  let currentRank = 0;
  let rankOffset = 0;

  const rankGold = (adventurer: Adventurer, index: number) => {
    if (adventurer.xp !== previousGold) {
      currentRank = index + 1 + (currentPage - 1) * itemsPerPage;
      rankOffset = 0;
    } else {
      rankOffset++;
    }
    previousGold = adventurer.xp ?? 0;
    return currentRank;
  };

  return (
    <div className="flex flex-col items-cente justify-between sm:w-3/4 sm:mx-auto">
      <div className="flex flex-col items-center py-2">
        <h1 className="text-lg sm:text-2xl m-0">Top 3 Submitted Scores</h1>
        {scores.length > 0 ? (
          <table className="w-full mt-4 text-sm sm:text-xl border border-terminal-green">
            <thead className="border border-terminal-green">
              <tr>
                <th className="p-1">Rank</th>
                <th className="p-1">Adventurer</th>
                <th className="p-1">XP</th>
                <th className="p-1">
                  Prize <span className="text-sm">(per mint)</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {scores.map((adventurer: Adventurer, index: number) => {
                if (index > 2) {
                  return null;
                } else {
                  return (
                    <tr
                      key={index}
                      className="text-center border-b border-terminal-green hover:bg-terminal-green hover:text-terminal-black cursor-pointer"
                      onClick={() => {
                        handleRowSelected(adventurer.id ?? 0);
                        clickPlay();
                      }}
                    >
                      <td>{index + 1}</td>
                      <td>{`${adventurer.name} - ${adventurer.id}`}</td>
                      <td>{adventurer.xp}</td>
                      <td>
                        <div className="flex flex-row items-center justify-center gap-2">
                          <span
                            className={` ${
                              index == 0
                                ? "text-gold"
                                : index == 1
                                ? "text-silver"
                                : index == 2
                                ? "text-bronze"
                                : ""
                            }`}
                          >
                            {index == 0
                              ? 10
                              : index == 1
                              ? 3
                              : index == 2
                              ? 2
                              : ""}
                          </span>

                          <Lords className="self-center w-6 h-6 ml-4 fill-current" />
                        </div>
                      </td>
                    </tr>
                  );
                }
              })}
            </tbody>
          </table>
        ) : (
          <h3 className="text-lg sm:text-2xl py-4">
            No scores submitted yet. Be the first!
          </h3>
        )}
      </div>
      <div className="flex flex-col gap-5 sm:gap-0 sm:flex-row justify-between w-full">
        {!showKill && (
          <div className="flex flex-col w-full sm:mb-4 sm:mb-0 sm:mr-4 flex-grow-2 sm:border sm:border-terminal-green p-2">
            <h4 className="text-center text-lg sm:text-2xl m-0">
              Live Leaderboard
            </h4>
            <table className="w-full text-sm sm:text-xl border border-terminal-green">
              <thead className="border border-terminal-green">
                <tr>
                  <th className="p-1">Rank</th>
                  <th className="p-1">Adventurer</th>
                  <th className="p-1">Gold</th>
                  <th className="p-1">XP</th>
                  <th className="p-1">Health</th>
                </tr>
              </thead>
              <tbody>
                {displayAdventurers?.map(
                  (adventurer: Adventurer, index: number) => {
                    const dead = (adventurer.health ?? 0) <= 0;
                    return (
                      <tr
                        key={index}
                        className="text-center border-b border-terminal-green hover:bg-terminal-green hover:text-terminal-black cursor-pointer"
                        onClick={() => {
                          handleRowSelected(adventurer.id ?? 0);
                          clickPlay();
                        }}
                      >
                        <td>{rankGold(adventurer, index)}</td>
                        <td>{`${adventurer.name} - ${adventurer.id}`}</td>
                        <td>
                          <span className="flex justify-center text-terminal-yellow">
                            <CoinIcon className="self-center w-4 h-4 sm:w-6 sm:h-6 fill-current" />
                            {adventurer.gold ? adventurer.gold : 0}
                          </span>
                        </td>
                        <td>
                          <span className="flex justify-center">
                            {adventurer.xp}
                          </span>
                        </td>
                        <td>
                          <span
                            className={`flex justify-center ${
                              !dead ? " text-terminal-green" : "text-red-800"
                            }`}
                          >
                            {adventurer.health}
                          </span>
                        </td>
                      </tr>
                    );
                  }
                )}
              </tbody>
            </table>
            {adventurers?.length > 10 && (
              <div className="flex justify-center sm:mt-8">
                <Button
                  variant={"outline"}
                  onClick={() =>
                    currentPage > 1 && handleClick(currentPage - 1)
                  }
                  disabled={currentPage === 1}
                >
                  back
                </Button>

                <Button
                  variant={"outline"}
                  key={1}
                  onClick={() => handleClick(1)}
                  className={currentPage === 1 ? "animate-pulse" : ""}
                >
                  {1}
                </Button>

                <Button
                  variant={"outline"}
                  key={totalPages}
                  onClick={() => handleClick(totalPages)}
                  className={currentPage === totalPages ? "animate-pulse" : ""}
                >
                  {totalPages}
                </Button>

                <Button
                  variant={"outline"}
                  onClick={() =>
                    currentPage < totalPages && handleClick(currentPage + 1)
                  }
                  disabled={currentPage === totalPages}
                >
                  next
                </Button>
              </div>
            )}
          </div>
        )}
        <Button className="sm:hidden" onClick={() => setShowKill(!showKill)}>
          {showKill ? "Show Leaderboard" : "Slay Idle Adventurer"}
        </Button>
        {((isMobileDevice && showKill) || !isMobileDevice) && (
          <div className="w-full border border-terminal-green p-2">
            <KillAdventurer />
          </div>
        )}
      </div>
    </div>
  );
}
