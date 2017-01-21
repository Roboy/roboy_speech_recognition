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

## Declare a cpp executable
#add_executable(bing_stt src/bing_stt_server.py)
#target_link_libraries(
#	bing_stt_node
#	${catkin_LIBRARIES}
#	${GSTREAMER_LIBRARIES}
#	${GST_APP_LIBRARIES}
#)
#add_dependencies(bing_stt ${catkin_EXPORTED_TARGETS})

## build talker and listener
#include_directories(
#	${catkin_INCLUDE_DIRS}
#	${GLIB_INCLUDE_DIRS}
#  ${GST_APP_INCLUDE_DIRS}
#)
