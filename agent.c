#include <Python.h>
#include <stdio.h>
#include "libpyroscope.pyspy.h"

static PyObject *start(PyObject *self, PyObject *args)
{
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

static PyObject *change_name(PyObject *self, PyObject *args)
{
    const char *name = PyUnicode_AsUTF8(args);
    ChangeName((char *)name);
    Py_RETURN_NONE;
}

static struct PyMethodDef agent_methods[] = {
    {"start", start, METH_VARARGS, "Start session"},
    {"stop", stop, METH_O, "Stop session"},
    {"change_name", change_name, METH_O, "Change session name"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef agent_definition = {
    PyModuleDef_HEAD_INIT, "agent",
    "Pyroscope Python agent", -1, agent_methods};

PyMODINIT_FUNC PyInit_agent(void)
{
    Py_Initialize();
    return PyModule_Create(&agent_definition);
}
