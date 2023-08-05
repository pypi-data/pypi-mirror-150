import os
import time
import ast
from collections import deque
import multiprocessing as mp

import torch
import numpy as np

class BasicDisplay:
    def __init__(self):
        self.losses = deque(maxlen=100)

    def handle(self, data):
        if data["type"] == "train_info":
            epoch = data["epoch"]
            batch_idx = data["batch_idx"]

            self.losses.append(data["loss"])
            loss_val = round(np.mean(self.losses), 2)

            print(f"({epoch:03} {batch_idx:04}) {loss_val:.2f}", end="\r")

        elif data["type"] == "val_info":
            epoch = data["epoch"]
            batch_num = data["batch_idx"]

            val_str = f"Epoch: {epoch} Batch: {batch_num} "

            for loss_info in data["losses"]:
                loss_type = loss_info["loss_type"]
                loss_val = loss_info["loss"]
                val_str += f"{loss_type}: {loss_val} "
            print()
            print(val_str)


class LogWriter:
    """
    Class used for the main process to coordinate writing to log file/saving
    checkpoints.
    """

    def __init__(self, log_path, log_proc=True, display=BasicDisplay):
        os.makedirs(log_path, exist_ok=True)
        self.log_path = log_path
        self.log_file_path = f"{log_path}/train.log"
        self.log_file = open(self.log_file_path, "w")
        
        if log_proc:
            spawn_logger_worker(display, self.log_file_path)

    def log_info(self, info):
        info.dump(self.log_file)
        self.log_file.flush()

    def log_str(self, log_str):
        self.log_file.write(log_str + "\n")
        self.log_file.flush()

    def checkpoint(self, epoch, batch_idx, model):
        checkpoint_path = f"{self.log_path}/model_{epoch}.pth"
        torch.save(model.state_dict(), checkpoint_path)



def log_worker(display_type, log_path):

    logger = display_type()

    file_obj = open(log_path, "r")

    # Main Loop
    while True:
        new_data = file_obj.readline().rstrip()

        if new_data == "":
            time.sleep(0.1)
        else:
            try:
                new_data = ast.literal_eval(new_data)
            except:
                print(f"Failed to parse: {new_data}")
            else:
                logger.handle(new_data)


def spawn_logger_worker(display_type, log_path):
    p = mp.Process(target=log_worker, args=(display_type, log_path,))
    p.daemon = True
    p.start()
