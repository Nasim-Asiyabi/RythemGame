import pygame  # pyright: ignore[reportMissingImports]
import random  
import sys  
import os  

# ============================================
# INITIALIZATION SECTION
# ============================================

pygame.init()
pygame.font.init()

# ============================================
# SCREEN CONFIGURATION
# ============================================

SCREEN_WIDTH = 810
SCREEN_HEIGHT = 620

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Master")

# COLOR DEFINITIONS
# ===========================================

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)  
COLOR_GRAY = (50, 50, 50)  
COLOR_RED = (255, 60, 60) 
COLOR_GREEN = (50, 255, 100)  
COLOR_BLUE = (50, 200, 225)  
COLOR_YELLOW = (255, 220, 0) 
COLOR_PURPLE = (180, 50, 255) 

# ============================================
# GAME CONSTANTS
# ============================================

FPS = 60  
LANE_WIDTH = 110 
HIT_Y = 500 
START_X = (SCREEN_WIDTH - (4 * LANE_WIDTH)) // 2

# ============================================
# KEY MAPPINGS
# ============================================

KEYS_MAPPING = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
KEYS_TEXT = ['d', 'f', 'j', 'k'] 

# ============================================
# FONT INITIALIZATION
# ============================================

font_large = pygame.font.SysFont("Arial", 49, bold=True)
font_medium = pygame.font.SysFont("Arial", 30)
font_small = pygame.font.SysFont("Arial", 21)

# ============================================
# HELPER FUNCTIONS
# ============================================

def clamp(value, min_value, max_value):
    """محدود کردن مقدار بین دو عدد"""
    return max(min_value, min(value, max_value))

def format_score(score):
    """فرمت کردن امتیاز با کاما"""
    return f"{score:,}"

def get_color_by_combo(combo):
    """گرفتن رنگ بر اساس کومبو"""
    if combo >= 50:
        return COLOR_PURPLE
    elif combo >= 25:
        return COLOR_YELLOW
    elif combo >= 10:
        return COLOR_GREEN
    else:
        return COLOR_WHITE

# ============================================
# NOTE CLASS
# ============================================

class Note:
    """کلاس نت - نوت‌هایی که از بالا می‌آیند"""

    def __init__(self, lane_idx):
        """سازنده کلاس Note"""
        self.lane = lane_idx
        self.x = START_X + (lane_idx * LANE_WIDTH) + 10
        self.y = -60
        self.width = LANE_WIDTH - 20 
        self.height = 40 
        self.active = True 
        self.create_time = pygame.time.get_ticks()

    def move(self, speed):
        """حرکت نت به سمت پایین"""
        self.y += speed 

    def get_rect(self):
        """گرفتن مستطیل برخورد نت"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        """رسم نت روی پنجره"""
        if self.active: 
            pygame.draw.rect(window, COLOR_BLUE, (self.x, self.y, self.width, self.height), border_radius=8)
            pygame.draw.rect(window, COLOR_WHITE, (self.x, self.y, self.width, self.height), 2, border_radius=8)

    def is_off_screen(self):
        """بررسی خارج شدن از صفحه"""
        return self.y > SCREEN_HEIGHT

# ============================================
# RHYTHM GAME CLASS
# ============================================

class RhythmGame:
    """کلاس اصلی بازی ریتم"""

    def __init__(self):
        """سازنده کلاس بازی"""
        self.clock = pygame.time.Clock()
        self.is_running = True 
        self.state = "MENU"  # MENU, PLAYING, GAMEOVER
        self.highscore_file = "highscore_data.txt"
        self.high_score = self.load_record()
        self.reset_variables()

    # ========================================
    # FILE HANDLING METHODS
    # ========================================

    def load_record(self):
        """بارگذاری رکورد از فایل"""
        if os.path.exists(self.highscore_file):
            try:
                with open(self.highscore_file, "r") as f:
                    return int(f.read())  
            except:
                return 0
        return 0

    def save_record(self):
        """ذخیره رکورد در فایل"""
        if self.score > self.high_score:
            self.high_score = self.score
            with open(self.highscore_file, "w") as f:
                f.write(str(self.high_score))

    # ========================================
    # GAME STATE METHODS
    # ========================================

    def reset_variables(self):
        """بازنشانی متغیرهای بازی"""
        self.notes_list = []
        self.score = 0 
        self.combo = 0  
        self.health = 100 
        self.base_speed = 2.5 
        self.current_speed = self.base_speed
        self.spawn_timer = 0
        self.spawn_rate = 60
        self.feedback_text = ""
        self.feedback_timer = 0 
        self.total_notes_hit = 0
        self.perfect_count = 0
        self.good_count = 0
        self.ok_count = 0
        self.miss_count = 0

    def check_difficulty(self):
        """بررسی و تنظیم سختی بازی بر اساس امتیاز"""
        level = self.score // 50
        new_speed = self.base_speed + (level * 0.5)

        if new_speed > 12:
            self.current_speed = 12
        else:
            self.current_speed = new_speed

    # ========================================
    # COLLISION HANDLING
    # ========================================

    def handle_collision(self, lane_index):
        """مدیریت برخورد با نت‌ها"""
        hit_detected = False

        for note in self.notes_list:
            if note.lane == lane_index and note.active:
                diff = abs(note.y - HIT_Y)

                if diff < 50:
                    note.active = False 
                    hit_detected = True
                    self.total_notes_hit += 1

                    if diff < 15:
                        self.score += 20
                        self.health = min(100, self.health + 2)
                        self.feedback_text = "PERFECT!"
                        self.feedback_timer = 30
                        self.perfect_count += 1

                    elif diff < 30:
                        self.score += 10
                        self.health = min(100, self.health + 1)
                        self.feedback_text = "GOOD"
                        self.feedback_timer = 30
                        self.good_count += 1

                    else:
                        self.score += 5
                        self.feedback_text = "OK"
                        self.feedback_timer = 30
                        self.ok_count += 1

                    self.combo += 1  
                    self.check_difficulty()  
                    break 

        if not hit_detected:
            self.combo = 0  
            self.health -= 5  
            self.feedback_text = "MISS"
            self.feedback_timer = 30
            self.miss_count += 1

    # ========================================
    # EVENT HANDLING
    # ========================================

    def handle_events(self):
        """مدیریت رویدادهای ورودی"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_record()  
                self.is_running = False 
                pygame.quit()  
                sys.exit() 

            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_RETURN: 
                        self.reset_variables()
                        self.state = "PLAYING"
                        
                elif self.state == "GAMEOVER":
                    if event.key == pygame.K_r:
                        self.reset_variables()
                        self.state = "PLAYING"
                    elif event.key == pygame.K_ESCAPE:
                        self.save_record()
                        self.is_running = False
                        
                elif self.state == "PLAYING":
                    if event.key in KEYS_MAPPING:
                        idx = KEYS_MAPPING.index(event.key)
                        self.handle_collision(idx)

    # ========================================
    # GAME LOGIC UPDATE
    # ========================================

    def update_logic(self):
        """به‌روزرسانی منطق بازی"""
        if self.state == "PLAYING":
            self.spawn_timer += 1
            threshold = self.spawn_rate / (self.current_speed / 3)

            if self.spawn_timer > threshold:
                rand_lane = random.randint(0, 3)  
                self.notes_list.append(Note(rand_lane))  
                self.spawn_timer = 0
                self.spawn_rate = random.randint(40, 90)  

            for note in self.notes_list:
                note.move(self.current_speed)

                if note.is_off_screen():
                    if note.active:
                        note.active = False
                        self.combo = 0
                        self.health -= 10
                        self.feedback_text = "MISS"
                        self.feedback_timer = 30
                        self.miss_count += 1

            self.notes_list = [n for n in self.notes_list if n.active]

            if self.feedback_timer > 0:
                self.feedback_timer -= 1

            if self.health <= 0:
                self.save_record()
                self.state = "GAMEOVER"

            self.health = clamp(self.health, 0, 100)

    # ========================================
    # DRAWING METHODS
    # ========================================

    def draw_lanes(self):
        """رسم خطوط لاین‌ها"""
        for i in range(4):
            x = START_X + (i * LANE_WIDTH)
            pygame.draw.rect(screen, COLOR_GRAY, (x, 0, LANE_WIDTH, SCREEN_HEIGHT), 1)

            keys = pygame.key.get_pressed()
            btn_color = COLOR_WHITE
            if keys[KEYS_MAPPING[i]]:
                btn_color = COLOR_GRAY  

            pygame.draw.rect(screen, btn_color, (x + 10, HIT_Y, LANE_WIDTH - 20, 40), 2, border_radius=5)
            txt = font_small.render(KEYS_TEXT[i], True, COLOR_WHITE)
            screen.blit(txt, (x + 45, HIT_Y + 50))

        pygame.draw.line(screen, COLOR_RED, (START_X, HIT_Y + 20), (START_X + 4 * LANE_WIDTH, HIT_Y + 20), 2)

    def draw_hud(self):
        """رسم رابط کاربری (امتیاز، کومبو و...)"""
        score_surf = font_medium.render(f"Score: {format_score(self.score)}", True, COLOR_WHITE)
        combo_surf = font_large.render(f"Combo: {self.combo}", True, get_color_by_combo(self.combo))
        speed_surf = font_small.render(f"Speed: {self.current_speed:.1f}", True, COLOR_GRAY)
        best_surf = font_small.render(f"Best: {format_score(self.high_score)}", True, COLOR_PURPLE)

        screen.blit(score_surf, (20, 20))
        screen.blit(best_surf, (20, 60))
        screen.blit(speed_surf, (20, 90))
        screen.blit(combo_surf, (20, 130))

    def draw_health_bar(self):
        """رسم نوار سلامتی"""
        pygame.draw.rect(screen, COLOR_RED, (SCREEN_WIDTH - 220, 20, 200, 25))
        pygame.draw.rect(screen, COLOR_GREEN, (SCREEN_WIDTH - 220, 20, 2 * self.health, 25))
        pygame.draw.rect(screen, COLOR_WHITE, (SCREEN_WIDTH - 220, 20, 200, 25), 2)

    def draw_feedback(self):
        """رسم بازخورد ضربه (PERFECT, GOOD, ...)"""
        if self.feedback_timer > 0:
            if "PERFECT" in self.feedback_text:
                fb_color = COLOR_GREEN
            elif "GOOD" in self.feedback_text:
                fb_color = COLOR_YELLOW
            else:
                fb_color = COLOR_RED

            fb_surf = font_large.render(self.feedback_text, True, fb_color)
            screen.blit(fb_surf, (SCREEN_WIDTH // 2 - fb_surf.get_width() // 2, SCREEN_HEIGHT // 2))

    def draw_menu(self):
        """رسم صفحه منو"""
        title = font_large.render("RHYTHM GAME", True, COLOR_BLUE)
        sub = font_medium.render("Press ENTER to Start", True, COLOR_WHITE)
        record = font_medium.render(f"High Score: {format_score(self.high_score)}", True, COLOR_PURPLE)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 300))
        screen.blit(record, (SCREEN_WIDTH // 2 - record.get_width() // 2, 400))

    def draw_game_over(self):
        """رسم صفحه پایان بازی"""
        over_txt = font_large.render("GAME OVER", True, COLOR_RED)
        score_txt = font_medium.render(f"Final Score: {format_score(self.score)}", True, COLOR_WHITE)
        retry_txt = font_medium.render("Press 'R' to Retry", True, COLOR_GREEN)
        
        perfect_txt = font_small.render(f"Perfect: {self.perfect_count}", True, COLOR_GREEN)
        good_txt = font_small.render(f"Good: {self.good_count}", True, COLOR_YELLOW)
        ok_txt = font_small.render(f"OK: {self.ok_count}", True, COLOR_BLUE)
        miss_txt = font_small.render(f"Miss: {self.miss_count}", True, COLOR_RED)

        screen.blit(over_txt, (SCREEN_WIDTH // 2 - over_txt.get_width() // 2, 100))
        screen.blit(score_txt, (SCREEN_WIDTH // 2 - score_txt.get_width() // 2, 200))
        
        screen.blit(perfect_txt, (SCREEN_WIDTH // 2 - 120, 280))
        screen.blit(good_txt, (SCREEN_WIDTH // 2 - 120, 310))
        screen.blit(ok_txt, (SCREEN_WIDTH // 2 - 120, 340))
        screen.blit(miss_txt, (SCREEN_WIDTH // 2 - 120, 370))
        
        screen.blit(retry_txt, (SCREEN_WIDTH // 2 - retry_txt.get_width() // 2, 450))

    def draw_playing(self):
        """رسم صفحه بازی در حال اجرا"""
        self.draw_lanes()
        
        for note in self.notes_list:
            note.draw(screen)

        self.draw_hud()
        self.draw_feedback()
        self.draw_health_bar()

    def draw(self):
        """رسم اصلی - توزیع بین صفحه‌های مختلف"""
        screen.fill(COLOR_BLACK)

        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "PLAYING":
            self.draw_playing()
        elif self.state == "GAMEOVER":
            self.draw_game_over()

        pygame.display.update()

    # ========================================
    # MAIN GAME LOOP
    # ========================================

    def run(self):
        """حلقه اصلی بازی"""
        while self.is_running:
            self.handle_events()
            self.update_logic()
            self.draw()
            self.clock.tick(FPS)


# ============================================
# PROGRAM ENTRY POINT
# ============================================

if __name__ == "__main__":
    game = RhythmGame()
    game.run()