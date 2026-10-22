# Lab 4 - Vibe Coding: Rhythm Tap

## Objective

Use a Vibe Coding tool to understand, fix, and extend an existing Python game. The objective is to practice writing effective prompts, implementing features in a small number of attempts, testing changes, and maintaining a Git-based development workflow.

## Project Information

- **Project:** Rhythm Tap
- **Language:** Python
- **Game library:** Pygame
- **Development repository:** [51_rhythm-tap](https://github.com/harshithabt/51_rhythm-tap)
- **Assignment type:** Individual
- **Duration:** 60 minutes

## Implemented Features

### 1. Hit Sound Effects
Sound feedback is generated for successful hits graded as PERFECT, GREAT, or OK.

### 2. Hold Notes
Hold notes require the player to press and sustain the corresponding lane key for the required duration.

### 3. BPM-Synchronized Spawning
Notes spawn according to the configured beats per minute (BPM), using the beat interval to control timing.

### 4. Game-Over Grade Summary
At the end of the game, the summary displays the score, PERFECT/GREAT/OK/MISS counts, accuracy percentage, and maximum combo.

## How to Run

1. Install Python.
2. Open a terminal in the `code/` directory.
3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the game:

   ```bash
   python main.py
   ```

Use the lane keys displayed by the game to play. Refer to the source code and the project repository for implementation details.

## Deliverables

| Deliverable | Location |
|---|---|
| Updated source code | `code/` |
| Before gameplay recording | `videos/before.mp4` |
| After gameplay recording | `videos/after.mp4` |
| Chat history exported as PDF | `PES1UG24AM118_Lab 04_Chat_History.pdf` |

The before video records the original game before modifications. The after video demonstrates the implemented features.

## Version Control

The implementation was developed in the dedicated Rhythm Tap repository, with commits used to track feature implementation and fixes. The updated code is included in this Lab 4 submission folder.

## Related Repository

[Open the Rhythm Tap development repository](https://github.com/harshithabt/51_rhythm-tap)
