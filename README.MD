# YakShop Backend (REST API)
<!-- ABOUT THE PROJECT -->
## About The Project
This project is a simple REST API for a yak shop where people can order milk and wool and also the shepard can keep an eye on the herd and the stock over time.
## Built with
The application was built with:
- Python
- Docker
- GitHub Actions
- Anaconda
- FastApi

<!-- Getting started -->
## Getting started
### Prequisites
For the prequisites you need python 3.8 (3.7 at least) installed on your machine. The development was done on Windows.

### Installation guide
#### Install in a conda env ( recommended )
Clone the repository.
~~~
git clone https://github.com/volkovwashere/yakshop.git
~~~
Export the python path (on Linux):
~~~
export PYTHONPATH=$PYTHONPATH:/home/<your_username>/yakshop/src
~~~
Step into the cloned repo.
~~~
cd yakshop
~~~
Install Anaconda3 or Miniconda3 on your machine.
Create an environment and set python to 3.8!
~~~
conda create -n your_env_name python=3.8
~~~
Activate your environment.
~~~
conda activate your_env_name
~~~
Install requirements
~~~
pip install -r requirements.txt
~~~
To run the script, run it from PyCharm or from the terminal. Set the default python path to the src folder or mark it as source from Pycharm and then run the script.
~~~
python uvicorn --host=0.0.0.0 --port=8000 src.yakshop.app:app
~~~ 

__OPTIONAL if you want to build a docker image locally__
~~~
docker build -t your_docker_image_name .
~~~
__Run the docker image__
~~~
docker run -p 8000:8000 your_docker_image_name
~~~
Go to localhost:8000/docs and check out the interactive API documentation.

# Some basic assumptions
The moment you open the YakShop online will be day 0, and all yaks will be eligible to be
shaved, as the two of you spent quite a lot of time setting up this shop and the shepherd
wasn’t able to attend much to his herd.
</br> Each morning the shepherd milks and shaves the eligible yaks. Yaks that aren’t eligible
for shaving on the exact day, cannot be shaved. For example, a yak who started out on
day 0 as 4 years, can be shaved again on day 13.
</br> Each day a LabYak produces 50-D*0.03 liters of milk (D = age in days)
</br> At most every 8+D*0.01 days you can again shave a LabYak (D = age in days)
</br> A yak’s first shave can occur at the age of 1 year.
</br> A LabYak dies the day he turns 10.