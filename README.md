# Tournament benchmarker
**Tournament-benchmarker** is a python command line tool to benchmark the performance of fighting game AIs in a tournament like fashion. This tool is written in Python 3.5.

Benchmarking reinforcement learning AIs is a difficult problem (this is not limited to RL). This is doubly true in tasks where there isn't a clear optimal policy. This is tripley true in tasks involving multiple competitive agents, where the optimal policy for each episode depends on which oppoent the AI is facing on that episode. Traditional abstract statistics used to study the quality of RL AIs, such as average reward per episode or episode length, may not be too illustrative. This is because they might not directly reflect how "good" an AI is in comparison with other available AIs. 

Tournament benchmarker aims at solving this issue for 1v1 fighting games.

*Disclaimer*: Currently tournament-benchmarker is tied to the game FightingICE. FightingICE is a game maintained by [Ritsumeikan University](http://en.ritsumei.ac.jp/) as part of the [CIG Fighting game AI competition](http://www.ice.ci.ritsumei.ac.jp/~ftgaic/). This means that tournament-benchmarker only works in conjunction with this game. In the future I will decouple the game from the tool to make the module game agnostic.

## Installation

The easiest way to install this package is by running

    pip install -r https://github.com/Danielhp95/tournament-benchmarker/requirements.txt
    pip install git+https://github.com/Danielhp95/tournament-benchmarker.git
   
which will install the package and any of its dependencies.

    
## Requirements

### Python 
Tournament-benchmarker uses Python 3.5 alongside the following python packages:
+ [py4j](https://www.py4j.org/). To communicate python with the Java Virtual Machine (JVM)
+ [numpy](http://www.numpy.org/). Python's crown jewel
+ [recordclass](https://pypi.org/project/recordclass/). A mutable version of namedtuple (link).
+ [tqdm](https://github.com/tqdm/tqdm). A progress bar for python CLIs, used to estimate tournament length, as it cannot be known in advance how long matches will take.
+ [beautifultable](https://github.com/pri22296/beautifultable). To print tournament results in a good looking fashion in the terminal.

### FightingICE specifics
 
Currently, for both the `game_starter` module and some tests in the `tests/` directory rely on the existence of a directory in the parent directory of tournament-benchmarker. This means that it is not possible to use this python module  for other games (yet).

## Supported tournament types.
There are 2 tournament types which are currently supported
* **N-Round robin tournament**. A 1-round robin tournament matches each contestant to all other contestants, an N-round robin tournament matches each contestant against all other contestants N times.
+ **Round knockout**. Perhaps the most classical form of tournament. Contestants are paired and matched against the corresponding pair partner. The loser leaves the tournament and the winner goes to the next round. If the number of contestants is odd, a random contestant classifies to the next round without playing a match. This process is repeated until there is only a single contestant, who then becomes the winner of the tournament.

## Usage

```python
from tournament import Tournament
from tournament import TournamentType

> t = Tournament(tournament_type=TournamentType.ROUND_ROBIN, round_robin_rounds=3, contestant_names=['AI_1', 'AI_2', 'AI_3'])
> t.begin_tournament()
> print(t)
```
Running the code above will print to the terminal:
```
+-----------------+-------------+----------------+-------------+
| Contestant name | Matches won | Matches played | Time played |
+-----------------+-------------+----------------+-------------+
|      AI_1       |      6      |       6        |      6      |
+-----------------+-------------+----------------+-------------+
|      AI_2       |      3      |       6        |    23805    |
+-----------------+-------------+----------------+-------------+
|      AI_3       |      0      |       6        |   39940.5   |
+-----------------+-------------+----------------+-------------+

```

## Available statistics
**Note**: all time measurements is counted in game frames.
Global statistics:
+ `leaderboard`. Contestant list sorting by wins in descending order.
+ `matches`. Number of matches played throughout the tournament.
+ `total_duration`. Tournament duration in game ticks (frames)

```python
> t = Tournament(tournament_type=TournamentType.ROUND_ROBIN, round_robin_rounds=3, contestant_names=['Machete', 'RandomAI'])
> t.begin_tournament()
> # Tournament finishes
> t.leaderboard

> t.matches
3
> t.total_duration
6969
```

Per contestant statistics:
+ `wins`. Individual wins.
+ `played_matchees`. Number of matches played by this contestant.
+ `played_time`. Number of game ticks that contestant spent playing in the tournament.

```python
> # Tournament winner
> contestant_statistics = t.leaderboard[0] THIS DOES NOT WORK BECAUSE LEADERBOARD IS NEVER POPULATED
> contestant_statistics.wins
2
> contestant_statistics.played_matches
3
> contestant_statistics.played_time
6969
```

## Future plans
+ Making **tournament-benchmarker** game agnostic by creating an abstract `game_starter` module.
+ Introducing new statistics. Maybe introducing match statistics.
+ Reaching at least 80% code coverage.
+ Adding this module to the python package index [PyPi](https://pypi.org/)
