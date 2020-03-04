from conans import ConanFile, CMake, tools
import os

class Open62541Conan(ConanFile):
    name = "open62541"
    description = "open62541 (http://open62541.org) is an open source and free implementation of OPC UA " \
                  "(OPC Unified Architecture) written in the common subset of the C99 and C++98 languages"
    topics = ("conan", "open62541", "opcua", "iec62541")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/open62541/open62541"
    license = "	MPL-2.0"

    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    short_paths = True

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])  
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
#       tools.replace_in_file(
#            os.path.join(self._source_subfolder, "CMakeLists.txt"),
#            "project(open62541)", """project(open62541)
#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()""")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False  # example
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        #tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "-Werror", "")
        cmake = self._configure_cmake()
        cmake.build()
        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.libs = ["open62541"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32")
        self.cpp_info.defines.append("UA_NO_AMALGAMATION")
        if self.options.shared and self.settings.os == "Windows":
            self.cpp_info.bindirs.append(self.package_folder)