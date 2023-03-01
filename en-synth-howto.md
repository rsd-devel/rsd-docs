# Basic synthesis procedure

* This section describes how to synthesize a circuit from code that has been verified by logic simulation.

## Synthesis method for ZYNQ FPGA
There are two ways to synthesize RSD for Zynq FPGA:

1. Boot RSD via ARM Linux on Zynq
    * See [here](en-fpga-zynq-synth-for-linux)
    * Boot Linux on ARM on ZYNQ and launch RSD from a user program running on it.
    * *This method is basically recommended since it is easier.*
2. Directly boot RSD without ARM Linux
    * See [here](https://translate.google.com/translate?hl=en&sl=ja&tl=en&u=https://github.com/rsd-devel/rsd/wiki/jp-fpga-zynq-synth-for-baremetal)
    * Launch a bare-metal RSD boot program on ARM, and Launch RSD from it.
