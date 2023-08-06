from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import init, font, display, key, Surface, event, quit, time, QUIT, KEYDOWN, K_BACKSPACE, K_RETURN
from sys import exit
from time import sleep
from easygui import enterbox
from socket import create_connection

login = enterbox('Please enter your username:', 'Login Required')
if (login == 'shivekS151600') or (login == 'vyomS300') or (login == 'gamerPanda_17'):
    pass
else:
    print("You are not allowed to use this program because you aren't registered.")
    sleep(2)
    exit()
local_ip = enterbox("What is the ip?", 'IP Required')
try:
    port = int(enterbox("What is the port?", "Port Required"))
except:
    port = 12345

init()

screen_width, screen_height = screen_size = (640, 640)  # Make the screen taller to fit more messages
font = font.Font(None, 50)
bg_color = (0, 0, 0)
text_color = (255, 255, 255)
space_character_width = 8
message_spacing = 8

# Connect to the server
try:
    connection = create_connection((local_ip, port))
except:
    try:
        connection = create_connection(('localhost', 12345))
    except:
        print("The server is currently not on at this time.")
        sleep(2)
        exit()
print("Please wait for a couple of seconds. The Chat Window should be open by now!")
connection.setblocking(False)
screen = display.set_mode(screen_size)
key.set_repeat(300, 100)

def message_to_surface(message): 
    words = message.split(' ')

    word_surfs = []
    word_locations = []
    word_x = 0
    word_y = 0
    text_height = 0

    for word in words:
        word_surf = font.render(word, True, text_color, bg_color)
        if word_x + word_surf.get_width() > screen_width:
            word_x = 0
            word_y = text_height
        word_surfs.append(word_surf)
        word_locations.append((word_x, word_y))
        word_x += word_surf.get_width() + space_character_width
        if word_y + word_surf.get_height() > text_height:
            text_height = word_y + word_surf.get_height()

    surf = Surface((screen_width, text_height))
    surf.fill(bg_color)
    for i in range(len(words)):
        surf.blit(word_surfs[i], word_locations[i])
    return surf

message_surfs = []

def add_message(message):
    if len(message_surfs) > 50:
        message_surfs.pop(0)
    message_surfs.append(message_to_surface(message))

text_from_socket = b''
def read_from_socket():
    global connection, text_from_socket, running
    try:
        data = connection.recv(2048)
    except BlockingIOError:
        return

    if not data:
        running = False
    for char in data:
        char = bytes([char])
        if char == b'\n':
            add_message(text_from_socket.strip().decode('utf-8'))
            text_from_socket = b''
        else:
            text_from_socket += char

def redraw_screen():
    screen.fill(bg_color)

    typing_surf = message_to_surface("> " + typing_text)
    y = screen_height - typing_surf.get_height()
    screen.blit(typing_surf, (0, y))

    message_index = len(message_surfs) - 1
    while y > 0 and message_index >= 0:
        message_surf = message_surfs[message_index]
        message_index -= 1
        y -= message_surf.get_height() + message_spacing
        screen.blit(message_surf, (0, y))
    display.flip()


running = True
typing_text = ""
clock = time.Clock()
notifications = 0

while running:
    clock.tick(60)
    for events in event.get():
        if events.type == QUIT:
            running = False
        elif events.type == KEYDOWN:
            if events.key == K_BACKSPACE:
                if typing_text:
                    typing_text = typing_text[:-1]
            elif events.key == K_RETURN:
                add_message('You: ' + typing_text)
                connection.send(typing_text.encode('utf-8') + b"\r\n")
                typing_text = ""
        
            else:
                typing_text += events.unicode

    read_from_socket()
    redraw_screen()

quit()
connection.close()
