# Dog Trainer
## Classify Dog Breeds with FastAI, Starlette and ReactJS

This repo contains my work on the first lesson from [FastAI](https://www.fast.ai/).

The model ([DogClassifier.ipynb](./DogClassifier.ipynb)) was trained with about 87% accuracy in predicting a dog's breed from a set of 120 possible classes. 

![](./images/dog-classifier.gif)  

The accompanying web app was cobbled together with [Starlette.py](https://www.starlette.io/) (thanks to [this example](https://github.com/simonw/cougar-or-not), which I poached heavily from) and [Create React App](https://github.com/facebook/create-react-app) for a default frontend.

## Installation

The fastest way to start classifying dogs is to do a "production" build.

**Client Files**

`cd app/client`

`npm install`

`npm run-script build`

These commands should install the JS dependencies and run a build. Then, head over to the server and install the Python dependencies.

**Server Files**

`cd ../server && python scripts/install`

Start the app:

`python app.py`

And if all went well, a server will be running at http://127.0.0.1:8000.

## Development

For frontend development, hot reloading works.

First make sure the Python server is running.

`python app.py`

Then start the Node server for editing.

`npm start`

Done. Change code, watch reload. Fun stuff.
