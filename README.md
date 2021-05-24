### How to benchmark

* Run `command.sh`
* Download __Widerface valuation set, Widerface annotation__, place at root of this repo
* Delete all in __groundtruth/__ and __detections/__
* Run `generate.py`
* Replace class `B` in `benchmark.ipynb` with class to be evaluated
* Run `benchmark.ipynb`
* Run `python pascalvoc.py`, type Y, result will show in __results/__