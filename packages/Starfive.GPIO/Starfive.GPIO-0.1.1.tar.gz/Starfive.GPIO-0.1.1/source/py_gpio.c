/*
Copyright (c) 2022-2027 Starfive

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include "Python.h"
#include "SHTC3_dev.h"

// python function SensorCheck()
static PyObject *py_SensorCheck(PyObject *self, PyObject *args)
{
   int ret = 0;
   PyObject *Opy;
   
   ret = SHTC3_SensorCheck();
   Opy = Py_BuildValue("i", ret);
   
   return Opy;
}


// python function softreset()
static PyObject *py_softreset(PyObject *self, PyObject *args)
{
   SHTC_SOFT_RESET();
   Py_RETURN_NONE;
}

// python function getTemperature()
static PyObject *py_getTem(PyObject *self, PyObject *args)
{
	float Tdata[2]= {0};
	PyObject *Opy;

	SHTC3_Read_DATA(Tdata);
	SHTC3_SLEEP();
	SHTC3_WAKEUP();
	Opy = Py_BuildValue("f", Tdata[0]);

	return Opy;
}

// python function getHumidity()
static PyObject *py_getHum(PyObject *self, PyObject *args)
{
	float Tdata[2]= {0};
	PyObject *Opy;

	SHTC3_Read_DATA(Tdata);
	SHTC3_SLEEP();
	SHTC3_WAKEUP();
	Opy = Py_BuildValue("f", Tdata[1]);

	return Opy;
}

static const char moduledocstring[] = "Python GPIO module for starfive";

PyMethodDef sfv_gpio_methods[] = {
   {"SensorCheck", py_SensorCheck, METH_VARARGS, "Check if sensor is exit"},
   {"softreset", py_softreset, METH_VARARGS, "Sensor soft reset"},
   {"getTem", py_getTem, METH_VARARGS, "Get temperature"},
   {"getHum", py_getHum, METH_VARARGS, "Get humidity"},
   {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION > 2
static struct PyModuleDef sfvgpiomodule = {
   PyModuleDef_HEAD_INIT,
   "Starfive._GPIO",      // name of module
   moduledocstring,
   -1,
   sfv_gpio_methods
};
#endif

#if PY_MAJOR_VERSION > 2
PyMODINIT_FUNC PyInit__GPIO(void)
#else
PyMODINIT_FUNC init_GPIO(void)
#endif
{
   PyObject *module = NULL;

#if PY_MAJOR_VERSION > 2
   if ((module = PyModule_Create(&sfvgpiomodule)) == NULL)
      return NULL;
#else
   if ((module = Py_InitModule3("Starfive._GPIO", sfv_gpio_methods, moduledocstring)) == NULL)
      return;
#endif

#if PY_MAJOR_VERSION > 2
   return module;
#else
   return;
#endif
}
