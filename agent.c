#include "libpyroscope.pyspy.h"
#include <Python.h>
#include <stdio.h>

static PyObject *start(PyObject *self, PyObject *args)
{
    char spy_name[] = "pyspy";
    char *app_name = NULL;
    char *server_address = NULL;
    int with_subprocesses = 0;
    int sample_rate = 0;
    char *auth = NULL;
    char *log_level = NULL;
    int ret = 0;

    ret = PyArg_ParseTuple(args, "sssiis", &app_name, &server_address,
                           &auth, &sample_rate, &with_subprocesses, &log_level);
    if (!ret)
    {
        return Py_BuildValue("i", -1);
    }

    ret = (int)(Start(app_name, spy_name, server_address, auth, sample_rate,
                      with_subprocesses, log_level));
    if (ret)
    {
        return Py_BuildValue("i", ret);
    }

    return Py_BuildValue("i", 0);
}

static PyObject *stop(PyObject *self, PyObject *args)
{
    int ret = -1;

    ret = (int)Stop();
    if (ret)
    {
        return Py_BuildValue("i", ret);
    }

    return Py_BuildValue("i", 0);
}

static PyObject *change_name(PyObject *self, PyObject *args)
{
    const char *app_name = NULL;
    int ret = 0;

    ret = PyArg_ParseTuple(args, "s", &app_name);
    if (!ret)
    {
        return Py_BuildValue("i", -1);
    }

    ret = (int)ChangeName((char *)app_name);
    if (ret)
    {
        return Py_BuildValue("i", ret);
    }
    return Py_BuildValue("i", 0);
}

static PyObject *set_tag(PyObject *self, PyObject *args)
{
    int ret = 0;
    const char *key = NULL;
    const char *val = NULL;

    ret = PyArg_ParseTuple(args, "ss", &key, &val);
    if (!ret)
    {
        return Py_BuildValue("i", -1);
    }

    ret = (int)SetTag((char *)key, (char *)val);
    if (ret)
    {
        return Py_BuildValue("i", ret);
    }

    return Py_BuildValue("i", 0);
}

static PyObject *test_logger(PyObject *self, PyObject *args)
{
    TestLogger();
    return Py_BuildValue("i", 0);
}

static PyObject *set_logger_level(PyObject *self, PyObject *args)
{
    int ret;
    int level = 0;
    ret = PyArg_ParseTuple(args, "i", &level);
    if (!ret)
    {
        return Py_BuildValue("i", -1);
    }
    SetLoggerLevel(level);
    return Py_BuildValue("i", 0);
}

static PyObject *build_summary(PyObject *self, PyObject *args)
{
    char* ret = BuildSummary();
    return Py_BuildValue("s", ret);
}

static struct PyMethodDef agent_methods[] = {
    {"start", start, METH_VARARGS, "Start session"},
    {"stop", stop, METH_O, "Stop session"},
    {"change_name", change_name, METH_VARARGS, "Change application name"},
    {"set_tag", set_tag, METH_VARARGS, "Set tags for the current session"},
    {"test_logger", test_logger, METH_VARARGS, "Test logger"},
    {"set_logger_level", set_logger_level, METH_VARARGS, "Set logger level"},
    {"build_summary", build_summary, METH_VARARGS, "Build summary"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef agent_definition = {PyModuleDef_HEAD_INIT, "agent",
                                              "Pyroscope Python agent", -1,
                                              agent_methods};

PyMODINIT_FUNC PyInit_agent(void)
{
    Py_Initialize();
    return PyModule_Create(&agent_definition);
}
