#include <Python.h>
#include <stdio.h>
#include "libpyroscope.pyspy.h"

static PyObject *start(PyObject *self, PyObject *args)
{
    // TODO: Handle kwargs
    char *app_name = NULL;
    char *server_address = NULL;
    int pid = -1;
    char spy_name[] = "pyspy";

    // TODO: Error handling
    PyArg_ParseTuple(args, "sis", &app_name, &pid, &server_address);

    printf("Called start() with: %s %d %s\n", app_name, pid, server_address);

    int ret = Start(app_name, pid, spy_name, server_address);

    if (ret)
    {
        printf("Error occurred!\n");
    }

    Py_RETURN_NONE;
}

static PyObject *stop(PyObject *self, PyObject *args)
{
    int pid = -1;
    printf("Called stop()\n");
    Py_RETURN_NONE;
}

static struct PyMethodDef agent_methods[] = {
    {"start", start, METH_VARARGS, "Start session"},
    {"stop", stop, METH_O, "Stop session"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef agent_definition = {
    PyModuleDef_HEAD_INIT, "agent",
    "Provides API for Pyroscope Python agent", -1, agent_methods};

PyMODINIT_FUNC PyInit_agent(void)
{
    Py_Initialize();
    return PyModule_Create(&agent_definition);
}
