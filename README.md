# PyPong
Multiplayer (P2P and client/server modes) **Pong** game written in Python using PyGames.


### Controls

* <kbd>&uarr;</kbd> - move your paddle up
* <kbd>&darr;</kbd> - move your paddle down
* <kbd>Space</kbd> - release ball if it's your turn*

First turn is for `Player 2`. Next turns are whoever lost last round.

### Platforms tested

* Windows (Python 3.5.0 x86, might work with older too)


### Dependencies

* PyGames (1.9.2, migth work with a lot older too)


### Network layer

Under the hood it uses custom abstraction layer on top of `socket` module.


### License

See [LICENSE](LICENSE) file.


### Gallery

![Imgur](http://i.imgur.com/lpHSEer.png)
