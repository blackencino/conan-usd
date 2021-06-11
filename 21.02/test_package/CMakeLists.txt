cmake_minimum_required(VERSION 3.10.0)
project(test_package CXX)

find_package(usd REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example PUBLIC usd::usd)
#target_compile_features(example PUBLIC cxx_std_14)
