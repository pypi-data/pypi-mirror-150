import os
import sys
import subprocess
import importlib
import time

import likeshell
from likeshell.shell import run_cls


def load_spider_name():
    pwd = os.getcwd()
    sys.path.append(pwd)
    # scrapy项目根目录下只能存在一个文件夹(除隐藏文件外)
    spider_paths = [i for i in os.walk(pwd).__next__()[1] if not i.startswith('.')]
    if not spider_paths:
        return
    spider_module_path = f'{spider_paths[0]}.spiders'
    spider_path = spider_module_path.replace('.', '/')
    if not os.path.exists(spider_path):
        return

    try:
        # scrapy项目spiders包中只能有一个py文件(除__init__.py文件外)
        spider_files = [
            i for i in os.walk(spider_path).__next__()[2] if i != '__init__.py' and i.endswith('.py')
        ]
        spider_file = spider_files[0][:-3]
        module = importlib.import_module(f'{spider_module_path}.{spider_file}')
        for k, v in module.__dict__.items():
            base = None
            if hasattr(v, '__base__'):
                base = v.__base__.__name__
            if isinstance(v, type) and base == 'HttpSpider':
                return v.name
    except Exception:
        return


class CjztCrawler(likeshell.Main):
    def crawl(self, iid, sid, env):
        spider_name = load_spider_name()
        if spider_name is None:
            cmd = f'python3 main.py {iid} {sid} {env}'
        else:
            cmd = f'scrapy crawl {spider_name} ' \
                  f'-a instance_id={iid} -a spider_id={sid} -a env={env} -a cjzt_log=./log_{iid}.log --nolog'
        os.system(cmd)

    def stats(self, iid, env):
        while True:
            cmd = f"ps -aux | grep -v grep | grep scrapy | grep {iid} | awk '{{print $3,$4}}'"
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            stats = p.stdout.read()
            if stats:
                cup_pst, mem_pst = stats.decode().split(' ')
                print(cup_pst, mem_pst)
            time.sleep(120)


def main():
    run_cls(CjztCrawler, CjztCrawler.__dict__)
