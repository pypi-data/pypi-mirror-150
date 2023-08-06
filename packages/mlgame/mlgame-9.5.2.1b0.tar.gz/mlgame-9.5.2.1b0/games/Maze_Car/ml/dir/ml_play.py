# from os import path
# import time
# import numpy as np

class MLPlay:
    def __init__(self, player):
        # self.player_no = player[6]
        self.PASSED = -55
        self.PREDIT = 222
        self.TARGET = 999
        self.UPSET = -10
        self.MAP = 30

        self.command = {}
        self.last_command = {}
        self.info = {}
        self.sensor = {}
        self.control_list = [{"left_PWM": 0, "right_PWM": 0}]

        print("Initial ml script")

    def update(self, scene_info: dict):

        # get data
        self.info = scene_info.copy()
        self.sensor = scene_info.copy()
        keys_info = ['R_sensor', 'L_sensor', 'F_sensor', 'L_T_sensor', 'R_T_sensor']  # 要移掉的
        list(map(self.info.pop, keys_info))
        keys_sensor = ['frame', 'status', 'x', 'y', 'angle', 'end']
        list(map(self.sensor.pop, keys_sensor))
        self.angle = scene_info["angle"]  # float
        self.x = round(scene_info["x"])
        self.y = abs(round(scene_info["y"]))

        if scene_info["status"] != "GAME_ALIVE":
            # print("GAME OVER.....")
            # self.last_command = ''
            return "RESET"

        # start the game
        if self.info["frame"] > 1:
            self.command = self.run_previous()
            if not self.command:  # 重新判斷
                self.command = self.mazeCar_run()

            # print(self.command, self.angle, self.sensor)
            # 保存上一個指令
            self.last_command = self.command
            return self.control_list

        else:
            self.control_list[0]["left_PWM"] = 100
            self.control_list[0]["right_PWM"] = 100
            return self.control_list

    def reset(self):
        """
        Reset the status
        """

        self.command = {}
        self.last_command = {}
        self.info = {}
        self.sensor = {}
        self.control_list = [{"left_PWM": 0, "right_PWM": 0}]

        print("reset_dir ml script")

    def run_previous(self):
        mis_error = 5  # 設定轉彎的誤差範圍
        max_dir = max(self.sensor, key=self.sensor.get)
        min_dir = min(self.sensor, key=self.sensor.get)

        # 轉彎的過程卡住
        if (min_dir == "F_sensor" or min_dir == "R_T_sensor" or min_dir == "L_T_sensor") and (
                self.sensor["F_sensor"] < 2 or self.sensor["L_T_sensor"] < 2 or self.sensor["R_T_sensor"] < 2):
            self.back({'dir': 'back', 'speed': 255, 'degree': self.angle, 'frame': self.info["frame"]})
            command = self.last_command

        elif self.last_command.get("dir") == "turn_LEFT" and (
                self.last_command["degree"] <= self.angle - mis_error or self.angle + mis_error <= self.last_command[
            "degree"]):
            self.turn_left(self.last_command)
            command = self.last_command

        elif self.last_command.get("dir") == "turn_RIGHT" and (
                self.last_command["degree"] <= self.angle - mis_error or self.angle + mis_error <= self.last_command[
            "degree"]):
            self.turn_right(self.last_command)
            command = self.last_command

        elif self.last_command.get("dir") == "turn_left" and (
                self.last_command["degree"] <= self.angle - mis_error or self.angle + mis_error <= self.last_command[
            "degree"]):
            self.turn_left(self.last_command)
            command = self.last_command

        elif self.last_command.get("dir") == "turn_right" and (
                self.last_command["degree"] <= self.angle - mis_error or self.angle + mis_error <= self.last_command[
            "degree"]):
            self.turn_right(self.last_command)
            command = self.last_command
        else:
            command = ""
        return command

    def mazeCar_run(self):
        max_dir = max(self.sensor, key=self.sensor.get)
        min_dir = min(self.sensor, key=self.sensor.get)

        # 側面卡住
        # if self.sensor[min_dir] < 2 and min_dir !="R_sensor" and min_dir !="L_sensor":
        #     if self.sensor[min_dir] < 1.5 :
        #         command = {'dir':'backe_fast', 'speed':255, 'degree':self.angle}
        #         self.back(command) 
        #     elif min_dir == "L_T_sensor":
        #         command = {'dir':'RIGHT', 'speed':255, 'degree':self.trnasDegree(self.angle-15)}
        #         self.turn_right(command) 
        #     elif min_dir == "R_T_sensor":
        #         command = {'dir':'LEFT', 'speed':255, 'degree':self.trnasDegree(self.angle+15)}
        #         self.turn_left(command) 
        #     else:
        #         command = {'dir':'back', 'speed':250, 'degree':self.angle}
        #         self.back(command) 
        # 正面卡住
        if min_dir == "F_sensor" and (
                self.sensor["F_sensor"] < 2 or self.sensor["L_T_sensor"] < 2 or self.sensor["R_T_sensor"] < 2):
            command = {'dir': 'back', 'speed': 250, 'degree': self.angle, 'frame': self.info["frame"]}
            self.back(command)
            # back fast
        # elif min_dir =="F_sensor" and  self.sensor["F_sensor"] < 5 and (max_dir=="R_T_sensor" or max_dir=="L_T_sensor"): 
        #     command = {'dir':'back_fast', 'speed':255, 'degree':self.angle,'frame':self.info["frame"]}
        #     self.back(command) 
        # 死巷迴轉
        elif self.sensor["F_sensor"] < 10 and self.sensor["R_sensor"] < 10 and self.sensor["L_sensor"] < 10 and \
                self.sensor["L_T_sensor"] < 15 and self.sensor["R_T_sensor"] < 15:
            command = {'dir': 'turn_U', 'speed': 255, 'degree': self.trnasDegree(self.angle + 180),
                       'frame': self.info["frame"]}
            self.turn_U(command)
        # 左右轉
        # elif (max_dir=="L_sensor" or max_dir=="R_sensor") and self.sensor[max_dir] > 60:
        #     #turn left 90
        #     if max_dir == "L_sensor":
        #         command = {'dir':'turn_LEFT','speed':200, 'degree':self.trnasDegree(self.angle+70) ,'frame':self.info["frame"]}
        #         self.turn_left(command) 
        #     #turn right 90
        #     else:
        #         command = {'dir':'turn_RIGHT','speed':200, 'degree':self.trnasDegree(self.angle-70),'frame':self.info["frame"]}
        #         self.turn_right(command)
        elif self.sensor["F_sensor"] < 20:
            # turn left slow
            if max_dir == "L_T_sensor":
                command = {'dir': 'turn_left', 'speed': 80, 'degree': self.trnasDegree(self.angle + 15),
                           'frame': self.info["frame"]}
                self.turn_left(command)
                # turn right slow
            elif max_dir == "R_T_sensor":
                command = {'dir': 'turn_right', 'speed': 80, 'degree': self.trnasDegree(self.angle - 15),
                           'frame': self.info["frame"]}
                self.turn_right(command)
            # turn left 90
            elif max_dir == "L_sensor":
                command = {'dir': 'turn_LEFT', 'speed': 150, 'degree': self.trnasDegree(self.angle + 25),
                           'frame': self.info["frame"]}
                self.turn_left(command)
                # turn right 90
            elif max_dir == "R_sensor":
                command = {'dir': 'turn_RIGHT', 'speed': 150, 'degree': self.trnasDegree(self.angle - 25),
                           'frame': self.info["frame"]}
                self.turn_right(command)
            else:
                # 慢行(探索)
                command = {'dir': 'move_slow', 'speed': 80, 'degree': self.angle, 'frame': self.info["frame"]}
                self.move(command)
        else:
            # 正常行
            command = {'dir': 'move_fast', 'speed': 225, 'degree': self.angle, 'frame': self.info["frame"]}
            self.move(command)

        return command

    def move(self, command: dict):
        self.control_list[0]["left_PWM"] = command["speed"]
        self.control_list[0]["right_PWM"] = command["speed"]
        if self.sensor["L_sensor"] - self.sensor["R_sensor"] > 2:
            self.control_list[0]["right_PWM"] += 30
        elif self.sensor["R_sensor"] - self.sensor["L_sensor"] > 2:
            self.control_list[0]["left_PWM"] += 30
        else:
            pass

    def back(self, command: dict):
        if command["speed"] == 255:
            self.control_list[0]["left_PWM"] = -command["speed"]
            self.control_list[0]["right_PWM"] = -command["speed"]
        elif self.sensor["L_T_sensor"] < self.sensor["R_T_sensor"]:
            self.control_list[0]["left_PWM"] = -command["speed"]
            self.control_list[0]["right_PWM"] = -command["speed"] // 2
        else:
            self.control_list[0]["left_PWM"] = -command["speed"] // 2
            self.control_list[0]["right_PWM"] = -command["speed"]

    def turn_U(self, command: dict):
        if self.sensor["L_sensor"] >= self.sensor["R_sensor"]:
            self.control_list[0]["left_PWM"] = -command["speed"]
            self.control_list[0]["right_PWM"] = command["speed"]
        else:
            self.control_list[0]["left_PWM"] = command["speed"]
            self.control_list[0]["right_PWM"] = -command["speed"]

    def turn_left(self, command: dict):
        self.control_list[0]["left_PWM"] = 2
        self.control_list[0]["right_PWM"] = command["speed"]

    def turn_right(self, command: dict):
        self.control_list[0]["left_PWM"] = command["speed"]
        self.control_list[0]["right_PWM"] = 2

    def trnasDegree(self, degree):
        if degree < 0:  # turn right
            return 360 - abs(degree)
        elif degree > 360:
            return degree % 360
        else:
            return degree
