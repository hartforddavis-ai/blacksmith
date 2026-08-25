TOOLS HELD: none

| Item | Law | Verdict | Deciding pass | Evidence |
| D | LAW 1 | REJECT | SIMPLE | "The dispatcher already writes one checksum per record and compares it on read. That comparison is what surfaced the 4 March record — the mismatch was logged by it, and the log line is quoted in the incident file." |
| E | LAW 2 | REJECT | MATCHED | "The January design does not mention an environment variable or an operator setting." |
| F | LAW 3 | REJECT | SINGLE | "The plan states that steps 1 and 2 will be built and tested as a pair, because the writer's new format cannot be exercised until the reader accepts it, and the reader has nothing to accept until the writer emits it." |
| G | NONE | N/A | "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists." | "The write-up closes by recording that an engineer has been asked to bring a proposal to the 15 March review." |
| H | LAW 1 | APPROVE | ROBUST | "Feeding the same header to a copy of the dispatcher sends it down the same branch every time it is fed." |
| I | LAW 2 | APPROVE | MATCHED | "The build: the sampler writes a row when the queue holds one or more jobs, and writes nothing when it holds none. The branch that wrote a zero row was deleted; it is not in the file." |

COUNTS
LAW 1 2 · LAW 2 2 · LAW 3 1 · NONE 1
