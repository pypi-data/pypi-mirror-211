if(${NOTEST})
    message(STATUS "Skipping test targets")
else()
    set(project acquire-core-libs)

    foreach(name
        unit-tests
        instance-types
    )
        set(tgt "${project}-${name}")
        add_executable(${tgt} ${name}.cpp)
        target_link_libraries(${tgt}
            acquire-core-logger
            acquire-core-platform
            acquire-device-properties
            acquire-device-kit
            acquire-device-hal
        )
        target_compile_definitions(${tgt} PUBLIC TEST="${tgt}")
        set_target_properties(${tgt} PROPERTIES
            MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>"
        )
        add_test(NAME test-${tgt} COMMAND ${tgt})
        set_tests_properties(test-${tgt} PROPERTIES LABELS anyplatform)
    endforeach()
endif()
