import pygame
import random
import math
import array

from game.beat import Note, LANES, LANE_KEYS, LANE_LABELS, LANE_COLORS

WIDTH, HEIGHT = 480, 640
FPS = 60
HIT_Y = HEIGHT - 80
HIT_WINDOW = 30
BG = (15, 10, 25)
LANE_W = WIDTH // LANES
HOLD_DURATION = 1000
BPM = 120


class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.hit_sounds = {
            "PERFECT": self.make_tone(1000),
            "GREAT": self.make_tone(750),
            "OK": self.make_tone(500),
        }
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rhythm Tap")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 22, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 40, bold=True)
        self.reset()

    def make_tone(self, frequency, duration=0.10, volume=0.25):
        sample_rate = 44100
        samples = array.array("h")
        for i in range(int(sample_rate * duration)):
            fade = 1.0 - i / (sample_rate * duration)
            value = int(32767 * volume * fade * math.sin(
                2 * math.pi * frequency * i / sample_rate
            ))
            samples.extend((value, value))
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def reset(self):
        self.notes = []
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.misses = 0
        self.grade_counts = {"PERFECT": 0, "GREAT": 0, "OK": 0, "MISS": 0}
        self.bpm = BPM
        self.beat_interval_ms = 60000.0 / self.bpm
        self.last_spawn_time = pygame.time.get_ticks()
        self.speed = 5
        self.frame = 0
        self.feedback = []
        self.game_over = False
        self.held_keys = set()
        self.hold_progress = {}

    def spawn_note(self):
        lane = random.randint(0, LANES - 1)
        is_hold = random.random() < 0.25
        self.notes.append(Note(lane, y=-30, speed=self.speed, is_hold=is_hold))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset()
                    continue
                if self.game_over or event.key in self.held_keys:
                    continue
                self.held_keys.add(event.key)
                for lane, key in enumerate(LANE_KEYS):
                    if event.key == key:
                        self.process_tap(lane)
                        break
            elif event.type == pygame.KEYUP:
                self.held_keys.discard(event.key)
        return True

    def record_miss(self, lane=None):
        self.misses += 1
        self.grade_counts["MISS"] += 1
        self.combo = 0
        if lane is not None:
            lane_x = lane * LANE_W + LANE_W // 2
            self.feedback.append(["MISS", (220, 60, 60), 40, lane_x, HIT_Y - 30])

    def process_tap(self, lane):
        if lane in self.hold_progress:
            return
        best = None
        best_dist = float("inf")
        for note in self.notes:
            if note.lane != lane or note.hit or note.missed:
                continue
            if any(hold["note"] is note for hold in self.hold_progress.values()):
                continue
            dist = abs(note.y + Note.HEIGHT // 2 - HIT_Y)
            if dist < best_dist:
                best_dist = dist
                best = note

        lane_x = lane * LANE_W + LANE_W // 2
        if best is None or best_dist > HIT_WINDOW:
            self.record_miss(lane)
            return

        if best.is_hold:
            best.y = HIT_Y - Note.HEIGHT // 2
            self.hold_progress[lane] = {
                "note": best,
                "start": pygame.time.get_ticks(),
            }
            self.feedback.append(["HOLD!", (100, 220, 255), 40, lane_x, HIT_Y - 60])
            return

        best.hit = True
        if best_dist < 8:
            grade, points, color = "PERFECT", 300, (255, 220, 0)
        elif best_dist < 18:
            grade, points, color = "GREAT", 200, (100, 220, 100)
        else:
            grade, points, color = "OK", 100, (180, 180, 255)

        self.grade_counts[grade] += 1
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        self.score += points * max(1, self.combo // 5)
        self.feedback.append([grade, color, 40, lane_x, HIT_Y - 30])
        self.hit_sounds[grade].play()

    def update_hold_notes(self):
        now = pygame.time.get_ticks()
        for lane, hold in list(self.hold_progress.items()):
            note = hold["note"]
            if LANE_KEYS[lane] not in self.held_keys:
                self.hold_progress.pop(lane)
                note.missed = True
                self.record_miss(lane)
                continue
            if now - hold["start"] >= HOLD_DURATION:
                note.hit = True
                self.hold_progress.pop(lane)
                self.grade_counts["PERFECT"] += 1
                self.combo += 1
                self.max_combo = max(self.max_combo, self.combo)
                self.score += 300 * max(1, self.combo // 5)
                lane_x = lane * LANE_W + LANE_W // 2
                self.feedback.append(["PERFECT", (255, 220, 0), 50, lane_x, HIT_Y - 30])
                self.hit_sounds["PERFECT"].play()

    def update(self):
        if self.game_over:
            return
        self.update_hold_notes()
        self.frame += 1

        now = pygame.time.get_ticks()
        if now - self.last_spawn_time >= self.beat_interval_ms:
            self.spawn_note()
            self.last_spawn_time += int(self.beat_interval_ms)
            if now - self.last_spawn_time >= self.beat_interval_ms:
                self.last_spawn_time = now

        if self.frame % 600 == 0:
            self.speed = min(10, self.speed + 0.5)

        active_holds = {id(hold["note"]) for hold in self.hold_progress.values()}
        for note in self.notes:
            if note.hit or note.missed or id(note) in active_holds:
                continue
            note.update()
            if note.y > HIT_Y + HIT_WINDOW + Note.HEIGHT:
                note.missed = True
                self.record_miss()

        self.notes = [
            note for note in self.notes
            if not (note.hit or (note.missed and note.y > HEIGHT + 10))
        ]
        self.feedback = [
            [text, color, ttl - 1, x, y]
            for text, color, ttl, x, y in self.feedback if ttl > 1
        ]
        if self.misses >= 15 and not self.hold_progress:
            self.game_over = True

    def draw(self):
        self.screen.fill(BG)
        for i in range(LANES + 1):
            pygame.draw.line(self.screen, (40, 40, 60),
                             (i * LANE_W, 0), (i * LANE_W, HEIGHT), 1)
        pygame.draw.line(self.screen, (80, 80, 100),
                         (0, HIT_Y), (WIDTH, HIT_Y), 2)

        for i in range(LANES):
            lane_x = i * LANE_W + LANE_W // 2
            pygame.draw.rect(
                self.screen, LANE_COLORS[i],
                pygame.Rect(lane_x - Note.WIDTH // 2, HIT_Y - 12, Note.WIDTH, 24),
                border_radius=6
            )
            label = self.font.render(LANE_LABELS[i], True, (20, 20, 20))
            self.screen.blit(label, (lane_x - label.get_width() // 2, HIT_Y - 10))

        for note in self.notes:
            if note.hit:
                continue
            lane_x = note.lane * LANE_W + LANE_W // 2
            pygame.draw.rect(self.screen, LANE_COLORS[note.lane],
                             note.get_rect(lane_x), border_radius=5)

        for text, color, ttl, x, y in self.feedback:
            surface = self.font.render(text, True, color)
            surface.set_alpha(min(255, ttl * 7))
            self.screen.blit(surface, (x - surface.get_width() // 2, y))

        score_text = self.font.render(f"Score: {self.score}", True, (220, 220, 220))
        combo_text = self.font.render(f"Combo: {self.combo}x", True, (255, 220, 80))
        miss_text = self.font.render(f"Misses: {self.misses}/15", True, (220, 100, 100))
        bpm_text = self.font.render(f"BPM: {self.bpm}", True, (160, 190, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(combo_text, (10, 38))
        self.screen.blit(miss_text, (WIDTH - miss_text.get_width() - 10, 10))
        self.screen.blit(bpm_text, (10, 66))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            self.screen.blit(overlay, (0, 0))
            message = self.big_font.render("GAME OVER", True, (220, 60, 60))
            self.screen.blit(message, (WIDTH // 2 - message.get_width() // 2, 105))
            title = self.font.render("GRADE SUMMARY", True, (255, 220, 80))
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 165))

            rows = [
                ("PERFECT", self.grade_counts["PERFECT"], (255, 220, 0)),
                ("GREAT", self.grade_counts["GREAT"], (100, 220, 100)),
                ("OK", self.grade_counts["OK"], (180, 180, 255)),
                ("MISS", self.grade_counts["MISS"], (220, 80, 80)),
            ]
            y = 205
            for label, count, color in rows:
                row = self.font.render(f"{label}: {count}", True, color)
                self.screen.blit(row, (WIDTH // 2 - row.get_width() // 2, y))
                y += 32

            total = sum(self.grade_counts.values())
            successful = (self.grade_counts["PERFECT"]
                          + self.grade_counts["GREAT"]
                          + self.grade_counts["OK"])
            accuracy = 100.0 * successful / total if total else 0.0
            accuracy_text = self.font.render(
                f"Accuracy: {accuracy:.1f}%", True, (220, 220, 220)
            )
            final_score = self.font.render(
                f"Score: {self.score} | Max Combo: {self.max_combo}x",
                True, (200, 200, 200)
            )
            restart = self.font.render("Press R to Restart", True, (160, 160, 160))
            self.screen.blit(accuracy_text, (WIDTH // 2 - accuracy_text.get_width() // 2, 350))
            self.screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 390))
            self.screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 445))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()