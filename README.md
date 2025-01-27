# Classification of molecules using FSM

This repository is proof of concept of employing a frequent subgraph mining technique to perform molecule classification.
The approach made use of [MoSS](https://borgelt.net/moss.html) program to perform FSM itself, and then wraps the results in a Python API for easier integration with various ML tools and libraries.

The experiment results can be found in this [report](./report/report.md).


## Building a native moss executable
It would be way more convenient to incorporate a native executable of the moss library into the project,
compared to using a user-dependant JRE.

For x86 64-bit systems, the process of building a native executable can be simplified by using a Docker environment.
To execute the build process locally, execute the following:
```bash
docker build --output=. .
```

Unfortunately, as mentioned [here](https://www.graalvm.org/22.1/docs/getting-started/container-images/),
the GraalVm docker images work only on "Linux, macOS, and Windows platforms on x86 64-bit systems, and for Linux on ARM 64-bit systems" - not on ARM-based Apple computers.
Therefore to build a native executable on an Apple M-series based system, it's necessary to do the following:

- Install GraalVM on the host system
- Execute the following code:
```bash
gu install native-image
javac moss/*.java
echo "Main-Class: moss.Miner" > manifest
jar cfm miner.jar manifest moss/*.class
native-image -jar miner.jar miner
```
