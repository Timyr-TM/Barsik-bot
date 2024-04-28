<img src="./src/barsik.png" align="left" width="200px" height="200px">
<h1>Barsik bot</h1>
<b>Discord bot with 🐍 Python</b>
<p>
<a href="https://python-poetry.org/">
<img alt="Poetry" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fpython-poetry.org%2Fbadge%2Fv0.json">
</a>
<img alt="Top language" src="https://img.shields.io/github/languages/top/Timyr-TM/Barsik-bot">
</p>
<p>
<a href="./changelog.md"><b>Changelog</b></a>
</p>
<br clear="both"/>
<hr/>

#  Installation

1. clone git repo
    ```commandline
    git clone https://github.com/Timyr-TM/Barsik-bot.git
   ```
2. install libs
    ```commandline
   poetry install
   ```
3. gen config
    ```commandline
    poetry poe bot --gen-config
    ```
4. set token in `config.json`
    ```json
    {
        "token": "<You are token>"
    }
    ```
5. run bot
    ```commandline
    poetry poe bot
    ```
