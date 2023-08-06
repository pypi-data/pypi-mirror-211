def colorize_print(message: str, color: str) -> None:
    color_dic = {"red": "31m",
                 "green": "32m",
                 "yellow": "33m",
                 "blue": "34m",
                 "purple": "35m",
                 "cyan": "36m"}
    print("\033[" + color_dic[color] + message + "\033[0m")
