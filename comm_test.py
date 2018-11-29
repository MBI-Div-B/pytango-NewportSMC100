import serial
from time import sleep
import array

def write_read(argin):
    ADDR = '1'
    # if argin ended with "?", then we expected an answer
    response = (argin[-1] == '?')
    if response:
        # cut the "?"
        prefix = ADDR + argin[:-1]
        send_str = ADDR + argin
        ser.flushInput()
        send_cmd(send_str)
        sleep (0.03)
        tmp_answer = ser.read(1024)
        if tmp_answer.startswith(prefix):
            answer = tmp_answer[len(prefix):]
        else:
            answer = 'bla'    
    else:    
        send_str = ADDR + argin
        send_cmd(send_str)
        answer = 'no res'
    return answer

def send_cmd(cmd):
    EOL = '\r\n'
    
    snd_str = cmd + EOL
    print snd_str
    print array.array('B', snd_str)
    ser.flushOutput()
    ser.write(snd_str)
    ser.flush()



if __name__ == "__main__":
    
    ser = serial.Serial(port="com94", timeout=0.050)
    if ser.isOpen():
        ser.close()
    ser.open()
    inp = ''
    while inp != 'q':
        inp = raw_input('Cmd (q=quit): ')      
        print (inp)
        if inp != 'q':
            print write_read(inp)
    ser.close()
    



