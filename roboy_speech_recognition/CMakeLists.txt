cmake_minimum_required(VERSION 2.8.3)
project(roboy_speech_recognition)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -g")

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  roboy_communication_cognition
)


catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs message_generation roboy_communication_cognition
)
