# coding: utf-8
import os, sys, logging, subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
from Commands import Commands
from Utils import Utils
from consolelog import Console
from Manager import manager
import configparser


def parser_args():
    num = len(sys.argv)

    if num < 3:
        logging.error("arguments number <3")
        return

    for i in range(len(sys.argv)):
        logging.info("** " + str(i) + " **" + sys.argv[i])
    command = sys.argv[1]
    file = sys.argv[2]

    files = [file]

    if len(sys.argv) > 3:
        with open(file, encoding="utf8") as fp:
            files = fp.readlines()

    return command, files


def clear_log(log_dir, log_path):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    for name in os.listdir(log_dir):
        file_path = os.path.join(log_dir, name)
        if file_path != log_path:
            os.remove(file_path)


def init_log():
    tools_path = Utils.get_tools_path()
    log_dir = os.path.join(os.path.dirname(tools_path), "log")
    log_path = os.path.join(log_dir, time.strftime("%Y-%m-%d") + ".log")
    clear_log(log_dir, log_path)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_path,
                        filemode='a+')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.stream = sys.stdout
    formatter = logging.Formatter('%(filename)-20s[line:%(lineno)-4d] %(levelname)-6s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info("日志初始化成功")

def init_config():
    config = configparser.ConfigParser()
    config.read(os.path.join(Utils.get_tools_path(), 'config', 'config.ini'))
    if config.has_section('Log'):
        if 'Type' in config['Log'].keys():
            if config['Log']['Type'] == "Consolve":
                Utils.log_type = 1
                Utils.cons_log = Console()
                Utils.cons_log.new_console_window(wait_for_new_console_setup=True, kill_program_on_console_close=False)
                Utils.cons_log.set_tag("UTILS")

if __name__ == '__main__':
    version = "1.5"
    init_log()
    init_config()
    try:
        command, files = parser_args()
    except Exception as e:
        logging.exception(e)
    # 去除前后回车
    for i, file in enumerate(files):
        files[i] = file.strip()
    logging.info("command:" + command)
    logging.info("files:" + str(files))

    try:
        manager(command,files)
        Utils.show_message("命令执行完毕")
    except subprocess.CalledProcessError as e:
        logging.exception(e)
        logging.exception(e.output)
    except Exception as e:
        logging.exception(e)
        Utils.show_message("命令执行失败：" + str(e))
    logging.info("log end")
    logging.info(
        "---------------------------------------------------------------------------------------------------------------------")
