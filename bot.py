from core.helper import helper
import os
from time import sleep
import ntpath
import time

def check_req(h, req_imgs):
    cnt = 0
    for img in req_imgs:
        acc, _ = h.match_template(img)
        if acc < 0.7:
            print('必要失敗: {}'.format(cnt))
            return False
        cnt += 1

    return True

def check_opt(h, opt_imgs, min):
    accs = []
    cnt = 0
    for img in opt_imgs:
        acc, _ = h.match_template(img)
        if acc > 0.7:
            cnt += 1
        if cnt >= min:
            return True
    print('選用失敗: {}'.format(cnt))    
    return False


OPT_MIN = 1

if __name__ == '__main__':

    start_time = time.time()

    project_path = os.path.dirname(os.path.abspath(__file__))
    h = helper(project_path)
    h.setup_adb_client()
    temps = h.load_templates()
    reqs = [ntpath.basename(path) for path in h.required_list]
    opts = [ntpath.basename(path) for path in h.optional_list]
    print('必要:')
    for i in range(len(reqs)):
        print('{}'.format(reqs[i]))
    print('選中:')
    for i in range(len(opts)):
        print('{}'.format(opts[i]))
    times = 1

    while True:
        # 跳過動畫，盡量減少match
        while True:
            skip_acc, skip_loc = h.match_template(temps['skip'])
            if(skip_acc > 0.7):
                h.tap_screen(skip_loc[0], skip_loc[1])
                continue
            re_acc, re_loc = h.match_template(temps['re'])
            if(skip_acc < 0.7 and re_acc > 0.7):
                break

        # 開始檢查是否成功
        #if check_req(h, temps['required']) and check_opt(h, temps['optional'], OPT_MIN):
        #    break
        print('=====  {} ========='.format(times))
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print()
        if check_req(h, temps['required']) and check_opt(h, temps['optional'], OPT_MIN):
            break
        # 再來一次
        h.tap_screen(re_loc[0], re_loc[1])
        times += 1

    print('Total {} times'.format(times))
    print('Total runtime {} secs'.format(time.time() - start_time))

