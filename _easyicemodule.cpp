#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <libeasyice.h>

static PyObject *_easyice_process_ts_file(PyObject *self, PyObject *args,
                                          PyObject *kwds)
{
  char *mrl;
  static const char *kwlist[] = {"mrl", NULL};
  // '$' 表示后面是 keyword arguments only, kw 默认是可选的.

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "$s", (char **)kwlist, &mrl))
  {
    return NULL;
  }
  printf("process mrl %s\n", mrl);
  easyice_global_init();
  EASYICE *handle = easyice_init();
  easyice_setopt(handle, EASYICEOPT_MRL, mrl);
  int ret_code = easyice_process(handle);
  if (ret_code != EASYICECODE_OK)
  {
  }
  easyice_cleanup(handle);
  easyice_global_cleanup();
  return PyBool_FromLong(ret_code);
}

void _easyice_udplive_callback(UDPLIVE_CALLBACK_TYPE type, const char *json, void *pApp)
{
  // printf("type=%d,content=%s,pApp=%s\n", type, json, (char *)pApp);
  printf("[UDPLIVE][Type=%d]. 调用 callback:%p\n", type, pApp);
  PyGILState_STATE state = PyGILState_Ensure();
  PyObject *args = Py_BuildValue("(is)", type, json);
  // _PyObject_Dump(args);
  PyObject *ret = PyObject_CallObject((PyObject *)pApp, args);
  if (ret == NULL)
  {
    printf("Failed to call callback\n");
    PyErr_Print();
  }
  PyGILState_Release(state);
}

static PyObject *_easyice_process_udplive(PyObject *self, PyObject *args,
                                          PyObject *kwds)
{
  char *mrl;
  PyObject *callback;
  long cb_update_interval = 1000000;  // 1s
  long calctsrate_interval_ms = 1000; // 1s
  static const char *kwlist[] = {"mrl", "callback", "cb_update_interval", "calctsrate_interval_ms", NULL};
  // '$' 表示后面是 keyword arguments only, kw 默认是可选的.

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "$sOii", (char **)kwlist, &mrl, &callback, &cb_update_interval, &calctsrate_interval_ms))
  {
    return NULL;
  }
  if (!PyCallable_Check(callback))
  {
    PyErr_SetString(PyExc_TypeError, "callback参数必须是可调用的");
    return NULL;
  }

  printf("process mrl %s\n", mrl);
  easyice_global_init();
  EASYICE *handle = easyice_init();
  easyice_setopt(handle, EASYICEOPT_MRL, (void *)mrl);
  // easyice_setopt(handle, EASYICEOPT_MRL, (void *)"udp://127.0.0.1:1234");
  easyice_setopt(handle, EASYICEOPT_UDPLIVE_LOCAL_IP, (void *)"0.0.0.0");
  easyice_setopt(handle, EASYICEOPT_UDPLIVE_FUNCTION, (void *)_easyice_udplive_callback);
  easyice_setopt(handle, EASYICEOPT_UDPLIVE_DATA, (void *)callback);

  //设置回调函数调用间隔周期
  easyice_setopt(handle, EASYICEOPT_UDPLIVE_CB_UPDATE_INTERVAL, (void *)cb_update_interval); //1s

  //设置计算 tsRate 的间隔周期，支持检测期间动态调整
  easyice_setopt(handle, EASYICEOPT_UDPLIVE_CALCTSRATE_INTERVAL, (void *)calctsrate_interval_ms); //1
  int ret_code = easyice_process(handle);
  if (ret_code != EASYICECODE_OK)
  {
    easyice_cleanup(handle);
    easyice_global_cleanup();
    PyErr_SetString(PyExc_Exception, "任务启动出错");
    return NULL;
  }

  return PyLong_FromVoidPtr((void *)handle);
}

static PyObject *_easyice_cleanup(PyObject *self, PyObject *obj)
{
  void *ptr = PyLong_AsVoidPtr(obj);
  EASYICE *handle = (EASYICE *)ptr;
  easyice_cleanup(handle);
  easyice_global_cleanup();
  Py_RETURN_NONE;
}

static PyMethodDef _easyice_methods[] = {
    {.ml_name = "process_ts_file",
     .ml_meth = (PyCFunction)(_easyice_process_ts_file),
     .ml_flags = METH_KEYWORDS | METH_VARARGS,
     .ml_doc = "easyice_process process ts file write json file"},
    {.ml_name = "process_udplive",
     .ml_meth = (PyCFunction)(_easyice_process_udplive),
     .ml_flags = METH_KEYWORDS | METH_VARARGS,
     .ml_doc = "easyice_process process udplive"},
    {.ml_name = "cleanup", .ml_meth = (PyCFunction)_easyice_cleanup, .ml_flags = METH_O, .ml_doc = "easyice cleanup handle"},
    {NULL, NULL, 0, NULL} /* Sentinel*/
};

static struct PyModuleDef _easyice_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "_easyice",
    .m_doc = "libeasyice light wrapper module",
    .m_size = -1,
    .m_methods = _easyice_methods,
};

PyMODINIT_FUNC PyInit__easyice(void)
{
  PyObject *m = PyModule_Create(&_easyice_module);
  if (!m)
  {
    return NULL;
  }
  // 这里可以进行其他的操作
  return m;
}