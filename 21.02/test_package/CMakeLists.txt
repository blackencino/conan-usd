cmake_minimum_required(VERSION 3.10.0)
project(test_package CXX)

#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()

find_package(usd REQUIRED)

add_executable(example example.cpp)
# target_link_libraries(example PUBLIC usd::usd Shlwapi.lib Dbghelp.lib Ws2_32.lib)
target_link_libraries(example PUBLIC usd::usd)

set(BLAH $<TARGET_FILE:usd::usd>)
message(STATUS "TARGET FILE: ${BLAH}")

# if(MSVC)
#     target_link_libraries(example -WHOLEARCHIVE:$<TARGET_FILE:usd_ms> usd_ms)
# elseif(CMAKE_COMPILER_IS_GNUCXX)
#     target_link_libraries(example -Wl,--whole-archive usd_ms -Wl,--no-whole-archive)
# elseif("${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
#     target_link_libraries(example -Wl,-force_load usd_ms)
# endif()

target_compile_features(example PUBLIC cxx_std_14)
# target_compile_definitions(example PUBLIC "PXR_STATIC")

message(STATUS "CONAN LIBS in test_package is: ${CONAN_LIBS}")

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
