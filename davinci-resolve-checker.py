#!/usr/bin/env python3

import argparse
import distro
import subprocess
import local_strings
from pylspci.parsers import VerboseParser
import pickle
import json

parser = argparse.ArgumentParser(description="Davinci Resolve checker")
parser.add_argument(
    "-l", "--locale",
    help="Locale for messages print by the checker, e.g. 'en_US'",
    dest='locale'
)
args = parser.parse_args()

local_str = local_strings.LocalStrings(preferred_locale=args.locale)

print(local_str["locale"], local_str.locale)

print(local_str["project name"], "2.6.2")  # When bumping, do not forget to also bump it in readme.

if distro.id() not in {"arch", "manjaro", "endeavouros", "garuda"}:
    print(local_str["you are running"], distro.name(), "(", distro.id(), ")", local_str["script not tested on distro"])
    exit(1)

dependencies_check = subprocess.run("pacman -Q expac mesa-demos python-distro python-pylspci", shell=True, capture_output=True, text=True)
if dependencies_check.returncode != 0:
    print(dependencies_check.stderr.strip())
    exit(1)

installed_dr_package = subprocess.run("expac -Qs '%n %v' davinci-resolve", shell=True, capture_output=True, text=True).stdout.rstrip('\n')
print(local_str["which DR package"], installed_dr_package)

installed_opencl_drivers = subprocess.run("expac -Qs '%n' opencl-driver", shell=True, capture_output=True, text=True).stdout.splitlines()
installed_opencl_nvidia_package = subprocess.run("expac -Qs '%n' opencl-nvidia", shell=True, capture_output=True, text=True).stdout.rstrip('\n')

debugging_with_pickled_lspci = False  # turn to true if want to debug somebody's lspci dump.
if not debugging_with_pickled_lspci:
    lspci_devices = VerboseParser().run()
else:
    # Use some dump file. To generate dumps, use dump_lspci_list.py.
    with open("lspci_dumps/optimus_laptop_no_any_driver_for_nvidia.bin", "rb") as fp:   # Unpickling.
        lspci_devices = pickle.load(fp)

print(local_str["openCL drivers"], " ".join([str(x) for x in installed_opencl_drivers]))

# Now we are going to check which GPUs are presented in system.
# According to this link: https://pci-ids.ucw.cz/read/PD/03
# There are four subclasses in PCI 03xx class
# I have seen all of them in machines that I could test, except 0301 - XGA controller
# lspci -d ::0300 - intel gpu or amd primary gpu
# lspci -d ::0302 - nvidia 3d controller on an optimus laptop
# lspci -d ::0380 - amd secondary gpu on an i+a laptop

print(local_str["presented gpus"])
print("\t" + "\n\t".join([x.device.name + " (" + local_str["kernel driver"] + " " + str(x.driver or '-') + ")" for x in lspci_devices if x.cls.id in (0x0300, 0x0301, 0x0302, 0x0380)]))

GL_VENDOR = subprocess.run('glxinfo | grep "OpenGL vendor string" | cut -f2 -d":"', shell=True, capture_output=True, text=True).stdout.strip()
print(local_str["opengl vendor"], GL_VENDOR)
# By GL_VENDOR we can distinguish not only OpenGL Open/Pro implementations, but also a primary GPU in use (kinda).
# See https://stackoverflow.com/questions/19985131/how-identify-the-primary-video-card-on-linux-programmatically for more information.

print("clinfo detected platforms and devices:")
clinfo_data = json.loads(subprocess.run('clinfo --json', shell=True, capture_output=True, text=True).stdout.strip())
found_ready_cl_gpu = False
cl_platform_index = len(clinfo_data["platforms"]) - 1
while cl_platform_index >= 0:
    number_of_devices = len(clinfo_data["devices"][cl_platform_index]['online'])
    platform_name = clinfo_data["platforms"][cl_platform_index]['CL_PLATFORM_NAME']
    print("\t" + platform_name + " (number of devices: " + str(number_of_devices) + ")")
    if platform_name != "Clover" and number_of_devices > 0:
        found_ready_cl_gpu = True
    cl_platform_index -= 1

if not found_ready_cl_gpu:
    print("Not found opencl platforms with appropriate GPUs. Check that you have installed corresponding driver. Otherwise you cannot run DR.")
    exit(1)

print("")  # Empty line, to separate verdict from configuration info.

if GL_VENDOR == "":
    print(local_str["missing opengl vendor"])
    exit(1)

if "opencl-mesa" in installed_opencl_drivers:
    print(local_str["should uninstall opencl-mesa"])
    exit(1)

found_AMD_GPU = None
found_INTEL_GPU = None
found_NVIDIA_GPU = None

for device in lspci_devices:
    if device.cls.id in (0x0300, 0x0301, 0x0302, 0x0380):
        if device.vendor.name == 'Intel Corporation':
            if found_INTEL_GPU == None:
                found_INTEL_GPU = device
            else:
                print(local_str["several intel gpus"])
                exit(1)
        if device.vendor.name == 'Advanced Micro Devices, Inc. [AMD/ATI]':
            if found_AMD_GPU == None:
                found_AMD_GPU = device
            else:
                print(local_str["several amd gpus"])
                exit(1)
        if device.vendor.name == 'NVIDIA Corporation':
            if found_NVIDIA_GPU == None:
                found_NVIDIA_GPU = device
            else:
                print(local_str["several nvidia gpus"])
                exit(1)

if found_AMD_GPU and found_NVIDIA_GPU:
    if found_AMD_GPU.driver != "vfio-pci" and found_NVIDIA_GPU.driver != "vfio-pci":
        print(local_str["confused by nvidia and amd gpus"])
        exit(1)
    else:
        if found_AMD_GPU.driver == "vfio-pci":
            print(local_str["amd gpu binded to vfio-pci"])
            found_AMD_GPU = None
        if found_NVIDIA_GPU.driver == "vfio-pci":
            print(local_str["nvidia gpu binded to vfio-pci"])
            found_NVIDIA_GPU = None

if not found_AMD_GPU and not found_NVIDIA_GPU and found_INTEL_GPU:
    print(local_str["only intel gpu, cannot run DR"])
    exit(1)

if found_AMD_GPU:
    if found_AMD_GPU.driver != 'amdgpu':
        if found_AMD_GPU.driver == 'radeon':
            if 'amdgpu' in found_AMD_GPU.kernel_modules and 'radeon' in found_AMD_GPU.kernel_modules:
                print(local_str["switch from radeon driver to amdgpu"])
                exit(1)
            else:
                print(local_str["no support for amd driver, cannot run DR"])
        print(local_str["not running amdgpu driver, cannot run DR"])
        exit(1)

    if 'opencl-amd' not in installed_opencl_drivers and 'rocm-opencl-runtime' not in installed_opencl_drivers:
        print(local_str["missing opencl driver"])
        exit(1)

    print(local_str["good to run DR"])

if found_NVIDIA_GPU:
    # I have tested it with DR 16.2.3 and found out that BMD have fixed that issue. See https://www.youtube.com/watch?v=NdOGFBHEnkU
    # So I will keep this comment for a while, then will remove it.
    # if 'opencl-amdgpu-pro-orca' in installed_opencl_drivers or 'opencl-amdgpu-pro-pal' in installed_opencl_drivers or 'opencl-amd' in installed_opencl_drivers:
    #     print("You have installed opencl for amd, but DaVinci Resolve stupidly crashes if it is presented with nvidia gpu. Remove it, otherwise you could not use DaVinci Resolve.")
    if not installed_opencl_nvidia_package:
        print(local_str["missing opencl-nvidia package"])
        exit(1)
    if found_NVIDIA_GPU.driver != 'nvidia':
        print(local_str["missing nvidia as kernel driver"])
        exit(1)
    if GL_VENDOR != "NVIDIA Corporation":
        print(local_str["not running nvidia rendered"])
        exit(1)
    print(local_str["good to run DR"])
