<!-- Banner here -->
# 🍄 Pynx-Shroom-Raider

A terminal-based adventure game written in **Python 3**, where you play as **Laro Craft**,  a passionate mushroom collector and daring adventurer exploring a mysterious forest while avoiding dangerous elements that may come his way.

**Laro Craft** comes from the humble village of *Kalikasan*; Laro is a devoted Filipino grandson, he embarks on a quest to heal his sick grandmother by crafting a legendary potion known as the Mighty Concoction **(a mixed of different ingredients)** that was made from rare and powerful mushrooms scattered across mystical, seasonal, and majestical land that is still unknown amongst Filipinos.

In the heart of the **“𝐋𝐢𝐛𝐥𝐢𝐛” 𝐚𝐧𝐝 “𝐊𝐚𝐬𝐮𝐥𝐮𝐤𝐬𝐮𝐥𝐮𝐤𝐚𝐧𝐠”** village of Kalikasan, there lies a simple *𝐛𝐚𝐡𝐚𝐲-𝐤𝐮𝐛𝐨* positioned beneath the shade of ancient balete trees. Within it resides an old but daring Lola whose wisdom once guided generations, now silenced by a mysterious illness that drains her strength with each passing moon.

No one knows what this mysterious illness might be, but…

Legends whisper of a cure: the 𝐌𝐈𝐆𝐇𝐓𝐘 𝐂𝐎𝐍𝐂𝐎𝐂𝐓𝐈𝐎𝐍...

Will you help him traverse the dangerous wilderness and find the cure?

**🫣 Sneak Peek**
<!-- <video src=''></video> -->

---
## 📘 Table of Contents
1. [🕹️ User Manual](#️-user-manual)
    - [🚩 Goal](#-goal)
    - [🏃 How to Run the Game](#-how-to-run-the-game)
    - [🎮 Controls](#-controls)
2. [⚙️ Mechanics](#️-mechanics)
    - [🧱 Tiles and Items Overview](#-tiles-and-items-overview)
3. [🧑‍💻 About Codebase](#about-codebase)
    - [📁 Directory Structure](#-directory-structure)
    - [🤔 How It Works](#-how-it-works)
4. [🧪 Unit Testing](#-unit-testing)
    - [🏃 Running the Tests](#-running-the-tests)
    - [🚨 Test Coverage](#-test-coverage)
    - [➕ Adding New Tests](#-adding-new-tests)
5. [⭐ Bonus Features](#-bonus-features)
6. [📚 References](#-references)
7. [👥 Team Information](#-team-information)
8. [⚖️ License & Copyright](#️-license--copyright)

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
        python3 shroom_raider.py -f levels/fall/stage1.txt
        ```

    - **Option 3: Automated Mode**

        Run a game using a sequence of moves and output the final result:
        ```bash
        python3 shroom_raider.py -f <stage_file> -m <string_of_moves> -o <output_file>
        ```
        Example
        ```bash
        python3 shroom_raider.py -f levels/fall/stage1.txt -m "DDWW" -o result.txt
        ```

        This command will:
        - Simulate the sequence of moves (right, right, up, up),
        - Produce no console output,
        - Write the final state and result (`CLEAR` or `NO CLEAR`) to `result.txt`.

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
├──__pycache__/
├── generated_maps/ 
├── shroom_raider.py                    # Shroom Raider: base game points
├── shroom_raider_extra.py              # Shroom Raider: Additional Feature points
├── utils/                              # Other helper functions
│   ├── algorithm.py                        # Algorithm to find optimal solution
│   ├── game_progress.py                    # Game Level Progression 
│   ├── movement_extra.py                   # Shroom Raider: Advanced Movement Features
│   ├── movement.py                         # Shroom Raider: Core Movement Mechanics
│   ├── parser.py                           # Game Parsing System 
│   ├── settings.py                         # All global variables
│   ├── storyline.py                        # Shroom Raider Storyline
│   ├── ui.py                               # All screen and UI management
│   └── validator.py                        #
│
│
├── tests/                              # Testing Game Function with Pytest
│   ├── __pycache__/
│   ├── test_movement/
│   ├── test_parser/
│   ├── test_shroom_raider/
│   ├── test_ui/
│   └── test_validator/
│
├── levels/                             # Game levels  
│   └── fall/                               # FALL  SEASON : Third season of the game
│       ├── stage1.txt
│       ├── stage2.txt
│       ├── stage3.txt
│       ├── stage4.txt
│       ├── stage5.txt
│       └── stage6.txt
│   └── spring/                             # SPRING  SEASON : First season of the game
│       ├── stage1.txt
│       ├── stage2.txt
│       ├── stage3.txt
│       ├── stage4.txt
│       ├── stage5.txt
│       └── stage6.txt
│   └── summer/                             # SUMMER  SEASON : Second season of the game
│       ├── stage1.txt
│       ├── stage2.txt
│       ├── stage3.txt
│       ├── stage4.txt
│       ├── stage5.txt
│       └── stage6.txt
│   └── temple/                             # TEMPLE STAGE : Final level of the game
│       ├── stage1.txt
│       ├── stage2.txt
│       ├── stage3.txt
│       ├── stage4.txt
│       ├── stage5.txt
│       └── stage6.txt
│   └── winter/                             # WINTER  SEASON : fourth season of the game
│       ├── stage1.txt
│       ├── stage2.txt
│       ├── stage3.txt
│       ├── stage4.txt
│       ├── stage5.txt
│       └── stage6.txt
│
├── requirements.txt                    
├── LICENSE
└── README.md
```

### 🤔 How It Works

<!-- ![Flowchart](./assets/flowchart.drawio.svg) -->
<!-- How your algorithm works and how that step is implemented -->

---

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
        <td><code>test_movement.py</code></td>
        <td>Test the user input and fire spread mechanics.</td>
    </tr>
    <tr>
        <td><code>test_parser.py</code></td>
        <td>Test the level information of the map, test the locations, </br>
        and test the parse output.</td>
    </tr>
    <tr>
        <td><code>test_ui.py</code></td>
        <td>Test the game ui.</td>
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

1. Modify `test_custom/test_user.py` in the function `test_functionality`.
2. Include all necessary `assert`s in different function so long as it starts with `test_`.
3. Run `pytest` again to verify!

---

## ⭐ Bonus Features

<table>
    <tr>
        <th>Feature</th>
        <th>Description</th>
    </tr>
    <tr>
        <td style="text-align: left; vertical-align: top;">Main Menu</td>
        <td>A central hub where players can start the game. </br> 
        The panel includes options to log in, sign up, play locally, or exit.</td>
    </tr>
    <tr>
        <td>Log in and Sign up for player</td>
        <td>Allows users to create accounts or access existing ones.</td>
    </tr>
    <tr>
        <td style="text-align: left; vertical-align: top;">Ability to exit the game/program via a command.</td>
        <td>Allows players to quit the game or program at any </br>
        time using a specific command.</td>
    </tr>
    <tr>
        <ul>
        <td style="text-align: left; vertical-align: top;">Playmode</td>
        <td>Offers different gameplay options: </br>
        <li> <b>Play Locally </b> - Can be played without signing in.</li> 
        <li><b>Unlocked Levels</b> - Stores the levels you have unlocked. </li>
        <li><b>Story Mode</b> - Start from the beginning of the game’s storyline.</li>
        <li><b>Endless Mode</b> The game loops continuously without an end.</li> 
        <li><b>Online Battle</b>  Play multiplayer matches online: </li>
            <ul>
            <li><b>Ranked Match</b></li>
            <li><b>Unranked Match</b></li>
            </ul>
        </ul>
        </td>
    </tr>
    <tr>
        <td style="text-align: left; vertical-align: top;">Leaderboard and Username input</td>
        <td>Players enter a username to track scores, which </br>
        are displayed on the leaderboard for ranking.</td>
    <tr>
        <ul>
        <td style="text-align: left; vertical-align: top;">Persistent leaderboard</td>
        <td><b>Tracks and displays player scores across sessions.</b>
        <li>Tracks level leaderboards across different seasons.</li>
        <li>Stores the moves used to complete each level.</li>
        </td>
        </ul>
    </tr>
        </tr>
        <td style="text-align: left; vertical-align: top;">Game Settings</td>
        <td>Lets players adjust game controls preference </br>
        (Keyboard or Gamepad Recognition)</td>
    </tr>
    </tr>
        </tr>
        <td>Storyline</td>
        <td>Laro’s game narrative and objectives.</td>
    </tr>
    </tr>
        </tr>
        <td>Algorithm to find optimal solution</td>
        <td>This function identifies the optimal solution for the </br>
        game stage and generates the appropriate output.</td>
    </tr>
        </tr>
        </tr>
        <td> Fancier user interface</td>
        <td>Calculates the terminal width to determine the screen layout,</br>
        and adjusts the map based on the available display size.</td>
    </tr>
</table>

## 📚 References

The following resources were used in creating this project:
- [Python Documentation](https://docs.python.org/3/)
- [Pytest Framework Docs](https://docs.pytest.org/en/stable/)
- [Emojipedia](https://emojipedia.org/)
- Stack Overflow discussions on:
    - String-Terminal Interaction Information [1](https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python) [2](https://stackoverflow.com/questions/70573954/python-curses-detect-texts-display-width-before-printing-it)

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
