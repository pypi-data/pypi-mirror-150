import os
from setuptools import setup, find_packages, Extension
import numpy as np
try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None


# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions

extensions = [
    Extension("cymorph.__init__", ["src/cymorph/__init__.pyx"]),
    Extension("cymorph.cython_asymmetry", ["src/cymorph/cython_asymmetry.pyx"]),
    Extension("cymorph.cython_entropy", ["src/cymorph/cython_entropy.pyx"]),
    Extension("cymorph.cython_g2", ["src/cymorph/cython_g2.pyx"]),
    Extension("cymorph.cython_smoothness", ["src/cymorph/cython_smoothness.pyx"])
]

CYTHONIZE = bool(int(os.getenv("CYTHONIZE", 0))) or cythonize is not None

if CYTHONIZE:
    compiler_directives = {"language_level": 3, "embedsignature": True}
    extensions = cythonize(extensions, compiler_directives=compiler_directives)
else:
    extensions = no_cythonize(extensions)


INSTALL_REQUIRES = [
    'numpy >= 1.22.1',
    'scipy >= 1.7.3',
    'matplotlib >= 3.5.1',
    'seaborn >= 0.11.2',
    'sep >= 1.2.0'
]

setup(
    include_dirs=[np.get_include()],
    ext_modules=extensions,
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "docs": ["sphinx", "sphinx-rtd-theme"]
    },
)