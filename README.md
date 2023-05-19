<div align="center">

# Chess AI in Python

![Issues](https://img.shields.io/github/issues/a2ys/chess-ai?style=for-the-badge) ![Forks](https://img.shields.io/github/forks/a2ys/chess-ai?style=for-the-badge) ![License](https://img.shields.io/github/license/a2ys/chess-ai?style=for-the-badge)

![Buid Status](https://img.shields.io/github/actions/workflow/status/a2ys/chess-ai/python-app.yml?style=for-the-badge) ![Release](https://img.shields.io/github/v/release/a2ys/chess-ai?include_prereleases&style=for-the-badge) ![Size](https://img.shields.io/github/repo-size/a2ys/chess-ai?label=size&style=for-the-badge)

</div>

## Description

This is a Chess AI currently in development. **It is written completely on Python, so it will be slower** than other AIs, but algorithms have been optimized wherever necessary and possible. It uses the [`Pygame`](pygame.org) library to provide the GUI and the media controls. FEN notations are supported upto castling, and future support is in development.

## How to install

[Clone the repository](https://github.com/git-guides/git-clone) in a favorable location of your choice on your local machine. The following command does the magic for you:

```shell
git clone https://github.com/a2ys/chess-ai.git
```

Even though the program uses a single library, `Pygame`, going by the [Python conventions](https://docs.python.org/3/tutorial/venv.html#:~:text=A%20common%20convention%20is%20to%20put%20this%20list%20in%20a%20requirements.txt%20file) is always recommended. So in the main program directory, run the following command:

```shell
python -m pip install -r requirements.txt
```
This command will install the required libraries for you.

Now you just have to run the `main.py` file, and enjoy the program. The following command does the magic for you:

```shell
python main.py
```

## How to use and configure?

As of now, no settings screen has been developed, so to use the program as you intend, you need to change the code. Most of the settings and their values are stored in the [`Constants.py`](defs/Constants.py) file. So to make a change, you first need to go to the file in the location `defs\Constants.py` and change the values of the constants as required. Some instructions are provided below.

### Game modes

The Game Mode, by default, is set to AI vs AI. In case you want to change it to another mode, you must do it in the following way:

- First of all, go the `Constants.py` file, and search for the variable, `GAME_MODE`. It will look like the block shown below:

    ```python
    GAME_MODE = GameModes.AI_VS_AI
    ```
- The `GAME_MODE` variable is responsible for different modes of playing the game, the values it can take are `GameModes.PLAYER_VS_PLAYER`, `GameModes.PLAYER_VS_AI` (you play as white, and the computer plays as black), `GameModes.AI_VS_PLAYER` (you play as black, and the computer plays as white) and `GameModes.AI_VS_AI` (default).
- You can change the value of the `GAME_MODE` variable to any value out of the above four.

### Initial board arrangement

The initial board in the game, by default, is set to the standard initial board. To be able to understand and edit the initial board arrangement, you should be familiar with the [FEN notation](https://www.chess.com/terms/fen-chess) in chess. In case you are familiar, and want to change the inital arrangement, you must do it in the following way:

- First of all, go to the `Constants.py` file, and search for the variable `initial_board`, which can be found in the beginning of the Python file. It will look like the block shown below:

    ```python
    initial_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    ```
- After getting to the variable, set it to the board arrangement of your choice.

### Depth of the AI

The depth to which the AI can think, by default, is set to $2$, which is sufficient for most cases. In case you want to increase or decrease the depth, you must do it in the following way:

- First of all, go the `Constants.py` file, and search for the variable, `DEPTH`. It will look like the block shown below:

    ```python
    DEPTH = 2
    ```
- A depth of $n$ means the AI looks $n$ moves in the future. The time-complexity of the move searching algorithm (negamax with alpha-beta pruning) is $O(b^{n/2})$ in most cases, and the space-complexity is $O(bn)$; where $b$ is the number of legal moves available in the position.
- Changing the `DEPTH` with change the number of moves the AI will look forward. Change this variable accoring to the processing power of your machine's processor, or just leave it unchanged.

### Colors

The Colors, by default, are set according to a visually pleasing and less noisy palette, so unless you crave for certain colors, you should leave them unchanged. In case you want to change the colors, you must do it in the following way:

- First of all, go the `Constants.py` file, and search for the following block of code somewhere in the middle:

    ```python
    # Colors format - [LIGHT, DARK]
    colors = [(238, 216, 192), (171, 122, 101)]
    highlight_colors = [(207, 172, 106), (197, 173, 96)]
    legal_move_colors = [(221, 89, 89), (197, 68, 79)]
    ```
- All the colors are in `RGB` format, in the order `(R, G, B)`. The first `tuple` in every `list` of colors denotes the color applied to the white squares, and the next one denotes the color applied to the black squares.
- The instructions below provide the steps to alter the colors correctly:
    - To change the color of the squares when the board is in `idle` state, change the values in the `colors` variable;
    - To change the color of the square of a piece which is clicked upon by the user, change the values in the `highlight_colors` variable;
    - To change the colors with which the `legal_move` squares are filled, change the values in the `legal_move_colors`.

### Dimensions and FPS

The `WIDTH`, `HEIGHT` and `FPS` variables are not recommended to be changed, so as to provide a seamless experience, but in case you want to change them, you must do it in the following way:

- First of all, go the `Constants.py` file, and find these lines:

    ```python
    WIDTH = HEIGHT = 720
    FPS = 60
    ```
- Change the values of `WIDTH` and `HEIGHT` variables, keeping both equal to each other, and a multiple of $8$, to avoid any visual inconsistency.
- Change the `FPS` to any value supported by your display.

### Final notes on usage and configuration

All the other variables/functions in the `Constants.py` file, or any other files not mentioned above are not supposed to be edited, and are important in providing necessary functionality to the program. If you want to experiment with the program, or make changes for contributions, you are free to do so with a threshold amount of knowledge in Python and about the project. Comments have been added wherever necessary to help understand the program better.

If you need further assistance with configuration, or any other topic related to this project, you can [create an issue](https://github.com/a2ys/chess-ai/issues/new/choose), or mail me at [oreus@duck.com](mailto:oreus@duck.com). Happy experimenting. :)

## Libraries in use

The program currently uses only one library, `Pygame`.

`Pygame` provides the necessary working GUI for the program, and connects it to the logic of the program. It also facilitates easy rendering of the images, as well as timely production of appropriate sounds.

## Minimum system requirements

- OS: Any operating system with Python 3.x and the required libraries installed.
- Processor: Any dual-core processor

  > The program makes an extensive use of your machine's processing power, so it is recommended to use a **quad-core** processor, for a seamless experience, even though the minimum requirement is **dual-core**.
- RAM: At least 2GB or above, DDR3 or above

  > The program extensively uses hashing and rapid storage and access of information from the machine's primary memory, so it is recommended to have a  **DDR4** memory to have a hassle-free experience.
- Permanent storage: Any storage type (SSD recommended)

## Willing to contribute?

If you are willing to add functionality to the program, you should [fork the repository](https://github.com/a2ys/chess-ai/fork) and make the desired changes. Then you should [create a pull request](https://github.com/a2ys/chess-ai/compare) to allow to merge your changes in the main branch.

Alternatively, if you find a bug/issue in the program, you can [create an issue](https://github.com/a2ys/chess-ai/issues/new/choose), and wait for it to be fixed.

Your contributions are wholeheartedly welcome.

## License

The project abides by the GNU GPL Version 3, which can be found [here](LICENSE.md).

In short:

It is a copyleft license, meaning that anyone who distributes software under this license must also provide the source code and make it available to others under the same license terms. The license also includes specific provisions to protect users from patents held by licensors, and is compatible with many other free software licenses. Additionally, the GPL Version 3 includes provisions to prevent "tivoization," which is the use of digital rights management to restrict the use of GPL-licensed software on certain hardware. The license also includes provisions for termination in the event of a violation of its terms, and for ensuring that any downstream recipients are also bound by the same terms.

The license summary above was generated by [ChatGPT](https://chat.openai.com), and is prone to errors; you should always refer to the original document for a better perspective.
