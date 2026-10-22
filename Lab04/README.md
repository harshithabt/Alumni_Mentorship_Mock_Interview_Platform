# Vibe Coding: Rhythm Tap

## Objective

Use a Vibe Coding tool to understand, fix, and extend an existing Python game. This lab focuses on writing effective prompts, implementing features in a small number of attempts, testing changes, and maintaining a Git-based development workflow.

---

## Project Information

- **Project:** Rhythm Tap
- **Language:** Python
- **Game Library:** Pygame
- **Development Repository:** [51_rhythm-tap](https://github.com/harshithabt/51_rhythm-tap)
- **Assignment Type:** Individual
- **Duration:** 60 minutes

---

## Implemented Features

### 1. Hit Sound Effects

Sound effects provide audio feedback for successful hits graded as PERFECT, GREAT, or OK.

### 2. Hold Notes

Hold notes require the player to press and sustain the corresponding lane key for the required duration.

### 3. BPM-Synchronized Spawning

Notes spawn according to the configured beats per minute (BPM), keeping note generation synchronized with the game's tempo.

### 4. Game-Over Grade Summary

At the end of the game, the summary displays the final score, PERFECT/GREAT/OK/MISS counts, accuracy percentage, and maximum combo.

## Controls

| Key | Action |
|---|---|
| D | Hit Lane 1 |
| F | Hit Lane 2 |
| J | Hit Lane 3 |
| K | Hit Lane 4 |
| R | Restart    | 

---

## How to Run

### Prerequisites

- Python 3
- pip package manager

### Installation and Execution

1. Clone or download the repository.
2. Open a terminal in the `Lab04/` directory.
3. Navigate to the code directory:

   ```bash
   cd code
   ```

4. Install the required dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Start the game:

   ```bash
   python main.py
   ```

Use the lane keys to play. For hold notes, press and sustain the corresponding lane key for the required duration.

---

## Project Structure

```text
Lab04/
├── README.md
├── PES1UG24AM118_Lab 04_Chat_History.pdf
├── videos/
│   ├── before.mp4
│   └── after.mp4
└── code/
    ├── main.py
    ├── requirements.txt
    ├── .gitignore
    └── game/
        ├── __init__.py
        ├── beat.py
        └── game_engine.py
```

---

## Deliverables

| Deliverable | Location |
|---|---|
| Updated source code | `code/` |
| Before gameplay video | `videos/before.mp4` |
| After gameplay video | `videos/after.mp4` |
| Chat history exported as PDF | `PES1UG24AM118_Lab 04_Chat_History.pdf` |

The before video records the original gameplay before modifications. The after video demonstrates the completed game and its implemented features.

## Version Control

The project was developed by modifying the assigned starter repository and maintaining the implementation in a personal GitHub repository. Git commits track the development changes and feature implementation.

The updated source code is included in this Lab 4 submission folder for evaluation.

## Related Repository

[View the Rhythm Tap development repository](https://github.com/harshithabt/51_rhythm-tap)

## Author

Harshitha B.T - PES1UG24AM118 ("AIML-B" Section)

---
