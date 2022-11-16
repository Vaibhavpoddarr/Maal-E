#include <ros.h>
#include <std_msgs/Empty.h>

ros::NodeHandle  nh;
int blue=13;


void callback(const std_msgs::Empty& toggle_msg)
{
  digitalWrite(blue,HIGH);
  delay(500);
  
  
  
}

ros::Subscriber<std_msgs::Empty> sub("toggle",&callback);



void setup() {
  // put your setup code here, to run once:
  pinMode(blue,OUTPUT);
  
  nh.initNode();
  nh.subscribe(sub);

}

void loop() {
  // put your main code here, to run repeatedly:
 
  nh.spinOnce();
  delay(500);
  }
