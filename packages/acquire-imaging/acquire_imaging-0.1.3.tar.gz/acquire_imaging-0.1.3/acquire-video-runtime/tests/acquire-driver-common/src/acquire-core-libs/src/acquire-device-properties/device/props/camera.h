#ifndef H_ACQUIRE_PROPS_CAMERA_V0
#define H_ACQUIRE_PROPS_CAMERA_V0

#include <stdint.h>

#include "components.h"
#include "metadata.h"

#ifdef __cplusplus
extern "C"
{
#endif

    struct CameraProperties
    {
        float exposure_time_us;
        float line_interval_us;
        enum Direction readout_direction;
        uint8_t binning;
        enum SampleType pixel_type;
        struct camera_properties_offset_s
        {
            uint32_t x, y;
        } offset;
        struct camera_properties_shape_s
        {
            uint32_t x, y;
        } shape;
        struct camera_properties_input_triggers_s
        {
            struct Trigger acquisition_start, frame_start, exposure;
        } input_triggers;
        struct camera_properties_output_triggers_s
        {
            struct Trigger exposure, frame_start, trigger_wait;
        } output_triggers;
    };

    struct CameraPropertyMetadata
    {
        struct Property exposure_time_us;
        struct Property line_interval_us;
        struct Property readout_direction;
        struct Property binning;
        struct camera_properties_metadata_offset_s
        {
            struct Property x, y;
        } offset;
        struct camera_properties_metadata_shape_s
        {
            struct Property x, y;
        } shape;

        /// bit field: bit i is 1 if SampleType(i) is supported, 0 otherwise
        uint64_t supported_pixel_types;

        struct CameraPropertyMetadataDigitalLineMetadata
        {
            /// The number of supported digital IO lines
            /// Must be less than 8.
            uint8_t line_count;

            /// name[i] is a short, null terminated string naming line i.
            /// Support describing up to 8 names for use with triggering.
            char names[8][64];
        } digital_lines;

        struct CameraPropertiesTriggerMetadata
        {
            struct camera_properties_metadata_trigger_capabilities_s
            {
                /// Bit x is set if line x can be used as a trigger input.
                uint8_t input;
                /// Bit x is set if line x can be used as a trigger output.
                uint8_t output;
            } acquisition_start, exposure, frame_start;
        } triggers;
    };

#ifdef __cplusplus
}
#endif

#endif // H_ACQUIRE_PROPS_CAMERA_V0
