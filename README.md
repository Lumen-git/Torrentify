# Torrentify

The Torrentify tool walks a file tree and makes torrents for each file it finds, saving them to an identical tree.

Files
|  Shared
|  |_Book.txt

becomes:

Torrents
| Files
| | Shared
| | |_Book.torrent

The tool also connects to a qBittorent web API to start seeding the torrents it makes.
