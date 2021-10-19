import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from utlis import *
import sudukoSolver
import cv2
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.core.window import Window
import numpy as np
import human

cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop)
ret,frame = cap.read() # return a single frame in variable `frame`

while(True):
    cv2.imshow('img1',frame) #display the captured image
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y'
        cv2.imwrite("C:/Users/s.simon.arnold3/PycharmProjects/finaleuooo/img.png",frame)
        cv2.destroyAllWindows()
        break

cap.release()

########################################################################
pathImage = "img_2.png"
heightImg = 450
widthImg = 450
model = intializePredectionModel()  # LOAD THE CNN MODEL
########################################################################
n = 0


def add():
    global n
    if n > 100:
        n = n + 1

Config.set('graphics', 'resizable', True)

class App(App):
    def build(self):
        # returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.9)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        Window.size = (450, 600)

        # label widget
        self.place = Label(
            text="Sudoku",
            font_size=48,
            color="#ff00ff"
        )
        self.window.add_widget(self.place)

        self.window.add_widget(Image(source="imgDetectedDigits.png", size_hint= (None,None), size = (400, 400), allow_stretch=True))

        # button widget
        self.button1 = Button(
            text="Sudoku lösen?",
            size_hint=(0.1, 0.5),
            bold=True,
            background_color='#00FFCE',
            # remove darker overlay of background colour
            # background_normal = ""
        )
        self.button1.bind(on_press=self.correct)

        self.button2 = Button(
            text="falsch",
            size_hint=(0.1, 0.5),
            bold=True,
            background_color='#00FFCE',
            # remove darker overlay of background colour
            # background_normal = ""
        )
        self.button2.bind(on_press=self.false)

        self.button3 = Button(
            text="correct",
            size_hint=(0.1, 0.5),
            bold=True,
            background_color='#00FFCE',
        )
        self.button3.bind(on_press=self.new_numb)

        self.window.add_widget(self.button1)
        self.window.add_widget(self.button2)

        return self.window

    def correct(self, instance):
        self.window.clear_widgets()
        inf_perspec()
        self.window.add_widget(Image(source="inv_perspective.png", size_hint= (None,None), size = (400, 400), allow_stretch=True))
        self.place = Label(
            text="Congratulations!",
            font_size=48,
            color="#ff00ff"
        )
        self.window.add_widget(self.place)

    def false(self, instance):
        self.window.clear_widgets()
        self.window.add_widget(Image(source="imgDetectedDigits.png", size_hint= (None,None), size = (400, 400), allow_stretch=True))

        # self.place.text = "row, col, new number"
        self.user_row = TextInput(multiline=False, input_type="number")
        self.user_col = TextInput(multiline=False, input_type="number")
        self.user_numb = TextInput(multiline=False, input_type="number")
        self.window.add_widget(self.user_row)
        self.window.add_widget(self.user_col)
        self.window.add_widget(self.user_numb)
        self.window.add_widget(self.button3)

    def false2(self, instance):
        self.window.clear_widgets()
        self.window.add_widget(Image(source="imgSolvedDigits.png", size_hint= (None,None), size = (400, 400), allow_stretch=True))

        # self.place.text = "row, col, new number"
        self.user_row = TextInput(multiline=False, size_hint=(0.05, 0.5), input_type="number")
        self.user_col = TextInput(multiline=False, size_hint=(0.05, 0.5), input_type="number")
        self.user_numb = TextInput(multiline=False, size_hint=(0.05, 0.5), input_type="number")
        self.window.add_widget(self.user_row)
        self.window.add_widget(self.user_col)
        self.window.add_widget(self.user_numb)
        self.window.add_widget(self.button3)

    def new_numb(self, instance):
        self.window.clear_widgets()
        i = self.user_row.text
        j = self.user_col.text
        new = self.user_numb.text
        correct_cell(i, j, new, board)
        self.window.add_widget(Image(source="imgSolvedDigits.png", size_hint= (None,None), size = (400, 400), allow_stretch=True))
        # button widget
        self.button1 = Button(
            text="Sudoku lösen?",
            size_hint=(0.1, 0.5),
            bold=True,
            background_color='#00FFCE',
        )
        self.button1.bind(on_press=self.correct)

        self.button2 = Button(
            text="falsch",
            size_hint=(0.1, 0.5),
            bold=True,
            background_color='#00FFCE',
            # remove darker overlay of background colour
            # background_normal = ""
        )
        self.button2.bind(on_press=self.false2)

        self.window.add_widget(self.button1)
        self.window.add_widget(self.button2)


def create_newimg(bo):
    flatList = []
    imgdet = imgBlank.copy()
    for sublist in bo:
        for item in sublist:
            flatList.append(item)
    solvedNumbers = flatList
    imgdet = displayNumbers(imgdet, solvedNumbers)
    imgdet = drawGrid(imgdet)
    try:
        os.remove("imgSolvedDigits.png")
        cv2.imwrite("imgSolvedDigits.png", imgdet)
    except:
        cv2.imwrite("imgSolvedDigits.png", imgdet)


def correct_cell(i, j, new, bo):
    i = int(float(i))
    j = int(j)
    bo[i][j] = int(new)
    create_newimg(bo)


#### 5. FIND SOLUTION OF THE BOARD
def inf_perspec():
    board = np.array_split(numbers, 9)
    human.solve(board)
    flatList = []
    for sublist in board:
        for item in sublist:
            flatList.append(item)
    solvedNumbers = flatList * posArray
    imgSolvedDigits = imgBlank.copy()
    imgSolvedDigits = displayNumbers(imgSolvedDigits, solvedNumbers)
    imgInvWarpColored = img.copy()
    imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (widthImg, heightImg))
    inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
    cv2.imwrite("C:/Users/s.simon.arnold3/PycharmProjects/finaleuooo/inv_perspective.png", inv_perspective)

#### 1. PREPARE THE IMAGE
img = cv2.imread(pathImage)
img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
imgThreshold = preProcess(img)

# #### 2. FIND ALL COUNTOURS
imgContours = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
imgBigContour = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)  # DRAW ALL DETECTED CONTOURS

#### 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
biggest, maxArea = biggestContour(contours)  # FIND THE BIGGEST CONTOUR
if biggest.size != 0:
    biggest = reorder(biggest)
    cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25)  # DRAW THE BIGGEST CONTOUR
    pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    imgDetectedDigits = imgBlank.copy()
    imgWarpColored = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)

    #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
    imgSolvedDigits = imgBlank.copy()
    boxes = splitBoxes(imgWarpColored)
    # cv2.imshow("Sample",boxes[65])
    numbers = getPredection(boxes, model)
    # print(numbers)
    imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
    numbers = np.asarray(numbers)
    board = np.array_split(numbers, 9)
    posArray = np.where(numbers > 0, 0, 1)
    # print(posArray)



    # #### 6. OVERLAY SOLUTION
    pts2 = np.float32(biggest)  # PREPARE POINTS FOR
    pts1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
    imgInvWarpColored = img.copy()
    imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (widthImg, heightImg))
    inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
    imgDetectedDigits = drawGrid(imgDetectedDigits)
    cv2.imwrite("C:/Users/s.simon.arnold3/PycharmProjects/finaleuooo/imgDetectedDigits.png", imgDetectedDigits)
    imgSolvedDigits = drawGrid(imgSolvedDigits)

    imageArray = ([img, imgThreshold, imgContours, imgBigContour],
                  [imgDetectedDigits, imgSolvedDigits, imgInvWarpColored, inv_perspective])
    stackedImage = stackImages(imageArray, 1)

    cv2.imwrite("C:/Users/s.simon.arnold3/PycharmProjects/finaleuooo/inv_perspective.png", inv_perspective)


    if __name__ == "__main__":
        App().run()

else:
    print("No Sudoku Found")

cv2.waitKey(0)
