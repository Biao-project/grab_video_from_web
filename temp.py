import threading
import queue










if __name__ == '__main__':
    qq = queue.Queue(4)
    qq.put('23434')
    print('size=', qq.qsize())
    if qq.qsize()>0:
        da = qq.get(timeout=0.1)
        print('da=', da)
    print('size=', qq.qsize(), qq.empty())
    if qq.qsize():
        da = qq.get(timeout=0.1)
        print('da2=', da)

    print('====')
