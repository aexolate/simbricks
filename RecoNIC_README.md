# Running RecoNIC Experiments
This documentation provides the preliminary installations required and steps to run the the RecoNIC example discussed in the dissertation.

## Preliminary Installations

The Vivado software and its required Intellectual Property (IP) licenses must first be acquired before running the experiments. These software and licenses are not included as part of the repository. Please refer to AMD's website for the installations and acquisition of licenses. The software/IP licenses can be purchased or applied through AMD University Program. Alternatively, the evaluation license can be used to temporarily evaluate this project.

**RecoNIC/xsim Requirements**
- Vivado 2021.2 (Enterprise Version) w/ vitis_net_p4 installed
    ```
    How to enable vitis_net_p4: (1) before Vivado installation, we need to '$ export VitisNetP4_Option_VISIBLE=true'; (2) When running Vivado installer, you should be able to see the option for Vitis Networking P4. Make sure you select the vitis_net_p4 option.
    ```

- IP License: ERNIC, Vitis Networking P4
- python >= 3.8

**SimBricks Requirements**
- docker


## Pre-Experiment Setup
```
# It is recommended to use VScode Dev Container to run the commands. 
# Press Ctrl+Shift+P and execute the Dev Containers: Reopen in Container 
# command to open the repository inside the container.

# >> SimBricks Setup
make
git submodule update --init

# Replace N with number of cores in the -jN parameter
make -jN sims/external/qemu/ready 
make -jN build-images-min
make convert-images-raw

# >> Vivado Setup
git clone https://github.com/Xilinx/XilinxBoardStore
export BOARD_REPO=$(pwd)/XilinxBoardStore

# Change the path to your Vivado/Vitis installation directory if it's not in /tools/Xilinx
# Make sure to change the Xilinx mount in `.devcontainer.json` as well if it is not /tools/Xilinx
export VIVADO_DIR=/tools/Xilinx/Vivado/2021.2
export PATH=$PATH:/tools/Xilinx/Vivado/2021.2/bin
export PATH=$PATH:/tools/Xilinx/Vitis_HLS/2021.2/bin

pip install numpy
pip install scapy

sudo apt update
sudo apt install libtinfo5
```


# RecoNIC Experiment

- The elboration/simulation of RecoNIC using Vivado requires sufficient system memory. Insufficient memory may lead to degraded performance due to swap files, or fatal errors. *Each* xsim simulation may peak to ~10GB of memory usage.
- If `TimeoutError` occurs, try increasing the timeout duration in `simbricks/orchestration/exectools.py` as the elaboration process may take awhile depending on CPU and Memory availalbe.

In the `experiments` directory, execute `python3 run.py --verbose --force pyexps/reconic.py` to run the RecoNIC experiment. The results can be found in the `/out` folder. Change the `testcase` variable in the python script to run the RDMA WRITE or RDMA READ experiment. 

For further configuration of the RDMA subsystem or payload, the configuration JSON file can be in `/workspaces/simbricks/sims/external/reconic/sim/testcases/write_2rdma/write_2rdma.json` for the WRITE testcase, and similarly for the READ testcase.