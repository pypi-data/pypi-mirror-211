# Contributing

## Project Structure
```
robot_containers
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # MIT License
├── README.md                       # General information about the project
├── docs                            # Documentation
│   └── troubleshooting.md          # Troubleshooting guide
├── pyproject.toml                  # Python package configuration
├── run.py                          # Script to build and run the container
├── src                             # Python package
│   └── roboco
│       ├── __init__.py             # Package entrypoint
│       ├── __main__.py             # Templating script entrypoint
│       ├── configurations.py       # Configuration options for each robot
│       └── template.py             # Templating script
└── templates                       # Dockerfile templates
    ├── jackal
    │   ├── Dockerfile.foxy
    │   ├── Dockerfile.humble
    │   └── Dockerfile.noetic
    ├── panda
    │   └── Dockerfile.noetic
    ├── ros
    │   ├── Dockerfile.foxy
    │   ├── Dockerfile.galactic
    │   ├── Dockerfile.humble
    │   ├── Dockerfile.kinetic
    │   ├── Dockerfile.melodic
    │   └── Dockerfile.noetic
    ├── ur5
    │   └── ...
    └── ...
```

## Adding a new robot

To add a new robot, create a new directory in `templates` and add a `Dockerfile` for each ROS distribution you want to support. The `Dockerfile` should be named `Dockerfile.<rosdistro>` where `<rosdistro>` is the name of the ROS distribution (e.g. `noetic`).

Where possible, include only the latest ROS distributions supported by the robot, for each of ROS 1 and ROS 2. For example, the UR5 supports ROS 1 Kinetic, Melodic and Noetic, and ROS 2 Foxy and Humble. We provide templates for only ROS 1 Noetic and ROS 2 Humble. This will reduce maintenance overhead, encourage users to use the latest ROS distributions, and allow us to focus on adding support for more robots. The plain ROS templates can be used to support older ROS distributions.