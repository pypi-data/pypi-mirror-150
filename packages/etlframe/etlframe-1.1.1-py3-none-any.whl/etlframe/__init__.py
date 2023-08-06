import os
import sys
from pathlib import Path

# from nb_log import nb_print

base_path = Path(__file__).parent
# print(base_path)

project_path = Path('./').absolute()

def read_log_config():
    with open(base_path.joinpath('nb_log_config.py'), 'r', encoding='utf-8') as r:
        content = r.read()
    return content





def write_log_config():
    # nb_print(f'当前项目的根目录是：\n {sys.path[1]}')
    root_path = Path(sys.path[1])
    project_path_nb_log_config = root_path.joinpath('nb_log_config.py')
    if not project_path_nb_log_config.exists():
        with open('nb_log_config.py', 'w') as w:
            w.write(read_log_config())
        print(f'{project_path_nb_log_config} 创建完成')
    else:
        print(f'{project_path_nb_log_config} 已经存在')
#
#
write_log_config()
