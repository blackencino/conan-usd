from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os

class USDConan(ConanFile):
    name = "usd"
    version = "21.02"
    license = "Modified Apache 2.0 License"
    homepage = "http://openusd.org/"
    url = "https://github.com/PixarAnimationStudios/USD.git"
    description = "Universal Scene Description (USD) is an efficient, " \
        "scalable system for authoring, reading, and streaming " \
        "time-sampled scene description for interchange between " \
        "graphics applications."
    topics = ("conan", "usd", "geometry", "pointcloud", "mesh", "vfx", "pixar")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False]
        }
    default_options = {
        "shared": True,
        "*:fPIC": True
        }
    generators = "cmake", "cmake_find_package", "cmake_paths", "virtualenv", \
        "virtualbuildenv", "virtualrunenv"
    exports_sources = ["CMakeLists.txt", "patches/*"]

    requires = (
        "boost/1.74.0",
        "openexr/2.5.3",
        "alembic/1.7.16@blackencino/latest",
        "draco/1.3.6",
        "tbb/2020.0",
        "hdf5/1.12.0",
        "zlib/1.2.11"
    )

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        pass

    def configure(self):
        if not self.options.shared:
            raise ConanInvalidConfiguration("USD only supports shared=True at this time")

    def requirements(self):
        self.options["tbb"].tbbmalloc = False
        self.options["tbb"].tbbproxy = False
        self.options["tbb"].shared = True

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        #tools.untargz("C:\\Users\\TM-Z8\\Downloads\\USD-21.02.tar.gz")
        tools.patch(patch_file="patches/USD-21.02.patch",
                    base_path="USD-{}".format(self.version))
        os.rename("USD-{}".format(self.version), self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)

        self._cmake.definitions["PXR_STRICT_BUILD_MODE"] = False
        self._cmake.definitions["PXR_VALIDATE_GENERATED_CODE"] = False
        self._cmake.definitions["PXR_HEADLESS_TEST_MODE"] = True
        self._cmake.definitions["PXR_BUILD_TESTS"] = False
        self._cmake.definitions["PXR_BUILD_EXAMPLES"] = False
        self._cmake.definitions["PXR_BUILD_TUTORIALS"] = False
        self._cmake.definitions["PXR_BUILD_USD_TOOLS"] = False
        self._cmake.definitions["PXR_BUILD_IMAGING"] = False
        self._cmake.definitions["PXR_BUILD_EMBREE_PLUGIN"] = False
        self._cmake.definitions["PXR_BUILD_OPENIMAGEIO_PLUGIN"] = False
        self._cmake.definitions["PXR_BUILD_OPENCOLORIO_PLUGIN"] = False
        self._cmake.definitions["PXR_BUILD_USD_IMAGING"] = False
        self._cmake.definitions["PXR_BUILD_USDVIEW"] = False
        self._cmake.definitions["PXR_BUILD_ALEMBIC_PLUGIN"] = True
        self._cmake.definitions["PXR_BUILD_DRACO_PLUGIN"] = True
        self._cmake.definitions["PXR_BUILD_PRMAN_PLUGIN"] = False
        self._cmake.definitions["PXR_BUILD_MATERIALX_PLUGIN"] = False
        self._cmake.definitions["PXR_ENABLE_MATERIALX_IMAGING_SUPPORT"] = False
        self._cmake.definitions["PXR_BUILD_DOCUMENTATION"] = False
        self._cmake.definitions["PXR_ENABLE_PYTHON_SUPPORT"] = False
        self._cmake.definitions["PXR_USE_PYTHON_3"] = False
        self._cmake.definitions["PXR_ENABLE_HDF5_SUPPORT"] = True
        self._cmake.definitions["PXR_ENABLE_OSL_SUPPORT"] = False
        self._cmake.definitions["PXR_ENABLE_PTEX_SUPPORT"] = False
        self._cmake.definitions["PXR_ENABLE_OPENVDB_SUPPORT"] = False
        self._cmake.definitions["PXR_ENABLE_NAMESPACES"] = True
        self._cmake.definitions["PXR_PREFER_SAFETY_OVER_SPEED"] = True
        self._cmake.definitions["PXR_USE_AR_2"] = False
        self._cmake.definitions["PXR_ENABLE_METAL_SUPPORT"] = False
        self._cmake.definitions["PXR_ENABLE_VULKAN_SUPPORT"] = False
        self._cmake.definitions["PXR_ENABLE_GL_SUPPORT"] = False
        self._cmake.definitions["PXR_ENABLE_PRECOMPILED_HEADERS"] = True
        self._cmake.definitions["BUILD_SHARED_LIBS"] = True
        self._cmake.definitions["PXR_BUILD_MONOLITHIC"] = False

        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.txt", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "usd"
        self.cpp_info.names["cmake_find_package_multi"] = "usd"
        self.cpp_info.names["pkg_config"] = "usd"

        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.system_libs.append("Shlwapi.lib")
            self.cpp_info.system_libs.append("Dbghelp.lib") 
            self.cpp_info.system_libs.append("Ws2_32.lib")
        if not self.options.shared:
            self.cpp_info.defines.append("PXR_STATIC")

        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.PATH.append(os.path.join(self.package_folder, "lib"))
        self.env_info.PXR_PLUGINPATH_NAME = os.path.join(self.package_folder, "lib", "usd")





