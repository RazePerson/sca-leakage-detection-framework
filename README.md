# SCA Leakage Detection Framework[¶](#SCA-Leakage-Detection-Framework)

This is a framework for TVLA. The goal of this framework is to make it easier for researchers, scientists, or anyone interested in using leakage detection techniques in SCA.

## Installation[¶](#Installation)

### Prerequisites

- python3 version 3.8.5+
    - to install python3 execute the following commands:
        ```shell
        $ sudo apt update -y
        $ sudo apt install python3 -y
        ```
- pip
    - to install pip execute the following commands:
        ```shell
        $ sudo apt update -y
        $ sudo apt install python3-pip -y
        ```

- Clone the repository:
    ```shell
    $ git clone https://github.com/RazePerson/sca-leakage-detection-framework.git
    ```


### Packages
Install following python packages
    
#### **Using Anaconda (Recommended)**:
    
- Follow the instructions for [installing Anaconda](https://docs.anaconda.com/anaconda/install/).


- Or follow this quick steps guide: 
    1. Prerequisites:
        ```shell
        $ sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
        ```
    2. Download Anaconda:
        ```shell
        $ wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
        # Optional verification of hash
        sha256sum Anaconda3-2021.05-Linux-x86_64.sh
        ```
    3. Install Anaconda:
        ```shell
        $ bash Anaconda3-2021.05-Linux-x86_64.sh
        ```
    4. Follow the installation prompt.
    5. [Verify installation](https://docs.anaconda.com/anaconda/install/verify-install/).
    
    **Note**: if the quick guide above doesn't work, please refer to the official installation guide.


- Create conda environment:
    ```shell
    $ conda create -n <environment_name> -y
    ```
- Activate conda environment:
    ```shell
    $ conda activate <environment_name>
    ```
- Install packages manually with these versions:
    ```shell
    $ conda install numpy=1.20.2 -y
    $ conda install pandas=1.2.4 -y
    $ conda install tqdm=4.59.0 -y
    $ conda install matplotlib=3.3.4 -y
    $ conda install seaborn=0.11.1 -y
    ```
- Or install packages using the *requirements.txt* file from the repo:
    ```shell
    $ conda install --file <path_to_repo>/requirements.txt -y
    ```

#### **Using Pip**:
- Install packages manually with these versions:
    ```shell
    $ pip install numpy==1.20.2
    $ pip install pandas==1.2.4
    $ pip install tqdm==4.59.0
    $ pip install matplotlib==3.3.4
    $ pip install seaborn==0.11.1
    ```

- Or install using the *requirements.txt* file from the repo:
    ```shell
    $ pip install -r <path_to_repo>/requirements.txt
    ```



## Framework Documentation Jupyter Notebook[¶](#Framework-Documentation-Jupyter-Notebook)

The full documentation of the framework can be found [here](https://github.com/RazePerson/sca-leakage-detection-framework/blob/master/sca-leakage-detection-framework/main-app.ipynb).