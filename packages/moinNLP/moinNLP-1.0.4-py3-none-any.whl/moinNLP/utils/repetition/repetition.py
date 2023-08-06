from concurrent.futures import ThreadPoolExecutor
import re
import os
import logging
import traceback

logger = logging.getLogger(__name__)


def remove_repetition(texts: list):
    try:
        index_texts = [(i, text) for i, text in enumerate(texts)]

        white_list = read_white_list()

        def run_thread(index_text, white_list):
            return execute(index_text, white_list)

        res = []
        # 多线程
        with ThreadPoolExecutor(max_workers=8) as thread_pool:
            # 使用线程执行map计算
            res_text = thread_pool.map(run_thread, index_texts, white_list)
            res.extend(res_text)

        return [text[1] for text in sorted(res, key=lambda x: x[0])]
    except Exception:
        logger.error(traceback.format_exc())
        return texts


def execute(index_text, white_list):
    text = ''
    index = 0
    if isinstance(index_text, tuple):
        text = index_text[1]
        index = index_text[0]
    try:
        # 标点与特定字符交换位置
        text = re.sub(r'([，？！。])([呢吗啊吧嘛呀])', r'\2\1', text)

        # 去重 单字叠词 某些特定词不去重
        reg1 = r'([\u4e00-\u9fa5\W]{1}(?!(' + '|'.join(white_list) + ')))\\1{1,}'
        text = re.sub(reg1, r"\1", text)

        # 去重 连续的长度为2的重复子串
        reg2 = r'([\u4e00-\u9fa5\d]{2})\1{1,}'
        # 重复的全是数字，则不做处理  11
        if re.search(reg2, text):
            if not re.search(reg2, text).group(1).isdigit():
                text = re.sub(reg2, r"\1", text)

        # 去重 重复子串中间间隔4个字以内, 包含连续的重复子串
        reg3 = r'([\u4e00-\u9fa5\d]{2,})(.{0,4})\1'
        # 重复的全是数字，则不做处理  1000000000000
        if re.search(reg3, text):
            if not re.search(reg3, text).group(1).isdigit():
                text = re.sub(reg3, r"\1\2", text)
    except Exception:
        logger.error(traceback.format_exc())
        return (index, text)

    return (index, text)


def read_white_list():
    path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件路径的上一级目录
    with open(os.path.join(path, 'white.txt'), 'r', encoding='utf8') as f:
        while_list = [line.strip() for line in f.readlines()]
        f.close()
    return while_list


if __name__ == '__main__':
    text = '100万100万以内是吧'
    text2 = '1000000万以内是吧'
    text3 = '1万1万以内是吧'
    text4 = '11万以内是吧'
    print(remove_repetition([text, text2, text3, text4]))
