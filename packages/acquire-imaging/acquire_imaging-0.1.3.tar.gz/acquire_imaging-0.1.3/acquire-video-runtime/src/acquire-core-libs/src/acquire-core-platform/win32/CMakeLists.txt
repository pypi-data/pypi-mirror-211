set(tgt acquire-core-platform)
add_library(${tgt} STATIC
        platform.h
        platform.c)
target_link_libraries(${tgt} PUBLIC acquire-core-logger)
target_include_directories(${tgt} PUBLIC "${CMAKE_CURRENT_LIST_DIR}")
set_target_properties(${tgt} PROPERTIES
        MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>"
)
