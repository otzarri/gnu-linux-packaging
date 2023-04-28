# 🧭 Build a minimal RPM package

This lab teaches how to build minimal RPM packages for [RPM-based Linux distributions](https://en.wikipedia.org/wiki/Category:RPM-based_Linux_distributions). During it you will create an example package called `hello-world`.

The goal is to easily understand the very basics of building RPM packages. Section [Links of interest](#links-of-interest) includes references to additional and more detailed information to extend you knowledge.

[RPM packaging system](https://rpm.org/) is implemented across various families of GNU/Linux distros using the same tools. For instance, [Fedora](https://www.fedoraproject.org/) and [OpenSuse](https://www.opensuse.org/) are two major distros that use the RPM to manage system packages. That's why the instructions in this lab are compatible with all the RPM-based distros.

The file that I've chosen to package is a Bash script because it provides a cross-arch and cross-distro application that does not need to be compiled. Bash is included in the vast majority of GNU/Linux distros.

## 🧪 Prepare the lab environment

Installing a virtual machine to build packages can be a tedious task. It's much easier to use OCI containers instead. You can create your container from any image of a RPM-based distro like [Almalinux](https://hub.docker.com/_/almalinux), [Fedora](https://registry.fedoraproject.org/repo/fedora/tags/), or [OpenSuse](https://registry.opensuse.org/cgi-bin/cooverview?srch_term=project%3D%5EopenSUSE%3AContainers%3A+container%3D%5Eopensuse%2Fleap%24).

> 💡 I use [Podman](https://podman.io/) but you can use [Docker](https://www.docker.com/) if you prefer, the usage is the same.

Run the command below to create a container based on the `almalinux` image. It also will mount the [assets](assets) directory to the path `/assets` inside the container.

```
$ podman run \
    --rm -ti \
    -v ./assets:/assets \
    docker.io/library/almalinux \
    /bin/bash
```

This will start a new ephemeral container and give you a shell session.

Now install the dependencies required by this lab:

```
# dnf install -y rpmdevtools rpmlint sudo tree
```

Add the user `tux` to build the packages as a regular user:

```
# useradd -rm -s /bin/bash -G wheel -u 1000 tux
```

Set the string `P4ssW0rd..` as password for user `tux`.

```
# echo "tux:P4ssW0rd.." | chpasswd
```

Now switch to user `tux`:

```
# su - tux
```

Great! You're now ready to complete the entire lab as a regular user (and also as root, when needed, with `sudo`) using this container.

## 🛂 Minimum requirements to build a RPM package

RPM packages are built using several small programs that perform specific tasks following [the UNIX philosophy](https://en.wikipedia.org/wiki/Unix_philosophy). For this lab, you'll be using [rpmdevtools](https://fedoraproject.org/wiki/Rpmdevtools), which was released by [Red Hat](https://www.redhat.com/) in 2006 to simplify the process of building RPM packages and is now widely adopted across RPM-based Linux distros.

It's mandatory to have the following assets in order to use `rpmdevtools`:

1. **Compressed file with the sources**: A compressed file that contains a root directory storing the entire program. It may contain executable files, source code, documentation, configuration files, etc. During this lab, you will create the source file that will contain the script [assets/hello-world.sh](assets/hello-world.sh).
2. **Spec file**: A text file with information about the software, such as the name, version, license, and changelog. It also includes instructions for compiling the software and required dependencies, among others. There is a finished spec file at [assets/hello-world.spec](assets/hello-world.spec) that you will use to create the example package.

All mentioned assets are available in the [assets](assets) directory and ready to be used during this lab.

## 🏗️ Prepare the RPM package workspace

The first task when developing a new RPM package with `rpmdevtools` is to create the workspace. The workspace is the directory where the package is built, consisting of a root directory and five subdirectories. Their names and functions are detailed in the table below.

| Subdirectory | Description                                           |
| ------------ | ----------------------------------------------------- |
| BUILD        | Stores temporary files during the build process.      |
| RPMS         | Stores RPM packages for different architectures.      |
| SOURCES      | Stores tar/gzip files containing the program sources. |
| SPEC         | Stores spec files.                                    |
| SRPMS        | Stores .src.rpm packages (source RPMs).               |

Fortunately, you don't have to remember all of this every time you build a new package. Simply use this command:

```
$ rpmdev-setuptree
```

The command above just created the workspace at `~/rpmbuild`, which is the default location used by `rpmdevtools`.

Verify that the workspace structure is correct:

```
tree ~/rpmbuild
/home/tux/rpmbuild
├── BUILD
├── RPMS
├── SOURCES
├── SPECS
└── SRPMS
```

## 🗜️ Create the compressed source file

The `rpmdevtools`, to build packages, require at least one compressed file containing the program sources located in the `SOURCES` directory of the workspace. During this section, you'll create this file and place it in its proper location.

Now you are going to create the compressed source file, for which you first need to prepare a directory with all the content. Create a new directory for the sources:

```
$ mkdir hello-world-0.0.1
```

Copy the program sources into this new directory. In this case, you only need to copy the [assets/hello-world.sh](assets/hello-world.sh) script.

```
$ cp /assets/hello-world.sh hello-world-0.0.1/
```

Since Bash scripts are interpreted and work by default on almost all GNU/Linux distros, you don't need to include anything else in the source file. Run the command below to create the compressed file and place it in the correct location within the RPM packaging workspace:

```
$ tar zcf ~/rpmbuild/SOURCES/hello-world-0.0.1.tar.gz hello-world-0.0.1
```

## 📝 Create the spec file

It's very important to create a correct spec file and place it in the `SPECS` subdirectory of the workspace. The `rpmdevtools` will read this file to obtain the metadata and build instructions for the package. This lab already includes a properly configured spec file to build the example package.

Copy the spec file to the `SPECS` subdirectory of the workspace:

```
$ cp /assets/hello-world.spec ~/rpmbuild/SPECS/
```

You can use the `rpmlint` command to analyze the spec file for errors and verify that it is correct:

```shell
$ rpmlint ~/rpmbuild/SPECS/hello-world.spec
```

## 📦 Build the RPM package

Everything needed for building the package is ready. Proceed to build it by executing the following command:

```
$ rpmbuild -ba ~/rpmbuild/SPECS/hello-world.spec
```

The package should have already been created at `~/rpmbuild/RPMS/noarch/hello-world-0.0.1-1.el8.noarch.rpm`. You can check it with the following command:

```
$ file ~/rpmbuild/RPMS/noarch/hello-world-0.0.1-1.el8.noarch.rpm
/home/tux/rpmbuild/RPMS/noarch/hello-world-0.0.1-1.el8.noarch.rpm: RPM v3.0 bin i386/x86_64 hello-world-0.0.1-1.el8## Install the RPM package
```

## 🚀 Install the RPM package and run the program

The package we have created is a normal RPM package like any other, which means that you can manage it using the `rpm` tool.

Use the command below to install the package:

```
$ sudo rpm -ivh ~/rpmbuild/RPMS/noarch/hello-world-0.0.1-1.el8.noarch.rpm
```

If you pay attention to the [spec file](assets/hello-world.spec), you will see that the asset [assets/hello-world.sh](assets/hello-world.sh) is installed in `/usr/bin/hello-world`, without the `.sh` extension. Use the following command to execute this script that we just installed using the RPM package:

```
$ hello-world
Hello world
```

If the above command returned the same output, congratulations! You have successfully packaged, installed, and executed a program through the RPM packaging system.

Use the `exit` command twice consecutively if you want to exit the container. This action will delete the container, and all its content will be lost except for the `/assets` directory. If you want the RPM package to persist, you can copy `hello-world-0.0.1-1.el8.noarch.rpm` to the `/assets` directory before exiting the container.

## 🔗 Links of interest

* [[RPM doc] RPM spec file reference documentation](https://rpm-software-management.github.io/rpm/manual/spec.html)
* [[Fedora doc] RPM Macros](https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/)
* [[Red Hat Enable Sysadmin] How to create a Linux RPM package](https://www.redhat.com/sysadmin/create-rpm-package)
* [[RHEL doc] Packaging software](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html-single/packaging_and_distributing_software/index#packaging-software_packaging-and-distributing-software)
