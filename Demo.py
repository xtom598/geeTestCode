#! python3
# coding:utf-8

import time,random
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s')

phoneNum = '13456788765'
# initial offset
initial_offset = 10
URLs = ['https://biaodan.info/q/7sisis']

#TODO get html elements
def sendPhone(driver, phoneNum, phoneInputClass, sendPhoneButtonId):
  # driver = webdriver.Chrome()
  logging.debug('Send Phone Start')
  phoneInput = driver.find_element_by_class_name(phoneInputClass)
  phoneInput.send_keys(phoneNum)
  time.sleep(2)
  sendBtn = driver.find_element_by_id(sendPhoneButtonId)
  sendBtn.click()
  time.sleep(5)

#TODO compare Captcha & return tarck
def elementsScreenshot(driver, bgImgClass, dragBallClass):
  # driver = webdriver.Chrome()
  logging.debug('start make background screenshot')
  driver.find_element_by_class_name(bgImgClass).screenshot('bg_full.png')
  time.sleep(2)
  ball = driver.find_element_by_class_name(dragBallClass)
  ActionChains(driver).click_and_hold(ball).perform()
  ActionChains(driver).move_by_offset(190, 0).perform()
  # move the ball to right
  # this is important
  time.sleep(0.5)
  driver.find_element_by_class_name(bgImgClass).screenshot('cut.png')
  # move the ball to left
  ActionChains(driver).move_by_offset(-30, 0).perform()
  time.sleep(1)
  ActionChains(driver).move_by_offset(-50, 0).perform()
  time.sleep(1)
  ActionChains(driver).move_by_offset(-40, 0).perform()
  time.sleep(1)
  ActionChains(driver).move_by_offset(-30, 0).perform()
  time.sleep(1)
  ActionChains(driver).move_by_offset(-40, 0).perform()

def dragBall(driver, track, dragBallClass):
  ball = driver.find_element_by_class_name(dragBallClass)
  logging.debug('ball start move')
  # simulate human's behave
  while track:
    len = random.choice(track)
    ActionChains(driver).move_by_offset(len, 0).perform()
    track.remove(len)
    logging.debug(track)
    time.sleep(len/10)
  imitate2L = ActionChains(driver).move_by_offset(-2, 0)
  imitateL = ActionChains(driver).move_by_offset(-1, 0)
  time.sleep(0.015)
  imitate2L.perform()
  time.sleep(0.04)
  imitateL.perform()
  time.sleep(0.04)
  imitate2L.perform()
  time.sleep(0.04)
  imitateL.perform()
  time.sleep(0.04)
  imitate2L.perform()
  ActionChains(driver).pause(random.randint(6, 10) / 10).release(ball).perform()

def getTrack(distance):
  logging.debug('calcute distance track')
  # simulate human's hebace s = 1 / 2 a t t
  track =[]
  current = 0
  mid = distance * 3 / 4
  t = random.randint(2, 3) / 10
  v = 0
  logging.debug('1')
  while current < distance:
    if current < mid:
      a = 2
    else:
      a = -3
    v0 = v
    v = v0 + a * t
    move = v0 * t + 1 / 2 * a * t * t
    current += move
    track.append(round(move))
    logging.debug(track)
  return track

# TODO compare two img
def compareImg(img1, img2, x, y):
  logging.debug('compare img start')
  pix1 = img1.load()[x, y]
  pix2 = img2.load()[x, y]
  threshold = 60
  if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(pix1[2] - pix2[2] < threshold)):
    return True
  else:
    return False

def getOffset(bgFullPath, bgPath):
  logging.debug('get img offset')
  bg_full = Image.open(bgFullPath)
  bg = Image.open(bgPath)
  left = initial_offset
  for width in range(left, bg_full.size[0]):
    for height in range(bg_full.size[1]):
      if not compareImg(bg_full, bg, width, height):
        left = width
        return left
  return left
#TODO execute Crack it

def main(driver):
  logging.debug('main() start')
  for url in URLs:
    driver.get(url)
    logging.debug('%s get html', url)
    time.sleep(3)
    sendPhone(driver, phoneNum, 'filter-input', 'btnSendCode')
    elementsScreenshot(driver, 'gt_cut_fullbg', 'gt_slider_knob')
    distance = getOffset('bg_full.png', 'cut.png')
    # logging.debug('%s',distance)
    track = getTrack(distance)
    dragBall(driver, track, 'gt_slider_knob')
    time.sleep(3)

if __name__ == '__main__':
  driver = webdriver.Chrome()
  for i in range(1, 2):
    logging.debug('%s Test', i)
    try:
      main(driver)
    except:
      print("%d Error", i)
      pass
  driver.close()
  driver.quit()

