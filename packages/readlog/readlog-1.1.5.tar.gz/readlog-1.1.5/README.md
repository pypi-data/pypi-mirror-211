## ReadLog

- A python code to read thermo info from lammps log file 

### Installation 

```bash
git clone https://github.com/eastsheng/ReadLog.git
cd ReadLog
python setup.py sdist
pip install .
```

### Requirements

- numpy
- pandas
- matplotlib

### Usage 

- run `plot_themo.py` in `demo` folder:

  ```bash
  python plot_thermo.py
  ```

- out:
- ![](README/_img/PotEng.png)



### Fixed

- Can adapt to incomplete thermo information

