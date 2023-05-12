# ColorBuster Game Manual

## How to Play

The goal of this game is to get as high of a score as possible by popping sets of tiles.
To pop tiles, you must click on a tile that has four or more adjacent tiles of the same color of the one you clicked.
The points given for each set grow exponentially depending on the number of popped tiles in one click.
As tiles below get popped, the tiles above fill in the space and new tiles get dynamically generated.
The game ends when there are no more tile sets with four or more adjacent tiles of the same color; at that point you can start a new game.

### How points are calculated

Points are calculated using the [triangle number sequence](https://en.wikipedia.org/wiki/Triangular_number), in code:

``self.score += (((numberOfPoppedTiles-4))*((numberOfPoppedTiles-4)+1)//2)+4``

## Developer Notes

### Limitations
At the very beginning of this project, I had the idea of doing it implementing pygame.
This would end up not being the smartest idea since I didn't have ease of implementation in mind.
I choose pygame because I've always wanted to get more familiar with it;
but if this was a client funded project, that sort of reasoning would rather insufficient.
The overall product is quite minimal but still captures the fundamentals of the game's elements.

### Implementations
In addition to the foundations of the game, I implemented a tile highlight feature, a hint timer, and audio.

#### Cursor Tile Highlighting
This feature temporarily colors tiles that your cursor is on in a lighter color.
Since there is no boarder on the tiles it can be hard to visually separate tiles of the same color.

#### Hint Timer
Instead of drawing another button, I decided to have hints show on an timing based system.
Once the player's mouse has been inactive for around 5 seconds the first calculated available move will highlight.
The count for this event will restart whenever the mouse moves and when a tile is clicked.

#### Audio & Music
I have music for the player to enjoy(hopefully) while the application is open.
The player can toggle the music on/off by pressing the m key, for "mute".
Clicking on tiles will also result in sound feedback.
A higher pitched sound will play when a valid tile is clicked and a lower pitch one when an invalid tile is clicked.

### Future Iterations
I would like to add a settings display that can pop up, where users can chose between different soundtracks, colorlayouts, and difficulties.
I like how the 5x5 layout looked but I could also add some variety there for players that would like it.
The next thing would be to create a database system for scores to be stored, so players can have fun trying to beat their hi-scores without haveing to remember it themselves.