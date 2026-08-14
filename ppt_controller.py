# ppt_controller.py
import win32com.client
import re
from rapidfuzz import fuzz


def connect_to_powerpoint():
    try:
        app = win32com.client.GetActiveObject("PowerPoint.Application")
        return app
    except Exception:
        print("PowerPoint is not available ... ")
        return None


def get_slideshow_view(app):

    if app is None:
        return None
    if app.SlideShowWindows.Count == 0:
        print("no slide_show is running ... ")
        return None
    return app.SlideShowWindows(1).View



def next_slide(app):
    view = get_slideshow_view(app)
    if view:
        view.Next()
        print(f"next slide: {view.CurrentShowPosition}")


def previous_slide(app):
    view = get_slideshow_view(app)
    if view:
        view.Previous()
        print(f"previoos slide:  {view.CurrentShowPosition}")


def goto_slide(app, slide_number):
    view = get_slideshow_view(app)
    if view:
        try:
            view.GotoSlide(slide_number)
            print(f"go to slide:  {slide_number}")
        except Exception:
            print(f"number {slide_number} is not available ... ")


def start_slideshow(app):
    if app is None:
        return None
    if app.Presentations.Count == 0:
        print("no slide_show is running ... ")
        return None
    app.Presentations(1).SlideShowSettings.Run()
    print("slide show started ... ")


def end_slideshow(app):
    if app is None:
        return None
    if app.SlideShowWindows.Count > 0:
        app.SlideShowWindows(1).View.Exit()
        print("slide show ended ... ")


NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20,
}


def extract_slide_number(text):

    digit_match = re.search(r"\d+", text)
    if digit_match:
        return int(digit_match.group())

    words = text.lower().split()
    for word in words:
        if word in NUMBER_WORDS:
            return NUMBER_WORDS[word]

    return None



COMMAND_PATTERNS = {
    "next": ["next slide", "next page"],
    "previous": ["previous slide", "previous page", "back", "go back"],
    "goto": ["go to slide", "go to page"],
    "start": ["start", "start slideshow", "begin"],
    "end": ["end", "end slideshow", "stop", "exit"],
}


def match_command(text, threshold=65):

    if not text:
        return None

    best_command = None
    best_score = 0

    for command_name, patterns in COMMAND_PATTERNS.items():
        for pattern in patterns:
            score = fuzz.partial_ratio(pattern.lower(), text.lower())
            if score > best_score:
                best_score = score
                best_command = command_name

    if best_score >= threshold:
        return best_command, best_score
    return None, best_score


def execute_command(app, text):

    command_name, score = match_command(text)

    if command_name is None:
        print(f'unavailable command: {text} , score: {score}')
        return

    print(f'command: {command_name}')

    if command_name == "next":
        next_slide(app)
    elif command_name == "previous":
        previous_slide(app)
    elif command_name == "goto":
        slide_num = extract_slide_number(text)
        if slide_num is not None:
            goto_slide(app, slide_num)
        else:
            print(" this number is not available ... ")
    elif command_name == "start":
        start_slideshow(app)
    elif command_name == "end":
        end_slideshow(app)


## for program test
# app = connect_to_powerpoint()
# execute_command(app , 'next slide please')