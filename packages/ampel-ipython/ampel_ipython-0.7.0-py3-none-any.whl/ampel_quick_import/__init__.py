import importlib, glob, os, re, pkg_resources, pathlib
from IPython.core.magic import needs_local_scope, register_line_magic # type: ignore

def _get_module_path(distribution):
	if isinstance(distribution, pkg_resources.EggInfoDistribution):
		return os.path.dirname(distribution.module_path)
	elif isinstance(distribution, pkg_resources.DistInfoDistribution):
		# if the distribution installed a .pth file, assume this points to the editable install
		for line in distribution.get_metadata_lines("RECORD"):
			path, hash, size = line.split(",")
			if path.endswith(".pth"):
				with open(path) as pth:
					return pth.readline().strip()
		# fall back to the importable location (wheel install)
		return distribution.location
	else:
		raise TypeError(f"Unsupported distribution type {type(distribution)} {distribution}")


ampel_folders = {
	_get_module_path(pkg_resources.get_distribution(dist_name)) # type: ignore
	for dist_name in pkg_resources.AvailableDistributions() # type: ignore
	if dist_name.startswith("pyampel") or dist_name.startswith("ampel-")
}


def load_ipython_extension(ipython):
	pass


def clsimport(modname, local_ns=None):

	clsname = modname.split(".")[-1]

	if clsname in globals():
		return

	mod = importlib.import_module(modname)
	cls = getattr(mod, clsname, None)
	if cls:
		local_ns[clsname] = cls
	else:
		print("Module %s does not define class %s" % (modname, clsname))


@register_line_magic
@needs_local_scope
def qi(line, local_ns):
	for el in line.split(" "):
		quickimport(el, local_ns)


def quickimport(clsname, local_ns=None):

	cwd = os.getcwd()
	for d in ampel_folders:
		os.chdir(d)
		a = glob.glob("**/" + clsname + ".py", recursive=True)
		if len(a) != 0:
			s = re.sub(
				".*\.ampel\.", # noqa
				"ampel.",
				a[0] \
					.replace("/", ".") \
					.replace(".py", "")
			)
			print(f"from {s} import {clsname}")
			clsimport(s, local_ns)
			os.chdir(cwd)
			return
	print(f"Class {clsname} not found")
	os.chdir(cwd)
