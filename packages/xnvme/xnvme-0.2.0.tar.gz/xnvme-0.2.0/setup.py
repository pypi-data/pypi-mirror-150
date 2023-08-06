import os
import shutil
import sys

from setuptools import find_packages, setup

LIB_PXD = "libxnvme.pxd"
PACKAGE_NAME = "xnvme"
# setup.py expects to be executed in current working dir, so '../../' would in the Git
# repo point to the root.
WORKSPACE_ROOT = os.environ.get("PY_XNVME_WORKSPACE_ROOT", "../../")
VERSION = "0.2.0"

if "sdist" in sys.argv:
    import autopxd  # Only needed when building

    cy_xnvme_pkg_path = f"{WORKSPACE_ROOT}/toolbox/cy_xnvme_pkg/"
    os.chdir(cy_xnvme_pkg_path)

    # c_include_path = os.path.join("../../", "include")
    c_include_path = os.path.join(WORKSPACE_ROOT, "include")

    regex = [
        r"s/SLIST_ENTRY\(xnvme_sgl\)/struct{struct xnvme_sgl *sle_next;}/g",
        r"s/SLIST_HEAD\(, xnvme_sgl\)/struct{struct xnvme_sgl *slh_first;}/g",
        r"s/SLIST_ENTRY\(xnvme_cmd_ctx\)/struct{struct xnvme_cmd_ctx *sle_next;}/g",
        r"s/SLIST_HEAD\(, xnvme_cmd_ctx\)/struct{struct xnvme_cmd_ctx *slh_first;}/g",
        r"s/FILE\s?\*/void */g",
        r"s/struct iovec\s?\*/void */g",
        # NOTE: Cython doesn't support arrays without length specified
        r"s/xnvme_be_attr item\[\]/xnvme_be_attr item[1]/g",
        # 's/xnvme_be_attr item\[\]/xnvme_be_attr *item/g',
        r"s/xnvme_ident entries\[\]/xnvme_ident entries[1]/g",
        # 's/xnvme_ident entries\[\]/xnvme_ident *entries/g',
    ]
    extra_cpp_args = [
        f"-I{c_include_path}",
        f'-I{os.path.join(WORKSPACE_ROOT, "third-party/windows/")}',
    ]

    LIB_PXD_PATH = f"{cy_xnvme_pkg_path}{PACKAGE_NAME}/{LIB_PXD}"

    with open(LIB_PXD_PATH, "w") as f_out:
        for h_file in ["libxnvme.h", "libxnvme_nvm.h", "libxnvme_pp.h"]:
            h_path = os.path.join(c_include_path, h_file)
            with open(h_path, "r") as f_in:
                f_out.write(
                    autopxd.translate(
                        f_in.read(),
                        h_file,
                        extra_cpp_args,
                        debug=False,
                        regex=regex,
                    )
                )


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Mads Ynddal",
    author_email="m.ynddal@samsung.com",
    url="https://github.com/OpenMPDK/xNVMe",
    classifiers=[
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    package_data={"": [LIB_PXD]},
    include_package_data=True,
)

if "sdist" in sys.argv:
    # Copy to build directory
    package_file = f'{PACKAGE_NAME}-{VERSION.strip("v")}.tar.gz'
    shutil.copyfile(
        "dist/" + package_file,
        WORKSPACE_ROOT + "/builddir/toolbox/cy_xnvme_pkg/" + package_file,
    )
