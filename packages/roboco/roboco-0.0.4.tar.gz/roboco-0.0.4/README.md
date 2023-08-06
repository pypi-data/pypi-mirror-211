
# Robot Containers
This repository contains Dockerfiles for building containers for [various robots](#available-containers).
It also includes a python script `run.py` that wraps the `docker` command to enable:

- building, starting and entering the container in one step
- graphical applications
- nvidia GPU passthrough
- realtime scheduling
- host networking
- full external device access (USB, cameras, etc.)

Finally, it includes `roboco`, a script for generating a new project from the included Dockerfiles.

[![CI - Test](https://github.com/monashrobotics/robot_containers/actions/workflows/ci.yml/badge.svg)](https://github.com/monashrobotics/robot_containers/actions/workflows/ci.yml)
[![CI - Docker Images](https://github.com/monashrobotics/robot_containers/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/monashrobotics/robot_containers/actions/workflows/docker-publish.yml)
[![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff) 
[![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 
[![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/)
[![image](https://img.shields.io/pypi/v/roboco.svg)](https://pypi.python.org/pypi/roboco)
[![image](https://img.shields.io/pypi/pyversions/roboco.svg)](https://pypi.python.org/pypi/roboco)

## Table of Contents

  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Adding a container to your project](#adding-a-container-to-your-project)
    * [Running the container](#running-the-container)
    * [Customising the container](#customising-the-container)
* [Available Dockerfile Templates](#available-dockerfile-templates)
  * [Hardware Drivers](#hardware-drivers)
  * [Software Snippets](#software-snippets)
* [Contributing](#contributing)
* [Troubleshooting](#troubleshooting)

## Requirements

### Docker
- Tested with Docker 20.10.23. 

- Install on Ubuntu using `sudo apt install docker.io` (other installation methods may not play well with the nvidia-docker2 runtime.)

- Follow "Manage Docker as a non-root user" at https://docs.docker.com/engine/install/linux-postinstall/

### nvidia-docker2 (for GPU support, optional)
- Install nvidia-docker2 by following https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#setting-up-nvidia-container-toolkit

### VSCode - Dev Containers Extension (Optional)
- Tested with v0.292.0 of Dev Containers extension https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

## Installation

### Using pip
```
pip install roboco
```

### Using git
```
git clone https://github.com/monashrobotics/robot_containers.git
cd robot_containers
pip install .
```

## Usage
### Adding a container to your project
```
roboco init
```

Follow the prompts to select the robot type and additional features.

Once completed, there will be two new files in your current directory: `Dockerfile` and `run.py`.

### Running the container

Build the image and run the container using:
```
./run.py
```

### Customising the container

The `Dockerfile` can be edited to add additional dependencies or change the base image.

When you make changes to the `Dockerfile`, you will need to rebuild the image using:
```
./run.py build
```
Then remove the old container and start a new one:
```
./run.py rm
./run.py
```

## Available Dockerfile Templates

Dockerfile templates are available for the following robot / ROS / Ubuntu combinations.

| Robot / ROS Distro (Ubuntu OS) | ROS 1 Noetic (20.04) | ROS 2 Foxy (20.04) | ROS 2 Humble (22.04)
| --- | :---: | :---: | :---: |
| ABB YuMi | WIP | ❌ | ❌ |
| Baxter | WIP | ❌ | ❌ |
| Fetch | WIP | ❌ | ❌ |
| Jackal | WIP | WIP | WIP |
| Panda | WIP | ❌ | ❌ |
| Ridgeback | WIP | ❌ | ❌ |
| UR5 | ✅ | ❌ | WIP |

Generic ROS 1 and ROS 2 Dockerfile templates for the following distributions are also available:

- ROS 1 Kinetic (16.04)
- ROS 1 Melodic (18.04)
- ROS 1 Noetic (20.04)

- ROS 2 Foxy (20.04)
- ROS 2 Galactic (20.04)
- ROS 2 Humble (22.04)

### Hardware Drivers

Snippets are available for these hardware drivers and ROS distro combinations:

| Driver / ROS Distro (Ubuntu OS) | ROS 1 Noetic (20.04) | ROS 2 Foxy (20.04) | ROS 2 Humble (22.04)
| --- | :---: | :---: | :---: |
| RealSense Camera | WIP | WIP | WIP |
| Velodyne LiDAR | WIP | WIP | WIP |
| Robotiq 2F-85 Gripper | WIP | ❌ | ❌ |
| Robotiq FT-300 Force-Torque Sensor | WIP | ❌ | ❌ |

### Software Snippets

Snippets are available for the following software packages:

| Software | ROS 1 Noetic (20.04) | ROS 2 Foxy (20.04) | ROS 2 Humble (22.04)
| --- | :---: | :---: | :---: |
| pytorch | WIP | WIP | WIP |

## Contributing
If there's a robot, or hardware driver that you'd like to see supported, please open an issue or pull request.
See [CONTRIBUTING.md](CONTRIBUTING.md)

## Troubleshooting
See [docs/troubleshooting.md](docs/troubleshooting.md)