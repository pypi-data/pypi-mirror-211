set(tgt acquire-core-logger)
add_library(${tgt} STATIC logger.h logger.c)
target_include_directories(${tgt} PUBLIC "${CMAKE_CURRENT_LIST_DIR}")
set_target_properties(${tgt} PROPERTIES
    MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>"
)
install(TARGETS ${tgt})
