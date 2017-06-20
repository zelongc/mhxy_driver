#!/usr/bin/python
# -*- coding: <encoding name> -*-

# Author: Zelong Cong
#         Univeristy of Melbourne
# Date:   20 June, 2017

# Notice:  This python scripts contains a few Chinese tokens specifing the relationships between
#          the variables and actual options in the Game.


import cv2
import numpy as np
from PIL import ImageGrab
import time
import pyautogui

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()


# capture the current game window when called.

window_TL = (301.0, 114.973, 1139.57, 763.9)    # window top left

status=0
"""
0 stands for Normal mode
1 stands for Battle mode
2 stands for Speical mode
"""

status_pool=('./icons/attack.png')   #   when found an attack icon. means in a battle mode



fixed_action_pool={'activity':(250,26),
                   'daily_activity':(108,157)}


bangpai_pool=(
    './icons/claim_bangpai_task.png',  # "领取帮派任务" 在帮派里
    './icons/qiecuo.png',  # "切磋"
    './icons/goumai.png',  # "购买"
    './icons/goumai2.png',  # 购买2
    './icons/bangpai_task.png',  # "帮派任务"     帮派任务触发战斗
    './icons/shiyong.png',  # "使用"
    './icons/jinruzhandou.png',  # "进入战斗"
    './icons/shangjiao.png',  # "上交"

    './icons/qinglong_task.png',
    './icons/zhuque_task.png',  # 任务栏最后点  Tasks block comes as last!
    './icons/xuanwu_task.png'
)

shimen_pool=(
              './icons/goumai.png',                    # "购买"
              './icons/goumai2.png',                   # "购买2"
              './icons/qiecuo.png',                    # "切磋"
              './icons/shangjiao.png',                  # "上交"
              './icons/shiyong.png',                    # "使用"
              './icons/jinruzhandou.png',               # "进入战斗"
              './icons/shimenrenwu.png' ,               # "师门任务"


              './icons/shimen_task.png',
              './icons/goumai.png',

              )


actions_pool=('./icons/claim_bangpai_task.png',        # "领取帮派任务" 在帮派里
              './icons/bangpai_task.png' ,             # "帮派任务"     帮派任务触发战斗
              './icons/goumai.png',                    # "购买"
              './icons/qiecuo.png',                    # "切磋"
              './icons/shangjiao.png',                 # "上交"
              './icons/shiyong.png',                   # "使用"
              './icons/jinruzhandou.png',              # "进入战斗"
              './icons/shimenrenwu.png' ,              # "师门任务"

              './icons/goumai.png',                    # 购买2
              './icons/shimen_task.png',
              './icons/qinglong_task.png',
              './icons/zhuque_task.png'            # 任务栏最后点  Tasks block comes as last!
              )

mijingxiangyao_pool=(
              './icons/mijingxiangyao.png',        # 点击 "秘境降妖"
              './icons/tiaozhan.png',              # 点击 '挑战'
              './icons/mijingxiangyao_task.png',   # 点击 '秘境降妖' 任务栏
              './icons/mijingxiangyao_pig.png',    # 点击 '动物头像'
              './icons/zaicitiaozhan.png',         # "再次挑战"
              './icons/shibai.png',                 # "失败"
              './icons/gift.png'
)

zhuogui_pool=(
                './icons/zidongpipei.png' ,         # 自动匹配
                # './icons/activity.png' ,            # 活动图片
                # './icons/'
)



def grab_game_window():

    time.sleep(2)


    # grab current screen with full resolution
                #   x1    y1      x2       y2   (topleft-x,y,  bottom-right x,y)

    snipshot=ImageGrab.grab(window_TL)     # catch the area of gaming area
    img_np=np.array(snipshot)    # convert the screenshot to numpy
    game_window = cv2.cvtColor(img_np,cv2.COLOR_BGR2RGB)
    return game_window


# match image and return location
def match_image(source,template, threshold=0.8):

    #both images should be in gray-scale
    res = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(res >= threshold)

    for x, y in zip(*loc[::-1]):
        return x, y
    return None



def click_action(x,y,click_num=1):
    x=x+window_TL[0]
    y=y+window_TL[1]
    pyautogui.moveTo(x,y)                               # mouse move and click
    for i in range(click_num):
        pyautogui.click()
    pyautogui.moveRel(0,0)                              # Go back to initial postion go get rid of mouse affection
    print('click',x,y)
    time.sleep(0.5)                                     # sleep 1.5 seconds awaiting changing of elements.


def loop_normal_actions(pool):
    # param:
    #     pool:  The action pool contains any possible action.
    #     count: Used to shut current mission when there is no
    #            click for a certain peroid (50 rounds action check)
    count=0
    # count
    while count<50:
        count=count+1
        for action in pool:

            # ############### add extra command before do any action.
            #
            # current_window=grab_game_window()
            # current_window=cv2.cvtColor(current_window,cv2.COLOR_RGB2GRAY)
            # first_check_icon= cv2.imread('./icons/shimen_task.png',0)
            # match_result=match_image(first_check_icon,current_window,threshold=0.75)
            # if match_result:
            #     x,y= match_result
            #     click_action(x,y,2)


            print('doing action',action)
            # current window
            current_window = grab_game_window()
            claim_bangpai_task_icon = cv2.imread(action,0)

            current_window = cv2.cvtColor(current_window, cv2.COLOR_RGB2GRAY)
            match_result=match_image(claim_bangpai_task_icon,current_window,threshold=0.75)
            print(match_result)
            if match_result:
                count=0
                x,y = match_result
                # trigger click action
                if 'shimen_task' in action or 'qinglong_task' in action or 'zhuque_task' in action or 'xuanwu_task' in action:
                    click_action(x,y,3)
                else:
                    click_action(x,y)

                if 'shangjiao' in action :
                    click_action(x,y,2)



def daily_activity():

    click_action(fixed_action_pool['activity'][0], fixed_action_pool['activity'][1])  # 点击 活动

    click_action(fixed_action_pool['daily_activity'][0], fixed_action_pool['daily_activity'][1])  # 点击 '日常活动'


def add_task_to_list(icon_path):
    match_result=None
    target_icon = cv2.imread(icon_path, 0)     # read target icon in gray scale
    # scroll the mouse 3 times.
    for i in range(3):

        current_window=grab_game_window()
        current_window=cv2.cvtColor(current_window,cv2.COLOR_RGB2GRAY)
        # justify if there is 帮派任务
        match_result=match_image(target_icon,current_window,threshold=0.9)
        if match_result :
            x,y=match_result
            click_action(x+250,y+35)                #  点击  '帮派任务'
            time.sleep(2)
            break
        else:
            pyautogui.moveTo(700,410)
            pyautogui.scroll(-8)
    if  not match_result:
        pyautogui.press('esc')
        return 'finished'

def start_task(pool,icon_path=None):

    # When user does not have any crew tasks:  Use Activity bar to claim one.

    daily_activity()       #打开日常任务栏

    # claim task
    if_finished=add_task_to_list(icon_path)
    if if_finished!='finished':

        # transfered to Crew basement. then begin tasks.
        loop_normal_actions(pool)           #   开始帮派任务 检测循环

        if 'zhuogui' in icon_path:
            start_task(pool,icon_path)


def run():
    # start Bang Pai mission
    print('开始 帮派任务')
    start_task(bangpai_pool, icon_path="./icons/bangpai_activity.png")
    print('开始 师门任务')
    # start_task(shimen_pool,icon_path="./icons/shimen_activity.png")
    print('开始 秘境降妖 活动')
    start_task(mijingxiangyao_pool,icon_path="./icons/mijingxiangyao_activity.png")

    # Zhuo Gui has no limitation in a day. put in the last.
    print('开始 捉鬼（队员模式）')
    start_task(zhuogui_pool,"./icons/zhuogui_activity.png")


if __name__=='__main__':
    run()