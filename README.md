# Gamza's malware sandbox
This is a sandbox analysis tools for suspicious executable file. This program can make you to execute the file with isolated environment and check the file is malicious. This can help you determine what actions the file does during execution and diagnose malicious files.

This tool supports analysis of one virtual environment at a time. You can run any executable file you want within a separate virtual environment, and check all event logs that occurred while the file was running in the form of a web dashboard. Basically, supported virtual environment operating systems are as follows.
- Windows 10
- Windows 7

## Installation
1. Download `VirtualBox`.
2. Clone this project
    ```bash
    $ git clone https://github.com/no-1-of-gamza/Gamza_VM_Sysmon.git
    ```
3. Download guest VM files from the links below.
    - Windows 10: []()
    - Windows 7: []()
4. Unzip that zip files and move both folders to the path below.
    - `C:\Program Files\Oracle\VirtualBox\`
5. Download the zip files of Elasticsearch and Kibana from the links below.
    - Elasticsearch: []()
    - Kibana: []()
6. Unzip that zip files and move both folders to C drive. Each folder's path should be as follows.
    - Elasticsearch: C:\\elasticsearch\\
    - Kibana: C:\\kibana\\

### Notice
The Virtual Machine runs on its own within the program when the analysis starts and automatically terminates when the analysis ends, so do not run it yourself.