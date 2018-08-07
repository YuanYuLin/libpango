import ops
import iopc

TARBALL_FILE="pango-1.42.1.tar.xz"
TARBALL_DIR="pango-1.42.1"
INSTALL_DIR="pango-bin"
pkg_path = ""
output_dir = ""
tarball_pkg = ""
tarball_dir = ""
install_dir = ""
install_tmp_dir = ""
cc_host = ""
dst_include_dir = ""
dst_lib_dir = ""
src_pkgconfig_dir = ""
dst_pkgconfig_dir = ""

def set_global(args):
    global pkg_path
    global output_dir
    global tarball_pkg
    global install_dir
    global install_tmp_dir
    global tarball_dir
    global cc_host
    global dst_include_dir
    global dst_lib_dir
    global src_pkgconfig_dir
    global dst_pkgconfig_dir
    global dst_usr_local_lib_dir
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    tarball_pkg = ops.path_join(pkg_path, TARBALL_FILE)
    install_dir = ops.path_join(output_dir, INSTALL_DIR)
    install_tmp_dir = ops.path_join(output_dir, INSTALL_DIR + "-tmp")
    tarball_dir = ops.path_join(output_dir, TARBALL_DIR)
    cc_host_str = ops.getEnv("CROSS_COMPILE")
    cc_host = cc_host_str[:len(cc_host_str) - 1]
    dst_include_dir = ops.path_join(output_dir, ops.path_join("include",args["pkg_name"]))
    dst_lib_dir = ops.path_join(install_dir, "lib")
    dst_usr_local_lib_dir = ops.path_join(install_dir, "usr/local/lib")
    src_pkgconfig_dir = ops.path_join(pkg_path, "pkgconfig")
    dst_pkgconfig_dir = ops.path_join(install_dir, "pkgconfig")

def MAIN_ENV(args):
    set_global(args)

    ops.exportEnv(ops.setEnv("CC", ops.getEnv("CROSS_COMPILE") + "gcc"))
    ops.exportEnv(ops.setEnv("CXX", ops.getEnv("CROSS_COMPILE") + "g++"))
    ops.exportEnv(ops.setEnv("CROSS", ops.getEnv("CROSS_COMPILE")))
    ops.exportEnv(ops.setEnv("DESTDIR", install_tmp_dir))
    ops.exportEnv(ops.addEnv("PATH", ops.path_join(install_tmp_dir, "usr/local/bin")))

    cc_sysroot = ops.getEnv("CC_SYSROOT")

    cflags = ""
    cflags += " -I" + ops.path_join(cc_sysroot, 'usr/include')
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), 'usr/include/libpng')

    ldflags = ""
    ldflags += " -L" + ops.path_join(cc_sysroot, 'lib')
    ldflags += " -L" + ops.path_join(cc_sysroot, 'usr/lib')
    ldflags += " -L" + ops.path_join(iopc.getSdkPath(), 'lib')
    ldflags += " -L" + ops.path_join(iopc.getSdkPath(), 'usr/lib')

    libs = ""
    libs += " -lpng -lz"

    #ops.exportEnv(ops.setEnv("LDFLAGS", ldflags))
    #ops.exportEnv(ops.setEnv("CFLAGS", cflags))
    #ops.exportEnv(ops.setEnv("LIBS", libs))
    #extra_conf.append('CFLAGS="-I' + ops.path_join(iopc.getSdkPath(), 'usr/include/libz') + '"')

    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.unTarXz(tarball_pkg, output_dir)
    #ops.copyto(ops.path_join(pkg_path, "finit.conf"), output_dir)

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(tarball_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)

    print "SDK include path:" + iopc.getSdkPath()

    extra_conf = []
    extra_conf.append("--host=" + cc_host)
    extra_conf.append("--disable-gtk-doc")

    cflags = ""
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libcairo")
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libglib")
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libglib/glib-2.0")
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/fontconfig")
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libharfbuzz")
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libharfbuzz/harfbuzz")
    extra_conf.append("CAIRO_CFLAGS=" + cflags)
    extra_conf.append("GLIB_CFLAGS=" + cflags)
    extra_conf.append("FONTCONFIG_CFLAGS=" + cflags)
    extra_conf.append("FREETYPE_CFLAGS=" + cflags)
    extra_conf.append("HARFBUZZ_CFLAGS=" + cflags)
    libs = ""
    libs += " -L" + ops.path_join(iopc.getSdkPath(), "lib") 
    libs += " -lcairo -lglib-2.0 -lfontconfig -lfreetype"
    libs += " -lharfbuzz -lharfbuzz-subset -lharfbuzz-icu"
    extra_conf.append("CAIRO_LIBS=" + libs)
    extra_conf.append("GLIB_LIBS=" + libs)
    extra_conf.append("FONTCONFIG_LIBS=" + libs)
    extra_conf.append("FREETYPE_LIBS=" + libs)
    extra_conf.append("HARFBUZZ_LIBS=" + libs)
    '''
    extra_conf.append("--without-libjpeg")
    extra_conf.append("--without-libtiff")
    extra_conf.append("--disable-glibtest")

    cflags = ""
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libxml2") 
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libglib/glib-2.0") 
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libglib/gio-unix-2.0") 
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libglib")
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), "usr/include/libpcre3")
    cflags += " -I" + ops.path_join(iopc.getSdkPath(), 'usr/include/libpng')
    extra_conf.append("BASE_DEPENDENCIES_CFLAGS=" + cflags)
    extra_conf.append("GLIB_CFLAGS=" + cflags)
    extra_conf.append("CFLAGS=" + cflags)

    libs = ""
    libs += " -L" + ops.path_join(iopc.getSdkPath(), "lib") 
    libs += " -lxml2 -lglib-2.0 -lpng -lz"
    extra_conf.append("BASE_DEPENDENCIES_LIBS=" + libs)
    extra_conf.append("GLIB_LIBS=" + libs)
    extra_conf.append("LIBS=" + libs)

    extra_conf.append("--disable-libmount")
    extra_conf.append("--disable-fam")
    extra_conf.append("--with-pcre=system")
    extra_conf.append('ZLIB_CFLAGS="-I' + ops.path_join(iopc.getSdkPath(), 'usr/include/libz') + '"')
    extra_conf.append('ZLIB_LIBS="-L' + ops.path_join(iopc.getSdkPath(), 'lib') + ' -lz"')
    extra_conf.append('LIBFFI_CFLAGS="-I' + ops.path_join(iopc.getSdkPath(), 'usr/include/libffi') + '"')
    extra_conf.append('LIBFFI_LIBS="-L' + ops.path_join(iopc.getSdkPath(), 'usr/lib') + ' -lffi"')
    extra_conf.append('PCRE_CFLAGS="-I' + ops.path_join(iopc.getSdkPath(), 'usr/include/libpcre3') + '"')
    extra_conf.append('PCRE_LIBS="-L' + ops.path_join(iopc.getSdkPath(), 'lib') + ' -lpcre"')
    extra_conf.append("glib_cv_stack_grows=no")
    extra_conf.append("glib_cv_uscore=no")
    extra_conf.append("glib_cv_pcre_has_unicode=yes")
    '''

    iopc.configure(tarball_dir, extra_conf)

    return True

def MAIN_BUILD(args):
    set_global(args)

    ops.mkdir(install_dir)
    ops.mkdir(install_tmp_dir)
    iopc.make(tarball_dir)
    iopc.make_install(tarball_dir)

    ops.mkdir(dst_lib_dir)

    libgdk_pixbuf = "libgdk_pixbuf-2.0.so.0.3612.0"
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/" + libgdk_pixbuf), dst_lib_dir)
    ops.ln(dst_lib_dir, libgdk_pixbuf, "libgdk_pixbuf-2.0.so.0.3612")
    ops.ln(dst_lib_dir, libgdk_pixbuf, "libgdk_pixbuf-2.0.so.0")
    ops.ln(dst_lib_dir, libgdk_pixbuf, "libgdk_pixbuf-2.0.so")

    dst_gdk_loader_dir = ops.path_join(dst_usr_local_lib_dir, "gdk-pixbuf-2.0/2.10.0/loaders/")
    ops.mkdir(dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-ani.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-bmp.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-gif.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-icns.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-ico.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-png.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-pnm.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-qtif.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-tga.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-xbm.so"), dst_gdk_loader_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-xpm.so"), dst_gdk_loader_dir)

    ops.mkdir(dst_include_dir)
    ops.copyto(ops.path_join(install_tmp_dir, "usr/local/include/."), dst_include_dir)

    ops.mkdir(dst_pkgconfig_dir)
    ops.copyto(ops.path_join(src_pkgconfig_dir, '.'), dst_pkgconfig_dir)

    return False

def MAIN_INSTALL(args):
    set_global(args)

    iopc.installBin(args["pkg_name"], ops.path_join(dst_lib_dir, "."), "lib")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_usr_local_lib_dir, "."), "usr/local/lib")
    iopc.installBin(args["pkg_name"], dst_include_dir, "include")
    iopc.installBin(args["pkg_name"], ops.path_join(dst_pkgconfig_dir, '.'), "pkgconfig")

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)

    return False

def MAIN(args):
    set_global(args)

