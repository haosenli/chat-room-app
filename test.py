import threading
import pickle
import time
import sys


def p1():
    while True:
        s = input()
        print(s)
        
def p2():
    count = 0
    while True:
        print('heheheh')
        count += 1
        if count > 5:
            sys.exit(0)
        time.sleep(2)
        
def main():
    t1 = threading.Thread(target=p1)
    t2 = threading.Thread(target=p2)
    t1.start()
    t2.start()
    
if __name__ == '__main__':
    # main()
    data = 'hahah hehehe'
    data_type = 'str'
    format = 'utf-8'
    head = 64
    # encode
    msg_len = str(len(data)).encode(format)
    data_type = data_type.encode(format)
    msg_len += b' ' * (head - len(msg_len))
    data_type += b' ' * (head - len(data_type))
    data = pickle.dumps(data)
    encoded_data = msg_len + data_type + data
    # decode
    padding1 = encoded_data[:head]
    encoded_data = encoded_data[head:]
    padding2 = encoded_data[:head]
    encoded_data = encoded_data[head:]
    msg_len = padding1.decode(format).strip()
    data_type = padding2.decode(format).strip()
    content = pickle.loads(encoded_data)
    print(msg_len, data_type, content)