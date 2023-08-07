# Tests

TuxRun support some tests, each tests is supported on some but not all architectures.

!!! tip "Listing tests"
    You can list the supported tests with:
    ```shell
    tuxrun --list-tests
    ```

## FVP AEMvA device

The following tests are supported by the default root filesystem.

Device    | Tests               | Parameters |
----------|---------------------|------------|
fvp-aemva | command             |            |
fvp-aemva | kselftest-gpio      |  KSELFTEST |
fvp-aemva | kselftest-ipc       |  KSELFTEST |
fvp-aemva | kselftest-ir        |  KSELFTEST |
fvp-aemva | kselftest-kcmp      |  KSELFTEST |
fvp-aemva | kselftest-kexec     |  KSELFTEST |
fvp-aemva | kselftest-rseq      |  KSELFTEST |
fvp-aemva | kselftest-rtc       |  KSELFTEST |
fvp-aemva | kunit\*             |            |
fvp-aemva | ltp-fcntl-locktests |            |
fvp-aemva | ltp-fs_bind         |            |
fvp-aemva | ltp-fs_perms_simple |            |
fvp-aemva | ltp-fsx             |            |
fvp-aemva | ltp-nptl            |            |
fvp-aemva | ltp-smoke           |            |
fvp-aemva | perf                |            |

The following tests are not supported by the default root filesystem. You should
provide a custom root filesystem.

Device    | Tests               |
----------|---------------------|
fvp-aemva | ltp-cap_bounds      |
fvp-aemva | ltp-commands        |
fvp-aemva | ltp-containers      |
fvp-aemva | ltp-crypto          |
fvp-aemva | ltp-cve             |
fvp-aemva | ltp-filecaps        |
fvp-aemva | ltp-fs              |
fvp-aemva | ltp-hugetlb         |
fvp-aemva | ltp-io              |
fvp-aemva | ltp-ipc             |
fvp-aemva | ltp-math            |
fvp-aemva | ltp-mm              |
fvp-aemva | ltp-pty             |
fvp-aemva | ltp-sched           |
fvp-aemva | ltp-securebits      |
fvp-aemva | ltp-syscalls        |
fvp-aemva | ltp-tracing         |

!!! tip "Passing parameters"
    In order to pass parameters, use `tuxrun --parameters KSELFTEST=http://.../kselftes.tar.xz`

!!! warning "KUnit config"
    In order to run KUnit tests, the kernel should be compiled with
    ```
    CONFIG_KUNIT=m
    CONFIG_KUNIT_ALL_TESTS=m
    ```
    The **modules.tar.xz** should be given with `--modules https://.../modules.tar.xz`.


## FVP Modello devices

Device              | Tests        | Parameters                       |
--------------------|--------------|----------------------------------|
fvp-morello-android | binder       |                                  |
fvp-morello-android | bionic       | GTEST_FILTER\* BIONIC_TEST_TYPE\*|
fvp-morello-android | boottest     |                                  |
fvp-morello-android | boringssl    | SYSTEM_URL                       |
fvp-morello-android | compartment  | USERDATA                         |
fvp-morello-android | device-tree  |                                  |
fvp-morello-android | dvfs         |                                  |
fvp-morello-android | libjpeg-turbo| LIBJPEG_TURBO_URL, SYSTEM_URL    |
fvp-morello-android | libpdfium    | PDFIUM_URL, SYSTEM_URL           |
fvp-morello-android | libpng       | PNG_URL, SYSTEM_URL              |
fvp-morello-android | lldb         | LLDB_URL, TC_URL                 |
fvp-morello-android | logd         | USERDATA                         |
fvp-morello-android | multicore    |                                  |
fvp-morello-android | zlib         | SYSTEM_URL                       |
fvp-morello-busybox | purecap      |                                  |
fvp-morello-oe      | fwts         |                                  |

!!! tip "Passing parameters"
    In order to pass parameters, use `tuxrun --parameters USERDATA=http://.../userdata.tar.xz`

!!! tip "Default parameters"
    **GTEST_FILTER** is optional and defaults to
    ```
    string_nofortify.*-string_nofortify.strlcat_overread:string_nofortify.bcopy:string_nofortify.memmove
    ```
    **BIONIC_TEST_TYPE** is optional and defaults to `static`. Valid values are `dynamic` and `static`.

## QEMU devices

The following tests are supported by the default root filesystem.

Device  | Tests               | Parameters           |
--------|---------------------|----------------------|
qemu-\* | command             |                      |
qemu-\* | kselftest-gpio      | CPUPOWER\* KSELFTEST |
qemu-\* | kselftest-ipc       | CPUPOWER\* KSELFTEST |
qemu-\* | kselftest-ir        | CPUPOWER\* KSELFTEST |
qemu-\* | kselftest-kcmp      | CPUPOWER\* KSELFTEST |
qemu-\* | kselftest-kexec     | CPUPOWER\* KSELFTEST |
qemu-\* | kselftest-rseq      | CPUPOWER\* KSELFTEST |
qemu-\* | kselftest-rtc       | CPUPOWER\* KSELFTEST |
qemu-\* | kunit\*             |                      |
qemu-\* | ltp-fcntl-locktests |                      |
qemu-\* | ltp-fs_bind         |                      |
qemu-\* | ltp-fs_perms_simple |                      |
qemu-\* | ltp-fsx             |                      |
qemu-\* | ltp-nptl            |                      |
qemu-\* | ltp-smoke           |                      |
qemu-\* | perf                |                      |

The following tests are not supported by the default root filesystem. You should
provide a custom root filesystem.

Device  | Tests               |
--------|---------------------|
qemu-\* | ltp-cap_bounds      |
qemu-\* | ltp-commands        |
qemu-\* | ltp-containers      |
qemu-\* | ltp-crypto          |
qemu-\* | ltp-cve             |
qemu-\* | ltp-filecaps        |
qemu-\* | ltp-fs              |
qemu-\* | ltp-hugetlb         |
qemu-\* | ltp-io              |
qemu-\* | ltp-ipc             |
qemu-\* | ltp-math            |
qemu-\* | ltp-mm              |
qemu-\* | ltp-pty             |
qemu-\* | ltp-sched           |
qemu-\* | ltp-securebits      |
qemu-\* | ltp-syscalls        |
qemu-\* | ltp-tracing         |

!!! tip "Passing parameters"
    In order to pass parameters, use `tuxrun --parameters KSELFTEST=http://.../kselftes.tar.xz`

!!! warning "CPUPOWER"
    Parameter CPUPOWER is only used by *qemu-i386* and *qemu-x86_64*.

!!! warning "KUnit config"
    In order to run KUnit tests, the kernel should be compiled with
    ```
    CONFIG_KUNIT=m
    CONFIG_KUNIT_ALL_TESTS=m
    ```
    The **modules.tar.xz** should be given with `--modules https://.../modules.tar.xz`.
