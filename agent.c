#include <Python.h>
#include <stdio.h>
#include "libpyroscope.pyspy.h"

static PyObject *start(PyObject *self, PyObject *args)
{
    char *app_name = NULL;
    char *server_address = NULL;
    int pid = -1;
    char spy_name[] = "pyspy";
    char auth[] = "";
    char log_level[] = "debug";
    int ret = 0;

    ret = PyArg_ParseTuple(args, "sis", &app_name, &pid, &server_address);
    if (!ret)
    {
        return Py_BuildValue("i", -1);
    }
//TODO: Adapt
    ret = (int)(Start(app_name, pid, spy_name, server_address, auth, 100, 1, log_level));
    if (ret)
    {
        return Py_BuildValue("i", ret);
    }

    return Py_BuildValue("i", 0);
}

static PyObject *stop(PyObject *self, PyObject *args)
{
    int pid = -1;
    int ret = -1;

    pid = PyLong_AsLong(args);
    if (pid < 0)
    {
        return Py_BuildValue("i", -1);
    }

    ret = (int)Stop(pid);
    if (ret)
    {
        return Py_BuildValue("i", ret);
    }

    return Py_BuildValue("i", 0);
}

static PyObject *change_name(PyObject *self, PyObject *args)
{
    const char *app_name = NULL;
    int pid = -1;
    int ret = 0;

    ret = PyArg_ParseTuple(args, "si", &app_name, &pid);
    if (!ret)
    {
        return Py_BuildValue("i", -1);
    }

    ret = (int)ChangeName((char *)app_name, pid);
    if (ret)
    {
        return Py_BuildValue("i", ret);
    }
    return Py_BuildValue("i", 0);
}

static struct PyMethodDef agent_methods[] = {
    {"start", start, METH_VARARGS, "Start session"},
    {"stop", stop, METH_O, "Stop session"},
    {"change_name", change_name, METH_VARARGS, "Change session name"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef agent_definition = {
    PyModuleDef_HEAD_INIT, "agent",
    "Pyroscope Python agent", -1, agent_methods};

PyMODINIT_FUNC PyInit_agent(void)
{
    Py_Initialize();
    return PyModule_Create(&agent_definition);
}
