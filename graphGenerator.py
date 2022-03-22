#!/usr/bin/python3
#© Butnariu Bogdan-Mihai
import matplotlib.pyplot as plt

def BKTTime():
    
    v_y = [11, 102.5, 7.18] #media nr varfurilor
    
    bkt_x = [0.025, 0.256, 0.023] #media timpilor de rulare de 5 ori pentru un test
    rdc_x = [0.41, 11.66, 0.26] #media timpilor de rulare de 5 ori pentru un test

    plt.plot(bkt_x, v_y, label='BKT Time', marker='*', linestyle='None')
    plt.plot(rdc_x, v_y, label='RDC Time', marker='*', color='red', linestyle='None')

    plt.title('Relation between RDC and BKT Time')
    plt.xlabel('Avg. Time per test')
    plt.ylabel('Avg. N. of Vertex')
    plt.legend()

    
    for i, j in zip(bkt_x, v_y):
        plt.text(i, j+0.5, '({}, {})'.format(i, j))
    for i, j in zip(rdc_x, v_y):
        plt.text(i, j+0.5, '({}, {})'.format(i, j))

    plt.savefig('BKTTime_V.jpg')
    plt.clf()

def RDCTime():
    
    v_y = [11, 102.5, 7.18] #media nr varfurilor

    rdc_x = [0.41, 11.66, 0.26] #media timpilor de rulare de 5 ori pentru un test
    
    plt.plot(rdc_x, v_y, label='RDC Time', marker='*', linestyle='None')

    plt.title('Relation between N. of Vertex and RDC Time')
    plt.xlabel('Avg. Time per test')
    plt.ylabel('Avg. N. of Vertex')
    plt.legend()

    for i, j in zip(rdc_x, v_y):
        plt.text(i, j+0.5, '({}, {})'.format(i, j))

    plt.savefig('RDCTime_V.jpg')
    plt.clf()

def BKTRDC():
    
    v_y = [11, 102.5, 7.18] #media nr varfurilor, cat 2, 1, 3
    
    rdc_x = [0.41, 11.66, 0.26] #media timpilor de rulare de 5 ori pentru un test
    bkt_x = [0.025, 0.256, 0.023] #media timpilor de rulare de 5 ori pentru un test

    #bkt / rdc
    bkt_rdc = []
    for i in range(0, 3):
        bkt_rdc.append(int(rdc_x[i]/bkt_x[i]))
    
    plt.plot(bkt_rdc, v_y, label='BKT/RDC', marker='*', linestyle='None')

    plt.title('Relation between N. of Vertex and BKT/RDC Factor')
    plt.xlabel('BKT/RDC Factor per test')
    plt.ylabel('Avg. N. of Vertex')
    plt.legend()

    for i, j in zip(bkt_rdc, v_y):
        plt.text(i, j+0.5, '({}, {})'.format(i, j))

    plt.savefig('BKT_RDC_V.jpg')
    plt.clf()    

if __name__ == '__main__':
    BKTTime()
    RDCTime()
    BKTRDC()