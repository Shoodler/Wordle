import random
import pygame as pg
from pathlib import Path

#Loading files-------------------------------------

def load_dict(file_name):
    file_path = Path(__file__).parent / "Library" / file_name

    with open (file_path, 'r') as file:
        words = file.readlines()
        return [word[:5].upper() for word in words]

dictGuesses = load_dict("guesses.txt")
dictAnswers = load_dict("answers.txt")

Answer = random.choice(dictAnswers)
#--------------------------------------------------

#Pygame vars---------------------------------------

Input = ""
Guesses = []
Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
AlphaUnguessed = Alphabet
GameOver = False
GameWin = False

#_________________________
Width = 600
Height = 700

#Margin________________
Margin = 10
MarginT = 100
MarginB = 100
MarginLR = 100

#Colours____________________
Grey = (70,70,80)
Green = (6,214,160)
Yellow = (255,209,102)
White = (255,255,255)

#Modify number of squares___________________________
g = 6 #G is number of guesses.
l = 5 #L is number of letters.  

#_________________________________________
SQSize = ( Width - (l-1)*Margin - 2*MarginLR ) // l

#Functions--------------------------------------------------
def determine_unguessed(guesses):
    guessed_letters = "".join(guesses)
    unguessed_letters = ""
    for letter in Alphabet:
        if letter not in guessed_letters:
            unguessed_letters = unguessed_letters + letter
    return(unguessed_letters)

def determine_color(guess, j):
    letter = guess[j]
    if letter == Answer[j]:
        return Green
    
    elif letter in Answer:
        n_target = Answer.count(letter)
        n_correct = 0
        n_occurance = 0
        for i in range(5):
            if guess[i] == letter:
                if i <= j:
                    n_occurance += 1
                if letter == Answer[i]:
                    n_correct +=1
        if n_target - n_correct - n_occurance >= 0:
            return Yellow

    return Grey

#Animation-----------------------------------------------------------------

pg.init()
pg.font.init()
pg.display.set_caption("Wordle")

#
Font = pg.font.SysFont("free sans bold", SQSize)
FontSmall = pg.font.SysFont("free sans bold", SQSize//2)
#

screen = pg.display.set_mode((Width,Height))

#Animation loop
animating = True
while animating: 

    #background
    screen.fill("white")

    #____________________________________Draw letters_________________
    letters = FontSmall.render(AlphaUnguessed, True, Grey )
    surface = letters.get_rect(center = (Width//2, MarginT//2))
    screen.blit(letters, surface)


    #____________________________________Generating Squares___________
    y = MarginT
    
    for i in range(g): #Change for number of guesses
        x = MarginLR

        for j in range(l):

            #defining sqaure
            square = pg.Rect(x, y, SQSize, SQSize)
            #drawing square
            pg.draw.rect(screen, Grey, square, width=2, border_radius= 4)

            #Draw Previous Guesses
            if i < len(Guesses):
                #colour of current guess
                color = determine_color(Guesses[i], j)
                pg.draw.rect(screen, color, square, border_radius= 4) #No width specified to create filled square
                
                letter = Font.render(Guesses[i][j], True, White) 
                surface = letter.get_rect(center = (x+SQSize//2 , y+SQSize//2))
                screen.blit(letter, surface)

            #Draw Current Guess
            if i == len(Guesses) and j < len(Input):
                letter = Font.render((Input[j]), True, Grey)
                surface = letter.get_rect(center = (x+SQSize//2 , y+SQSize//2))
                screen.blit(letter, surface)

            x += SQSize + Margin
        
        y += SQSize + Margin

    #_________________________________Game Over and display answer_________________

    if len(Guesses) == g and Guesses[l] != Answer:
        GameOver = True
        letters = Font.render(Answer, True, Grey)
        surface = letters.get_rect(center = (Width//2 , Height-MarginB//2-Margin))
        screen.blit(letters, surface)

    #_________________________________Display start_________________________________
    pg.display.flip()
#--------------------------------------------------------------------------

#User Interaction----------------------------------------------------------

    for event in pg.event.get():

        #________________________________________Exit window animation_______________
        if event.type == pg.QUIT:
            animating = False

        #________________________________________User presses button on KB___________
        elif event.type == pg.KEYDOWN:

            #____________________Escape key pressed
            if event.key == pg.K_ESCAPE:
                animating = False

            #_____________________Backspace for corrections
            if event.key == pg.K_BACKSPACE:
                if len(Input) > 0:
                    Input = Input[:len(Input)-1]

            #_____________________Enter key for submission
            elif event.key == pg.K_RETURN:
                if len(Input) == 5 and Input in dictGuesses:
                    Guesses.append(Input)
                    AlphaUnguessed = determine_unguessed(Guesses)

                    print() #DEBUGGING LINE
                    print(f'Accepted input: {Input}') #DEBUGGING LINE
                    print(f'Current List: {Guesses}') #DEBUGGING LINE
                    print() #DEBUGGING LINE

                    GameOver = True  if Input == Answer else False
                    Input = ""

            #____________________Space to restart
            elif event.key == pg.K_SPACE:
                GameOver = False
                GameWin = False
                Answer = random.choice(dictAnswers)
                Guesses = []
                AlphaUnguessed = AlphaUnguessed
                Input = ""

            #Regular Input
            elif len(Input) < 5 and not GameOver:
                Input = Input + event.unicode.upper()

                print(f"Input: {Input}, Valid: {Input.upper() in dictGuesses}")

#___________________________________THANK YOU :3__________________________________________________
#___________________________________SHOODLER 2024_________________________________________________




    