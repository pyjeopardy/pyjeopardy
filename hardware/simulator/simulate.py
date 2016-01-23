#!/usr/bin/python3

import os
import time
import pty


def main():
    sim_err = True

    master, slave = pty.openpty()

    print("Opened {}".format(os.ttyname(slave)))

    while True:
        input = ""

        # read all available data
        while True:
            tmp = os.read(master, 1)

            if ord(tmp) == 13:
                break

            input += tmp.decode("utf-8")

        # react
        if input == "V":
            os.write(master, b"buzzer\r\n")
            os.write(master, b"simulator 0.1\r\n")
        if input == "Q":
            if sim_err:
                os.write(master, b"E\r\n")
                sim_err = False
            else:
                os.write(master, b"A\r\n")
                time.sleep(2)
                os.write(master, b"1\r\n")

if __name__ == "__main__":
    main()
