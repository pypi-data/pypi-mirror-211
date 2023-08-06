Lightweight wrapper for the unofficial Proton-DB API (https://protondb.max-p.me/)


Usage:

import proton_db as proton


protonDB = proton.protonDB()



getGames()
Lists all the games we have discovered so far. Returns an array of objects with these fields in it:


appId

title



getReports(appId)
Lists all reports for a given game (by Valve's appId), in reverse timestamp order. Returns an array of objects with these fields in it:


id - Server's local id

appId - The game ID for this report. Redundant for uniformity's sake.

timestamp

rating

notes

os

gpuDriver

specs

protonVersion


