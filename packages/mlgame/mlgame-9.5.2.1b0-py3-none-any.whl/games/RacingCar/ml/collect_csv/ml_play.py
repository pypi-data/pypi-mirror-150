import csv
import os
import pickle

count = None
feature =None
target =None
class MLPlay:
    def __init__(self):
        global count,feature,target
        self.other_cars_position = []
        self.coins_pos = []
        print("Initial ml script")
        count=0
        feature =[]
        target = []

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        global count,feature,target
        # print( scene_info['status'])
        if scene_info['status'] != "GAME_ALIVE":
            #     todo store data
            count += 1
            print(f"store at {count}")

            with open(os.path.join(os.path.dirname(__file__), '0-feature-' + str(count) + '.pickle'), 'wb') as f:
                pickle.dump(feature, f)
            with open(os.path.join(os.path.dirname(__file__), '0-target-' + str(count) + '.pickle'), 'wb') as f:
                pickle.dump(target, f)
            with open(os.path.join(os.path.dirname(__file__), '0-feature-' + str(count) + '.csv'), 'w',
                      newline='') as f:
                csv.writer(f, delimiter=',').writerows(feature)
            with open(os.path.join(os.path.dirname(__file__), '0-target-' + str(count) + '.csv'), 'w', newline='') as f:
                csv.writer(f, delimiter=',').writerows(target)
            # time.sleep(1)
            return "RESET"
        if scene_info.__contains__("coin"):
            self.coin_pos = scene_info["coin"]
        print(scene_info)
        feature.append([1, 1, 1])
        target.append([2, 2, 2])
        return ["SPEED"]

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
