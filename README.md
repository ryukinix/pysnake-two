## __two-snake__

## Abstract

A remake and modification of the __Snake Game__ with Pygame + Python! The game shoud have better graphics, but yet, is not so GOOD. 

## My Feelings

Myself even drew all sprites in photoshop manually (with mouse!). And I confess to all of you, I'm no talent in the art of drawing — unfortunately. The key central of this game is the idea to play with two players local a Snake Game! I (think) this very fun. I'm fight with my friends. Local game is very funs... it's nostalgic.

**NOTE: This software is alpha yet and your focus is the learning in control datas on logic games.**

![Game Image](two-snake.png)

## Usage

Player |     Keys    | Moviment 
------ | ----------- | --------
One    |      W      |    Up
One    |      A      |   Left
One    |      S      |   Down
One    |      D      |   Right
Two    |  Up arrow   |    Up
Two    |  Left arrow |   Left
Two    |  Down arrow |   Down
Two    |  Right arrow|   Right


__There's also action keys!__

 Key  |      Action       |
------| ----------------  |
 ESC  |  Pause game       |
 F1   |  Speed Up (FPS)   |
 F2   |  Speed Down (FPS) |



## Dependency

You do **need** of:
  * [Python](https://www.python.org/)
  * [Pygame](http://www.pygame.org/download.shtml)

To install pygame in linux debian-based you have two options:

  * Using **apt**:
    ```bash
    sudo apt-get install python-pygame
    ```
 
  * Using **pip**:
    ```bash
    sudo pip install pygame
    ```
      
     
## Observation

This game was write previously in python3 on Windows. But i have add other file to suport python2 + pygame on Linux, a dumb solution for that (in future i fix that correctly).


*Remind*: In linux, the standard python version for pygame is python 2.x, then use the version *_2.py if have problens with this! 

  * Update_**_6246_**x: I probably fix that thing with parallels universes on python2 // python3 after the commit **_6246_**x


## License

This project is license on __[Apache v2](http://www.apache.org/licenses/LICENSE-2.0.html)__!

## Roadmap 
  - [ ] When the some snake death: not restart game, but reboot that instance only (most important currently).
  - [ ] Background sprite and textures.
  - [ ] Generate random food with __perfect__ prevision to not generate below at any snake on the board.
  - [ ] Compatiblites with python2 and python3 on same code.
  - [X] Sprites player with two colors diffs: head, body, turn and tail.
  - [X] A system with highscore and parser to verify and save on the exits of game the most highscore you won with that execution.
  - [x] Musics and other sounds interactives.
  - [X] Pause game


## Contributors
 * Me (Manoel Vilela).


