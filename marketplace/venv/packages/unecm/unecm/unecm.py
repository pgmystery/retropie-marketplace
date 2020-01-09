# -*- coding: utf-8 -*-
import os
import threading
import ctypes


root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
unecm_library_path = os.path.join(root_dir, "unecm.so")
unecm = ctypes.CDLL(unecm_library_path)


def process(infilename="", outfilename=None, oldfilename=None, update_callback=None):
	if len(infilename) == 0:
		return False

	args = [infilename]
	if outfilename:
		args.append(outfilename)
	if oldfilename:
		args.append(oldfilename)

	unecm.main.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
	cargs = (ctypes.c_char_p * (len(args)))(*tuple(args))

	t = None
	if update_callback:
		t = threading.Thread(target=_update_callback, args=(update_callback,))
		t.start()

	result = unecm.main(ctypes.c_int(len(args)), cargs)

	if update_callback:
		t.do_run = False
		t.join()

	if result == 0:
		return True
	else:
		return False

def _update_callback(callback):
	old_int = -1
	t = threading.currentThread()
	while getattr(t, "do_run", True):
		try:
			progress_value = ctypes.c_int.in_dll(unecm, "progress").value
			if old_int != progress_value:
				callback(progress_value)
				old_int = progress_value
		except:
			break
