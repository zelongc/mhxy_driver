import cv2
import numpy as np
import pyautogui


screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()


pyautogui.moveTo(700,414)
pyautogui.scroll(-8)
