#ifndef H_ACQUIRE_KIT_CAMERA_V0
#define H_ACQUIRE_KIT_CAMERA_V0

#include "device/props/device.h"
#include "device/props/camera.h"

#ifdef __cplusplus
extern "C"
{
#endif

    struct Camera
    {
        struct Device device;
        enum DeviceState state;

        enum DeviceStatusCode (*set)(struct Camera*,
                                     struct CameraProperties* settings);
        enum DeviceStatusCode (*get)(const struct Camera*,
                                     struct CameraProperties* settings);
        enum DeviceStatusCode (*get_meta)(const struct Camera*,
                                          struct CameraPropertyMetadata* meta);
        enum DeviceStatusCode (*get_shape)(const struct Camera*,
                                           struct ImageShape* shape);
        enum DeviceStatusCode (*start)(struct Camera*);
        enum DeviceStatusCode (*stop)(struct Camera*);

        // Fire the software trigger if it's enabled.
        enum DeviceStatusCode (*execute_trigger)(struct Camera*);

        enum DeviceStatusCode (*get_frame)(struct Camera*,
                                           void* im,
                                           size_t* nbytes,
                                           struct ImageInfo* info);
    };

#ifdef __cplusplus
}
#endif

#endif // H_ACQUIRE_KIT_CAMERA_V0
