<div align="center">

# Chess AI in Python

![Issues](https://img.shields.io/github/issues/a2ys/chess-ai?style=for-the-badge) ![Forks](https://img.shields.io/github/forks/a2ys/chess-ai?style=for-the-badge) ![License](https://img.shields.io/github/license/a2ys/chess-ai?style=for-the-badge)

</div>

### Description

This is a Chess AI currently at the end of development. **It is written completely on Python, so it will be slower** than other AIs out in the market, but algorithms have been optimised wherever necessary and possible. It uses the [`Pygame`](pygame.org) library to provide the GUI and the media controls. FEN notations are supported upto castling, and future support is in development.

### How to install

[Clone the repository](https://github.com/git-guides/git-clone) in your favorable location on your local machine. The following command does the magic for you:

```
git clone https://github.com/a2ys/chess-ai.git
```

Even though the program uses a single library, `Pygame`, going by the [Python conventions](https://docs.python.org/3/tutorial/venv.html#:~:text=A%20common%20convention%20is%20to%20put%20this%20list%20in%20a%20requirements.txt%20file) is always recommended. So in the main program directory, run the following command:

```
python -m pip install -r requirements.txt
```
This command will install the required libraries for you.

Now you just have to run the `main.py` file, and enjoy the program. The following command does the magic for you:

```
python main.py
```

### Libraries in use

The program currently uses only one library, `Pygame`.
Pygame provides the necessary working GUI for the program, and connects it to the logic of the program. It also facilitates easy rendering of the images, as well as timely production of appropriate sounds.

### Minimum system requirements

- OS: Any operating system with Python 3.x and the required libraries installed.
- Processor: Any **dual-core** processor.
  > The program makes an extensive use of your machine's processing power, so it is recommended to use a **quad-core** processor, for a seamless experience, even though the minimum requirement is **dual-core**.
- RAM: At least 2GB or above, DDR3 or above
  > The program extensively uses hashing and rapid storage and access of information from the machine's primary memory, so it is recommended to have a  **DDR4** memory to have a hassle-free experience.
- Permanent storage: Any storage type (SSD recommended)

### Contributing

If you are willing to add functionality to the program, you should [fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo) and make your desired changes. Then you should [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to allow to merge your changes in the main branch.

Alternatively, if you find a bug/issue in the program, you can [create an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues), and wait for it to be fixed.

Your contributions are wholeheartedly welcome.

### License - GNU GPL-3.0
TL;DR - It is a copyleft license, meaning that anyone who distributes software under this license must also provide the source code and make it available to others under the same license terms. The license also includes specific provisions to protect users from patents held by licensors, and is compatible with many other free software licenses. Additionally, the GPL Version 3 includes provisions to prevent "tivoization," which is the use of digital rights management to restrict the use of GPL-licensed software on certain hardware. The license also includes provisions for termination in the event of a violation of its terms, and for ensuring that any downstream recipients are also bound by the same terms.
