# pyMAP
Python library for processing raw IMAP-lo data calibration data, accessing and working the IMAPlo sql database, and executing basic analysis routines. 

## Getting started
1. Install Anaconda
    - how to install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)
2. Install Git
    - how to install [Git](https://github.com/git-guides/install-git)
3. Clone pyMAP onto the users local environment
    - see <> Code/Clone above
4. Add repository to path
    - insert steps here
    - or use sys.path.append(r’<where pyMAP package is cloned>’)
5. load pyMAP anaconda environment .yaml
    - insert steps here
6. Install [UNH pulse secure](https://networking.unh.edu/vpn/)

### Prerequisites
- up to date anaconda, load .yaml file to make this process easies
- add packages

## Package contents

### ```pyMAP.tof```
Set of tools for cleaning and analizing direct event data TOF data, and compare results to simplified models. Uses IMAP/IBEX-lo tof dimensions and user provided times of flight to calculate ideal times of flight, ion speeds, foil energy loss. 

### ```pyMAP.plt```
set of plotting tools tailored to visualizing IMAPlo calibration data. Currently only have standardized plotting for direct event data. 
- see examples/tof_plotting_demo.ipynb

### ```pyMAP.tools```

### ```pyMAP.data```
library of load functions to take raw calibration data and import to pandas dataframe. Specifically see pyMAP.data.load. 

## Jill: IMAPlo SQL Calibration Database
Jill is a server housed in Morse Hall at UNH, containing the IMAPlo instrument calibration data. The server is 20TB of Raid 5 storage, with daily state backup. Raw data is ingested from the IMAPlo calibration sharepoint server science/testing/IMAPlo_Cal.

### DB access
- see examples/jill access example.ipynb

to access jill you need 
1. given access by one of the server admins
    - if you don't have access to jill contact jon: jonathan.bower@unh.edu
2. to be on the unh network (on campus or on vpn) 
3. initialize jill through ```pymap.jill()```
4. input jill login information (also your unh login information) when prompted

### ```pymap.jill``` 
- initializing jill issues an ssh connection with sql port forwarding then generates and connects the sqlalchemy engine
- querys to the sql database can be issued using sql syntax with the jill.query command
- quiery results are output to pandas dataframe 

##  Examples
Example Python notebooks showing the functionality can bee seen in ```pyMAP/examples```.

## Versioning 

## Authors
- Jonathan Bower, jonathan.bower@unh.edu
- Aly Aly
- Taeho Lim 

## License
This software has been developed for use analyzing IMAP-lo calibration, so Probably NASA Open Source Agreement (NOSA)? 

## Acknowledgements
