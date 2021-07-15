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
    int ret = 0;

    ret = PyArg_ParseTuple(args, "sis", &app_name, &pid, &server_address);
    if (!ret)
    {
        return Py_BuildValue("i", -1);
    }

    ret = (int)(Start(app_name, pid, spy_name, server_address));
    if (ret)
    {
        return Py_BuildValue("i", -1);
    }

    return Py_BuildValue("i", 0);
}

static PyObject *stop(PyObject *self, PyObject *args)
{
    // TODO: If not called, we have a leak
    // TODO: For now `pid` is ignored, as we support only single session
    int pid = -1;

    pid = PyLong_AsLong(args);
    if (pid < 0)
    {
        return Py_BuildValue("i", -1);
    }

    Stop(pid);

    return Py_BuildValue("i", 0);
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
