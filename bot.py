from core.helper import helper
import os
from time import sleep
import ntpath
import time

def check_req(h, req_imgs):
    accs = []
    for img in req_imgs:
        acc, _ = h.match_template(img)
        accs.append(acc)

    return accs

def check_opt(h, opt_imgs, min):
    accs = []
    cnt = 0
    for img in opt_imgs:
        acc, _ = h.match_template(img)
        accs.append(acc)
        if acc > 0.7:
            cnt += 1


    return (accs, cnt)

OPT_MIN = 1

start_time = time.time()

project_path = os.path.dirname(os.path.abspath(__file__))
h = helper(project_path)
temps = h.load_templates()
reqs = [ntpath.basename(path) for path in h.required_list]
opts = [ntpath.basename(path) for path in h.optional_list]
times = 1

while True:
    # 跳過動畫
    while True:
        skip_acc, skip_loc = h.match_template(temps['skip'])
        re_acc, re_loc = h.match_template(temps['re'])
        if(skip_acc < 0.7 and re_acc > 0.7):
            break
        if(skip_acc > 0.7 and re_acc < 0.7):
            h.tap_screen(skip_loc[0], skip_loc[1])

    # 開始檢查是否成功
    req_accs = check_req(h, temps['required'])
    opt_accs, cnt = check_opt(h, temps['optional'], OPT_MIN)
    '''[DEBUG]
    print('必要:')
    for i in range(len(reqs)):
        print('{}: {}'.format(reqs[i], req_accs[i]))
    print('選中:')
    for i in range(len(opts)):
        print('{}: {}'.format(opts[i], opt_accs[i]))
    '''
    print('=====  {} ========= : {}, {}'.format(times, sum(acc > 0.65 for acc in req_accs), cnt))
    if all(acc > 0.65 for acc in req_accs) and cnt >= OPT_MIN:
        break
    # 再來一次
    h.tap_screen(re_loc[0], re_loc[1])
    times += 1

print('Total {} times'.format(times))
print('Total runtime {} secs'.format(time.time() - start_time))

