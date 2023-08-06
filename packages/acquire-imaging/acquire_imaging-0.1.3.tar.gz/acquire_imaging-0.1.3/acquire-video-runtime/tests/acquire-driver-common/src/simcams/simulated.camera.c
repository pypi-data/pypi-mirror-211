#include "simulated.camera.h"

#include "device/kit/camera.h"
#include "device/kit/driver.h"
#include "device/props/camera.h"
#include "device/props/components.h"
#include "platform.h"
#include "logger.h"

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "pcg_basic.h"

#ifdef __AVX2__
#include "bin2.avx2.c"
#else
#include "bin2.plain.c"
#endif

#define MAX_IMAGE_WIDTH (1ULL << 13)
#define MAX_IMAGE_HEIGHT (1ULL << 13)
#define MAX_BYTES_PER_PIXEL (2)

#define containerof(ptr, T, V) ((T*)(((char*)(ptr)) - offsetof(T, V)))
#define countof(e) (sizeof(e) / sizeof(*(e)))

#define L aq_logger
#define LOG(...) L(0, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)
#define LOGE(...) L(1, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)

// #define TRACE(...) L(0, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)
#define TRACE(...)

#define ECHO(e)                                                                \
    TRACE("ECHO %s", #e);                                                      \
    e
// #define ECHO(e) e

#define EXPECT(e, ...)                                                         \
    do {                                                                       \
        if (!(e)) {                                                            \
            LOGE(__VA_ARGS__);                                                 \
            goto Error;                                                        \
        }                                                                      \
    } while (0)
#define CHECK(e) EXPECT(e, "Expression evaluated as false:\n\t%s", #e)

#define max(a, b) (((a) > (b)) ? (a) : (b))

uint8_t
popcount_u8(uint8_t value);

static float
get_animation_time_sec();

struct SimulatedCamera
{
    struct CameraProperties properties;
    enum BasicDeviceKind kind;

    struct
    {
        struct clock throttle;
        int is_running;
        struct thread thread;
    } streamer;

    struct
    {
        void* data;
        struct ImageShape shape;
        struct lock lock;
        int64_t frame_id;
        int64_t last_emitted_frame_id;
        struct condition_variable frame_ready;
    } im;

    struct
    {
        struct event event;
    } software_trigger;

    uint64_t hardware_timestamp;
    struct Camera camera;
};

static size_t
bytes_of_type(const enum SampleType type)
{
    CHECK(0 <= type && type < SampleTypeCount);
    const size_t table[] = { 1, 2, 1, 2, 4, 2, 2, 2 };
    CHECK(countof(table) == SampleTypeCount);
    return table[type];
Error:
    return 0;
}

static size_t
bytes_of_image(const struct ImageShape* const shape)
{
    return shape->strides.planes * bytes_of_type(shape->type);
}

static size_t
aligned_bytes_of_image(const struct ImageShape* const shape)
{
    const size_t n = bytes_of_image(shape);
    return ((n + 31) >> 5) << 5;
}

static void
im_fill_rand(const struct ImageShape* const shape, uint8_t* buf)
{
    const size_t nbytes = aligned_bytes_of_image(shape);
    const uint8_t* const end = buf + nbytes;
    for (uint8_t* p = buf; p < end; p += 4)
        *(uint32_t*)p = pcg32_random();
}

/// This is used for animating the parameter in im_fill_pattern.
/// This timebase gets shared between all "pattern" cameras and as a result they
/// are synchronized.
///
/// Thread safety: Don't really need to worry about since we don't care who
/// wins during initialization. Afterwards it's effectively read only.
static struct
{
    struct clock clk;
    int is_initialized;
} g_animation_clk = { 0 };

static void
im_fill_pattern(const struct ImageShape* const shape,
                float ox,
                float oy,
                uint8_t* buf)
{
    float t = get_animation_time_sec();

    const float cx = ox + 0.5f * (float)shape->dims.width;
    const float cy = oy + 0.5f * (float)shape->dims.height;
    for (uint32_t y = 0; y < shape->dims.height; ++y) {
        const float dy = y - cy;
        const float dy2 = dy * dy;
        for (uint32_t x = 0; x < shape->dims.width; ++x) {
            const size_t o = (size_t)shape->strides.width * x +
                             (size_t)shape->strides.height * y;
            const float dx = x - cx;
            const float dx2 = dx * dx;
            buf[o] =
              (uint8_t)(127.0f *
                        (sinf(6.28f * (t * 10.0f + (dx2 + dy2) * 1e-2f)) +
                         1.0f));
        }
    }
}
static float
get_animation_time_sec()
{
    float t;
    {
        struct clock* const clk = &g_animation_clk.clk;
        if (!g_animation_clk.is_initialized) {
            clock_init(clk);
            g_animation_clk.is_initialized = 1;
        }
        t = (float)clock_toc_ms(clk) * 1e-3f;
    }
    return t;
}

static void
compute_strides(struct ImageShape* shape)
{
    uint32_t* dims = (uint32_t*)&shape->dims;
    int64_t* st = (int64_t*)&shape->strides;
    st[0] = 1;
    for (int i = 1; i < 4; ++i)
        st[i] = st[i - 1] * dims[i - 1];
}

static void
compute_full_resolution_shape_and_offset(const struct SimulatedCamera* self,
                                         struct ImageShape* shape,
                                         uint32_t offset[2])
{
    const uint8_t b = self->properties.binning;
    const uint32_t w = b * self->properties.shape.x;
    const uint32_t h = b * self->properties.shape.y;
    offset[0] = b * self->properties.offset.x;
    offset[1] = b * self->properties.offset.y;
    shape->type = self->im.shape.type;
    shape->dims = (struct image_dims_s){
        .channels = 1,
        .width = w,
        .height = h,
        .planes = 1,
    };
    compute_strides(shape);
}

static void
simulated_camera_streamer_thread(struct SimulatedCamera* self)
{
    clock_init(&self->streamer.throttle);

    while (self->streamer.is_running) {
        struct ImageShape full = { 0 };
        uint32_t origin[2] = { 0, 0 };

        ECHO(lock_acquire(&self->im.lock));
        ECHO(compute_full_resolution_shape_and_offset(self, &full, origin));

        switch (self->kind) {
            case BasicDevice_Camera_Random:
                im_fill_rand(&full, self->im.data);
                break;
            case BasicDevice_Camera_Sin:
                ECHO(im_fill_pattern(
                  &full, (float)origin[0], (float)origin[1], self->im.data));
                break;
            case BasicDevice_Camera_Empty:
                break; // do nothing
            default:
                LOGE(
                  "Unexpected index for the kind of simulated camera. Got: %d",
                  self->kind);
        }
        {
            int w = full.dims.width;
            int h = full.dims.height;
            int b = self->properties.binning >> 1;
            while (b) {
                ECHO(bin2(self->im.data, w, h));
                b >>= 1;
                w >>= 1;
                h >>= 1;
            }
        }

        if (self->properties.input_triggers.frame_start.enable) {
            ECHO(event_wait(&self->software_trigger.event));
        }

        self->hardware_timestamp = clock_tic(0);
        ++self->im.frame_id;

        ECHO(condition_variable_notify_all(&self->im.frame_ready));
        ECHO(lock_release(&self->im.lock));

        if (self->streamer.is_running)
            clock_sleep_ms(&self->streamer.throttle,
                           self->properties.exposure_time_us * 1e-3f);
    }
}

//
//  CAMERA INTERFACE
//

static enum DeviceStatusCode
simcam_get_meta(const struct Camera* camera,
                struct CameraPropertyMetadata* meta)
{
    const struct SimulatedCamera* self =
      containerof(camera, const struct SimulatedCamera, camera);
    const unsigned binning = self->properties.binning;
    // current shape
    const float cw = (float)self->properties.shape.x;
    const float ch = (float)self->properties.shape.y;
    // max shape
    const float w = (float)MAX_IMAGE_WIDTH / (float)binning;
    const float h = (float)MAX_IMAGE_HEIGHT / (float)binning;
    // max offset - min width and height are 1 px.
    const float ox = max(0, w - cw - 1);
    const float oy = max(0, h - ch - 1);

    *meta = (struct CameraPropertyMetadata){
        .line_interval_us = { 0 },
        .exposure_time_us = { .high = 1.0e6f, .writable = 1, },
        .binning = { .low = 1.0f, .high = 8.0f, .writable = 1, },
        .shape = {
            .x = { .low = 1.0f, .high = w, .writable = 1, },
            .y = { .low = 1.0f, .high = h, .writable = 1, },
        },
        .offset = {
            .x = { .high = ox, .writable = 1, },
            .y = { .high = oy, .writable = 1, },
        },
        .supported_pixel_types = (1ULL << SampleType_u8),
        .digital_lines = {
          .line_count=1,
          .names = { [0] = "Software" },
        },
        .triggers = {
          .frame_start = {.input=1, .output=0,},
        },
    };
    return Device_Ok;
}

#define clamp(v, L, H) (((v) < (L)) ? (L) : (((v) > (H)) ? (H) : (v)))

static enum DeviceStatusCode
simcam_set(struct Camera* camera, struct CameraProperties* settings)
{
    struct SimulatedCamera* self =
      containerof(camera, struct SimulatedCamera, camera);
    struct CameraPropertyMetadata meta = { 0 };

    if (!settings->binning)
        settings->binning = 1;

    EXPECT(popcount_u8(settings->binning) == 1,
           "Binning must be a power of two. Got %d.",
           settings->binning);

    if (self->properties.input_triggers.frame_start.enable &&
        !settings->input_triggers.frame_start.enable) {
        // fire if disabling the software trigger while live
        event_notify_all(&self->software_trigger.event);
    }

    self->properties = *settings;
    self->properties.pixel_type = SampleType_u8;
    self->properties.input_triggers = (struct camera_properties_input_triggers_s){
        .frame_start = { .enable = settings->input_triggers.frame_start.enable,
                         .line = 0, // Software
                         .kind = Signal_Input,
                         .edge = TriggerEdge_Rising,
        },
    };

    simcam_get_meta(camera, &meta);
    struct ImageShape* const shape = &self->im.shape;
    shape->dims = (struct image_dims_s){
        .channels = 1,
        .width = clamp(settings->shape.x,
                       (uint32_t)meta.shape.x.low,
                       (uint32_t)meta.shape.x.high),
        .height = clamp(settings->shape.y,
                        (uint32_t)meta.shape.y.low,
                        (uint32_t)meta.shape.y.high),
        .planes = 1,
    };
    compute_strides(shape);

    self->properties.shape = (struct camera_properties_shape_s){
        .x = shape->dims.width,
        .y = shape->dims.height,
    };

    return Device_Ok;
Error:
    return Device_Err;
}

static enum DeviceStatusCode
simcam_get(const struct Camera* camera, struct CameraProperties* settings)
{
    const struct SimulatedCamera* self =
      containerof(camera, const struct SimulatedCamera, camera);
    *settings = self->properties;
    return Device_Ok;
}

static enum DeviceStatusCode
simcam_get_shape(const struct Camera* camera, struct ImageShape* shape)
{
    const struct SimulatedCamera* self =
      containerof(camera, const struct SimulatedCamera, camera);
    *shape = self->im.shape;
    return Device_Ok;
}

static enum DeviceStatusCode
simcam_start(struct Camera* camera)
{
    struct SimulatedCamera* self =
      containerof(camera, struct SimulatedCamera, camera);
    self->streamer.is_running = 1;
    self->im.last_emitted_frame_id = -1;
    self->im.frame_id = -1;
    TRACE("SIMULATED CAMERA: thread launch");
    CHECK(thread_create(&self->streamer.thread,
                        (void (*)(void*))simulated_camera_streamer_thread,
                        self));
    return Device_Ok;
Error:
    return Device_Err;
}

static enum DeviceStatusCode
simcam_stop(struct Camera* camera)
{
    struct SimulatedCamera* self =
      containerof(camera, struct SimulatedCamera, camera);
    self->streamer.is_running = 0;
    event_notify_all(&self->software_trigger.event);
    condition_variable_notify_all(&self->im.frame_ready);

    TRACE("SIMULATED CAMERA: thread join");
    ECHO(thread_join(&self->streamer.thread));

    TRACE("SIMULATED CAMERA: exiting");
    return Device_Ok;
}

static enum DeviceStatusCode
simcam_execute_trigger(struct Camera* camera)
{
    struct SimulatedCamera* self =
      containerof(camera, struct SimulatedCamera, camera);
    event_notify_all(&self->software_trigger.event);
    return Device_Ok;
}

static enum DeviceStatusCode
simcam_get_frame(struct Camera* camera,
                 void* im,
                 size_t* nbytes,
                 struct ImageInfo* info_out)
{
    struct SimulatedCamera* self =
      containerof(camera, struct SimulatedCamera, camera);
    CHECK(*nbytes >= bytes_of_image(&self->im.shape));
    CHECK(self->streamer.is_running);

    // FIXME: software trigger. Could use a bool or maybe just trigger frame
    // ready
    TRACE("last: %5d current %5d",
          self->im.last_emitted_frame_id,
          self->im.frame_id);
    ECHO(lock_acquire(&self->im.lock));
    while (self->streamer.is_running &&
           self->im.last_emitted_frame_id >= self->im.frame_id) {
        ECHO(condition_variable_wait(&self->im.frame_ready, &self->im.lock));
    }
    self->im.last_emitted_frame_id = self->im.frame_id;
    if (!self->streamer.is_running) {
        goto Shutdown;
    }

    memcpy(im, self->im.data, bytes_of_image(&self->im.shape)); // NOLINT
    info_out->shape = self->im.shape;
    info_out->hardware_frame_id = self->im.frame_id;
    info_out->hardware_timestamp = self->hardware_timestamp;
Shutdown:
    ECHO(lock_release(&self->im.lock)); // only acquired in non-error path
    return Device_Ok;
Error:
    return Device_Err;
}

enum DeviceStatusCode
simcam_close_camera(struct Camera* camera_)
{
    struct SimulatedCamera* camera =
      containerof(camera_, struct SimulatedCamera, camera);
    EXPECT(camera_, "Invalid NULL parameter");
    simcam_stop(&camera->camera);
    if (camera->im.data)
        free(camera->im.data);
    free(camera);
    return Device_Ok;
Error:
    return Device_Err;
}

struct Camera*
simcam_make_camera(enum BasicDeviceKind kind)
{
    struct SimulatedCamera* self = malloc(sizeof(*self));
    EXPECT(self, "Allocation of %llu bytes failed.", sizeof(*self));
    memset(self, 0, sizeof(*self)); // NOLINT
    struct CameraProperties properties = {
        .exposure_time_us = 10000,
        .line_interval_us = 0,
        .readout_direction = Direction_Forward,
        .binning = 1,
        .pixel_type = SampleType_u8,
        .shape = { .x = 1920, .y = 1080 },
        .input_triggers = { .frame_start = { .enable = 0,
                                       .line = 0, // Software
                                       .kind = Signal_Input,
                                       .edge = TriggerEdge_Rising, }, },
    };
    *self = (struct SimulatedCamera){
        .properties = properties,
        .kind=kind,
        .im={
          .data=0,
          .shape = {
            .dims = {
              .channels = 1,
              .width = properties.shape.x,
              .height = properties.shape.y,
              .planes = 1,
            },
            .strides = {
              .channels=1,
              .width=1,
              .height=properties.shape.x,
              .planes=properties.shape.x*properties.shape.y,
            },
            .type=SampleType_u8
          },
        },
        .camera={
          .state = DeviceState_AwaitingConfiguration,
          .set=simcam_set,
          .get=simcam_get,
          .get_meta=simcam_get_meta,
          .get_shape=simcam_get_shape,
          .start=simcam_start,
          .stop=simcam_stop,
          .execute_trigger=simcam_execute_trigger,
          .get_frame=simcam_get_frame
        }
    };
    thread_init(&self->streamer.thread);
    lock_init(&self->im.lock);
    condition_variable_init(&self->im.frame_ready);
    event_init(&self->software_trigger.event);
    CHECK(self->im.data =
            malloc(MAX_IMAGE_WIDTH * MAX_IMAGE_HEIGHT * MAX_BYTES_PER_PIXEL));

    return &self->camera;
Error:
    if (self)
        free(self);
    return 0;
}
