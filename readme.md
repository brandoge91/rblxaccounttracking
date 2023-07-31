# Simple roblox account tracking

A simple python discord bot that tracks roblox users total play time and provides a few couple of extra details.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary packages.

```bash
pip install -r requirements.txt
```

This project uses [Mongo](https://www.mongodb.com/) as the database so it's essential we set it up correctly, you'll need a connection string as well as a database named ``accountTracker`` and 2 collections ``usersData`` & ``usersToTrack``.

Finally make sure you have made a copy of ``.env.example`` and updated it to ``.env`` and filled out all the variables.


* ``botToken`` - Your discord bot token, read up on getting it [here](https://www.writebots.com/discord-bot-token/).
* ``connectionString`` - A MongoDb connection string, read [here](https://www.mongodb.com/docs/manual/reference/connection-string/).
* ``botCookie`` - A roblox account cookie (don't use your main account!), read on getting one [here](https://ro.py.jmk.gg/dev/roblosecurity/).



## Usage


To run the bot run the ``main.py`` file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

*  GNU GENERAL PUBLIC LICENSE