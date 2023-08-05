#include "filter.h"

static PyObject*
_saturation_apply(PyObject *self, PyObject *args)
{
    PyObject *buffer = NULL;
    float changeVal;
    char *image_mode_str;

    if (!PyArg_ParseTuple(args, "sfO:apply", &image_mode_str, &changeVal, &buffer)) {
        return NULL;
    }

    Py_ssize_t size = PyBytes_Size(buffer);
    unsigned char *ptr = (unsigned char *) PyBytes_AsString(buffer);

    int num_bytes = bytes_per_pixel(image_mode_str);

    int r_idx = rgb_order(image_mode_str, 'R'),
        g_idx = rgb_order(image_mode_str, 'G'),
        b_idx = rgb_order(image_mode_str, 'B'),
        i = 0, r, g, b;


    float p;
    size -= num_bytes;
    for (; i <= size; i += num_bytes) {
        r = ptr[i + r_idx];
        g = ptr[i + g_idx];
        b = ptr[i + b_idx];

        // Magic conversions borrowed from http://alienryderflex.com/saturation.html
        p = sqrt( r*r*0.299 + g*g*0.587 + b*b*0.114 );

        r = p + ( r - p ) * changeVal;
        g = p + ( g - p ) * changeVal;
        b = p + ( b - p ) * changeVal;

        ptr[i + r_idx] = ADJUST_COLOR(r);
        ptr[i + g_idx] = ADJUST_COLOR(g);
        ptr[i + b_idx] = ADJUST_COLOR(b);
    }

    Py_INCREF(buffer);
    return buffer;
}

FILTER_MODULE(_saturation,
    "apply(image_mode, change, buffer) -> string"
)
