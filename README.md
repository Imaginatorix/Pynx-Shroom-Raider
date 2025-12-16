<!-- Banner here -->
# 🍄 Pynx-Shroom-Raider

A terminal-based adventure game written in **Python 3**, where you play as **Laro Craft**,  a passionate mushroom collector and daring adventurer exploring a mysterious forest while avoiding dangerous elements that may come his way.

**Laro Craft** comes from the humble village of *Kalikasan*; Laro is a devoted Filipino grandson, he embarks on a quest to heal his sick grandmother by crafting a legendary potion known as the Mighty Concoction **(a mixed of different ingredients)** that was made from rare and powerful mushrooms scattered across mystical, seasonal, and majestical land that is still unknown amongst Filipinos.

In the heart of the **“𝐋𝐢𝐛𝐥𝐢𝐛” 𝐚𝐧𝐝 “𝐊𝐚𝐬𝐮𝐥𝐮𝐤𝐬𝐮𝐥𝐮𝐤𝐚𝐧𝐠”** village of Kalikasan, there lies a simple *𝐛𝐚𝐡𝐚𝐲-𝐤𝐮𝐛𝐨* positioned beneath the shade of ancient balete trees. Within it resides an old but daring Lola whose wisdom once guided generations, now silenced by a mysterious illness that drains her strength with each passing moon.

No one knows what this mysterious illness might be, but…

Legends whisper of a cure: the 𝐌𝐈𝐆𝐇𝐓𝐘 𝐂𝐎𝐍𝐂𝐎𝐂𝐓𝐈𝐎𝐍...

Will you help him traverse the dangerous wilderness and find the cure?

### [📖 **Sphinx Documentation (HTML)**](docs/_build/html/index.html)

<!-- **🫣 Sneak Peek** -->
<!-- <video src=''></video> -->

---
## 📘 Table of Contents
1. [🕹️ User Manual](#️-user-manual)
    - [🚩 Goal](#-goal)
    - [🏃 How to Run the Game](#-how-to-run-the-game)
    - [🎮 Controls](#-controls)
    - [📶 Leaderboard Mechanics](#-Leaderboard)
2. [⚙️ Mechanics](#️-mechanics)
    - [🧱 Tiles and Items Overview](#-tiles-and-items-overview)
3. [🧑‍💻 About Codebase](#about-codebase)
    - [📁 Directory Structure](#-directory-structure)
4. [🧪 Unit Testing](#-unit-testing)
    - [🏃 Running the Tests](#-running-the-tests)
    - [🚨 Test Coverage](#-test-coverage)
    - [➕ Adding New Tests](#-adding-new-tests)
5. [📚 References](#-references)
6. [👥 Team Information](#-team-information)
7. [⚖️ License & Copyright](#️-license--copyright)

---

## 🕹️ User Manual

### 🚩 Goal

Navigate through a forest grid, collect every mushroom 🍄 while avoiding falling victim to the dangerous external elements (e.g. water 🟦).

### 🏃 How to Run the Game

1. Clone the repository
    ```bash
    git clone https://github.com/Imaginatorix/Pynx-Shroom-Raider.git
    cd pynx-shroom-raider
    ```
2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
3. Play!
    - **Option 1: Adventure Mode**

        Play directly from your terminal:
        ```bash
        python3 shroom_raider.py
        ```
        This goes through all the levels in order.

    - **Option 2: Play a Specific Stage**

        ```bash
        python3 shroom_raider.py -f <stage_file>
        ```
        Example
        ```bash
        python3 shroom_raider.py -f levels/challenge/stage1.txt
        ```

    - **Option 3: Automated Mode**

        Run a game using a sequence of moves and output the final result:
        ```bash
        python3 shroom_raider.py -f <stage_file> -m <string_of_moves> -o <output_file>
        ```
        Example
        ```bash
        python3 shroom_raider.py -f levels/challenge/stage1.txt -m "DDWW" -o result.txt
        ```

        This command will:
        - Simulate the sequence of moves (right, right, up, up),
        - Produce no console output,
        - Write the final state and result (`CLEAR` or `NO CLEAR`) to `result.txt`.

    - **Option 4: Leaderboard Mode**

        Show the leaderboard depending on the stage file given:
        ```bash
        python3 shroom_raider.py -l <stage_file>
        ```
        Example
        ```bash
        python3 shroom_raider.py -l levels/challenge/stage1.txt
        ```


### 🎮 Controls

<table>
    <tr>
        <th>Key</th>
        <th>Action</th>
    </tr>
    <tr>
        <td>W</td>
        <td>Move Up</td>
    </tr>
    <tr>
        <td>A</td>
        <td>Move Left</td>
    </tr>
    <tr>
        <td>S</td>
        <td>Move Down</td>
    </tr>
    <tr>
        <td>D</td>
        <td>Move Right</td>
    </tr>
    <tr>
        <td>P</td>
        <td>Pick up item on current tile</td>
    </tr>
    <tr>
        <td>!</td>
        <td>Reset the stage</td>
    </tr>
</table>

***Notes:***
- Controls are case-insensitive (w = W).
- You can input multiple moves at once (e.g., `WASD`) before pressing Enter.
- Invalid input does nothing and re-prompts you.

---
### 📶 Leaderboard
- The leaderboard ranks the `top 10 users` based on the **number of moves** done per stage file. 
- After collecting all mushrooms, the number of moves the player used to get all the mushrooms. The move count will reset when the player inputs `!` to restart the level.
- The leaderboard will be shown directly after winning the game.
- The leaderboard can also be shown using the `-l` flag when running the game ([see instructions](#-Leaderboard))
- Stored in a .json file locally after cloning the repository.

## ⚙️ Mechanics

### 🧱 Tiles and Items Overview

<table>
    <tr>
        <th>UI</th>
        <th>ASCII</th>
        <th>Name</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>🧑</td>
        <td>L</td>
        <td>Laro Craft</td>
        <td>It's you!</td>
    </tr>
    <tr>
        <td>'&#x3000;'</td>
        <td>.</td>
        <td>Empty tile</td>
        <td>Walkable tile</td>
    </tr>
    <tr>
        <td>🌲</td>
        <td>T</td>
        <td>Tree</td>
        <td>Blocks movement; cut or burn to clear</td>
    </tr>
    <tr>
        <td>🍄</td>
        <td>+</td>
        <td>Mushroom</td>
        <td>Collect to score</td>
    </tr>
    <tr>
        <td>🪨</td>
        <td>R</td>
        <td>Rock</td>
        <td>Can be pushed into walkable tiles and turn water tiles to paved tiles</td>
    </tr>
    <tr>
        <td>🟦</td>
        <td>~</td>
        <td>Water</td>
        <td>Lose if you fall in; turns into paved tiles when rock is pushed in</td>
    </tr>
    <tr>
        <td>⬜</td>
        <td>_</td>
        <td>Paved</td>
        <td>Walkable tile</td>
    </tr>
    <tr>
        <td>🪓</td>
        <td>x</td>
        <td>Axe</td>
        <td>Cuts one tree (single use)</td>
    </tr>
    <tr>
        <td>🔥</td>
        <td>*</td>
        <td>Flamethrower</td>
        <td>Burns connected trees (single use)</td>
    </tr>
</table>

---

<h2 id="about-codebase">🧑‍💻 About Codebase</h2>

### 📁 Directory Structure

```bash
Pynx-Shroom-Raider/
├── shroom_raider.py                    # Shroom Raider: base game integrated with leaderboard
├── utils/                              # Other helper functions
│   ├── custom_types/                       # Classes and enums used
│   ├── leaderboard.py                      # Leaderboard logic 
│   ├── movement.py                         # Shroom Raider: Core Movement Mechanics
│   ├── parser.py                           # Game Parsing System 
│   ├── settings.py                         # All global variables
│   ├── ui.py                               # All screen and UI management
│   └── validator.py                        # Internal validation 
│
│
├── tests/                              # Testing Game Function with Pytest
│   ├── data_generator/
│   ├── test_custom/
│   ├── test_parser/
│   ├── test_shroom_raider/
│   ├── test_validator/
│   ├── conftest.py
│   └── unit_test_format.py
│
├── docs/                               # Sphinx generated docs
│
├── levels/                             # Game levels  
│   ├── challenge/                             #  The three map designs that our group submit
│   │   ├── stage1.txt
│   │   ├── stage2.txt
│   │   └── stage3.txt
│   └── stage0.py                              #  Default map for the game
├── requirements.txt                    
├── LICENSE
└── README.md
```



## 🧪 Unit Testing

Unit tests are written using `pytest`, as required.

### 🏃 Running the Tests

To execute all tests, run:
```bash
pytest
```

### 🚨 Test Coverage

<table>
    <tr>
        <th>Test Directory</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>test_parser.py</code></td>
        <td>Test the level information of the map, test the locations, </br>
        and test the parse output.</td>
    </tr>
    <tr>
        <td><code>test_shroom_raider.py</code></td>
        <td>Test the core game mechanics.</td>
    </tr>
    <tr>
        <td><code>test_validator.py</code></td>
        <td>Test the validation of game information, and location.</td>
    </tr>
</table>

The tests:
- Covers all movement directions and item interactions.
- Includes valid and invalid input handling.
- Simulates multiple endgame states.
- And other criteria for thoroughness

### ➕ Adding New Tests

1. Modify `tests/test_custom/test_user.py` in the function `test_functionality`.
2. Include all necessary `assert`s in different function so long as it starts with `test_`.
3. Run `pytest` again to verify!

---

## 📚 References

### Core Documentation
- [Python Documentation](https://docs.python.org/3/)
- [Pytest Framework Documentation](https://docs.pytest.org/en/stable/)
- [Emojipedia](https://emojipedia.org/)
- [Pillow (PIL.Image) Documentation](https://pillow.readthedocs.io/en/stable/reference/Image.html#module-PIL.Image)
- [Python `calendar` Module](https://docs.python.org/3.14/library/calendar.html#module-calendar)
- [Python `random` Module](https://docs.python.org/3/library/random.html)
- [Python `string` Module](https://docs.python.org/3/library/string.html)

### Style Guides & Documentation Standards
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 8 Checker (PDF)](https://app.readthedocs.org/projects/pep8/downloads/pdf/release-1.7.x/)
- [Python Docstrings Guide (DataCamp)](https://www.datacamp.com/tutorial/docstrings-python)
- [NumPy Docstring Standard](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Sphinx Documentation Tutorial (YouTube)](https://www.youtube.com/watch?v=nZttMg_n_s0)

### Pytest & Testing Resources
- [Pytest: Generate Tests vs `mark.parametrize`](https://pytest-with-eric.com/introduction/pytest-generate-tests/#Comparing-pytest-mark-parametrize-and-pytest-generate-tests)
- [Limiting Maximum Runtime for Unit Tests](https://stackoverflow.com/questions/19527320/how-can-i-limit-the-maximum-running-time-for-a-unit-)

### Stack Overflow Discussions

#### Terminal & Console Handling
- [Get Linux Console Window Width in Python](https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python)
- [Detect Text Display Width Before Printing (curses)](https://stackoverflow.com/questions/70573954/python-curses-detect-texts-display-width-before-printing-it)
- [Programmatically Change Console Font Size](https://stackoverflow.com/questions/52336257/python-programmatically-change-console-font-size)
- [Resize the Terminal with Python](https://stackoverflow.com/questions/6418678/resize-the-terminal-with-python)
- [Detect Window Resize in Python](https://stackoverflow.com/questions/65310175/how-to-detect-window-resize-in-python)

#### Performance & Language Details
- [Most Negative Value for Python Integers](https://stackoverflow.com/questions/4241832/most-negative-value-for-python)
- [`deepcopy` Performance Issues](https://stackoverflow.com/questions/24756712/deepcopy-is-extremely-slow)

### Algorithms & Procedural Generation

#### Talks & Videos
- [Ty Taylor — *The Art and Science of Procedural Puzzle Generation*](https://www.youtube.com/watch?v=Mssc0S8GeFI)
- [Procedural Generation of Sokoban Levels](https://www.youtube.com/watch?v=ljj6rAaM4A8)

## 👥 Team Information

**Course:** CS 11 - Introduction to Computer Science 1

**Section:** 25.1

**Project:** Shroom Raider

**Institution:** University of the Philippines Diliman

**Developed by:**
- 👤 Divina, Ken
- 👤 Domingo, Ericson
- 👤 Jumawan, Edward Isaac

## ⚖️ License & Copyright

See the [LICENSE](LICENSE) file for license rights and limitations (MIT).
