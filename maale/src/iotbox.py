#!/usr/bin/python3

import rospy 
from maale.msg import iot


def get_from_firebase():
    #enter the recieiving code 
    #if condition where threshold is met
    temp=78.5
    humidity=45
    light=30

    return temp,humidity,light

def Iot(t,h,l):
    iot_data=iot()
    pub=rospy.Publisher("/iot",iot,queue_size=1)
    rate=rospy.Rate(1)

    while not rospy.is_shutdown():

        
        iot_data.temp=t
        iot_data.humidity=h
        iot_data.ldr=l

        pub.publish(iot_data)
        rate.sleep()


if __name__=="__main__":
    rospy.init_node('iot')
    t,h,l=get_from_firebase()
    Iot(t,h,l)




