#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <libeasyice.h>

;

static PyObject *_easyice_process(PyObject *self, PyObject *args,
                                  PyObject *kwds)
{
  char* mrl;
  static  char *kwlist[] = {"mrl", NULL};
  // '$' 表示后面是 keyword arguments only, kw 默认是可选的.

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "$s", kwlist, &mrl))
  {
    return NULL;
  }
  printf("process mrl %s\n", mrl);
  easyice_global_init();
  EASYICE* handle = easyice_init();
  easyice_setopt(handle, EASYICEOPT_MRL, mrl);
  int ret_code = easyice_process(handle);
  if (ret_code != EASYICECODE_OK)
  {
  }
  easyice_cleanup(handle);
  easyice_global_cleanup();
  return PyBool_FromLong(ret_code);
}

static PyMethodDef _easyice_methods[] = {
    {.ml_name = "easyice_process",
     .ml_meth = (PyCFunction)(_easyice_process),
     .ml_flags = METH_KEYWORDS | METH_VARARGS,
     .ml_doc = "easyice_process process ts file write json file"},
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