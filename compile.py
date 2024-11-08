from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
extensions = [
    Extension("car_accident_detect", ["lib/car_accident_detect.py"]),
    Extension("traffic_count", ["lib/traffic_count.py"]),
    Extension("object_detection", ["lib/object_detection.py"]),
    Extension("decrypt", ["lib/decrypt.py"]),
    Extension("utils", ["lib/utils.py"])
]
setup(
    name="AI_server",
    ext_modules=cythonize(extensions,exclude=['lib/deep_sort_pytorch', 'lib/ByteTrack']))
