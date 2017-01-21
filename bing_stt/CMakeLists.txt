cmake_minimum_required(VERSION 2.8.3)
project(bing_stt)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -g")

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

##  services in the 'srv' folder
add_service_files(
   FILES
   TextSpoken.srv
)

generate_messages(
   DEPENDENCIES
   std_msgs
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs message_generation 
)
