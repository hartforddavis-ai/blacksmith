TOOLS HELD:

| Item | Law | Verdict | Deciding pass | Evidence |
| --- | --- | --- | --- | --- |
| D | LAW 1 | REJECT | ROBUST | "The dispatcher already writes one checksum per record and compares it on read." |
| E | LAW 2 | REJECT | SHOWN | "The January design does not mention an environment variable or an operator setting." |
| F | LAW 3 | REJECT | SINGLE | "The plan states that steps 1 and 2 will be built and tested as a pair, because the writer's new format cannot be exercised until the reader accepts it..." |
| G | NONE | N/A | A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three... | "Incident write-up, 8 March. At 02:15 the queue reached 1,840 and the oldest job waited 46 minutes." |
| H | LAW 1 | APPROVE | ROBUST | "On 2 March a header carrying three fields reached the queue through that branch, and a job ran against the wrong account." |
| I | LAW 2 | APPROVE | BUILT | "Run on 7 March against a queue left empty for one hour. The output file gained no rows across that hour, and gained rows again when jobs arrived." |

COUNTS
LAW 1 2 · LAW 2 2 · LAW 3 1 · NONE 1
