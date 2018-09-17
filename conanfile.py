from conans import ConanFile, CMake, tools

fallthrough_patch = """index 84504427..b62de9f3 100644
--- a/include/msgpack/unpack_template.h
+++ b/include/msgpack/unpack_template.h
@@ -236,6 +236,7 @@ msgpack_unpack_func(int, _execute)(msgpack_unpack_struct(_context)* ctx, const c
 
             _fixed_trail_again:
                 ++p;
+                __attribute__((fallthrough));
 
             default:
                 if((size_t)(pe - p) < trail) { goto _out; }
"""

class MsgpackConan(ConanFile):
    name = "msgpack"
    version = "2.1.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Msgpack here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/msgpack/msgpack-c.git")
        self.run("cd msgpack-c && git checkout tags/cpp-2.1.1")
        tools.patch(base_path="./msgpack-c/", patch_string=fallthrough_patch)
        

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        cmake.definitions["MSGPACK_CXX11"] = "ON"
        cmake.definitions["MSGPACK_BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["MSGPACK_BUILD_TESTS"] = "OFF"
        cmake.verbose = True
        cmake.configure(source_folder="msgpack-c")
        cmake.build()


    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["msgpackc"]

