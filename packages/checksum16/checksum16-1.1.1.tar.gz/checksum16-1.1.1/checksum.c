#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <arpa/inet.h>

uint16_t do_csum(uint16_t start_csum, const uint16_t *restrict ptr, size_t len) {
    unsigned long csum = htons(start_csum);
    while (len > 1) {
        csum += *ptr++;
        len -= sizeof(*ptr);
    }
    if (len) {
        csum += *(uint8_t*) ptr;
    }

    // Fold the csum to a uint16_t
    csum = (csum >> 16) + (csum & 0xffff);
    csum += (csum >>16);
    return ntohs((uint16_t)(~csum));
}


static PyObject* calculate_checksum(PyObject* self, PyObject* args) {
    self=self; //unused
    const uint16_t* restrict buffer;
    size_t len;
    uint16_t csum = 0;
    if (!PyArg_ParseTuple(args, "s#|H", &buffer, &len, &csum))
        return NULL;
    csum = do_csum(csum, buffer, len);
    return PyLong_FromLong(csum);
}

static PyMethodDef checksum_methods[] = {
    {"checksum", calculate_checksum, METH_VARARGS,
    "Calculate a checksum of a buffer object"},
    {NULL, NULL, 0, NULL},
};


static struct PyModuleDef checksum_module = {
    PyModuleDef_HEAD_INIT,
    "checksum",
    "Calculate IP checksum of buffers",
    -1,
    checksum_methods,
};

PyMODINIT_FUNC PyInit_checksum(void) {
    return PyModule_Create(&checksum_module);
}
