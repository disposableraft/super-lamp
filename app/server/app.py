import aiohttp
from fastai.vision import (
    open_image,
    load_learner
  )
from io import BytesIO
import json
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, JSONResponse
import uvicorn

app = Starlette(debug=True)

# LOL allow it all
app.add_middleware(CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
  )

app.mount('/static', StaticFiles(directory='../client/build/static'), name='static')

async def get_bytes(url):
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      return await response.read()

# The react default homepage
@app.route('/')
async def homepage(request):
    react = open('../client/build/index.html', 'r')
    return HTMLResponse(react.read())

@app.route("/url", methods=["GET"])
async def from_url(request):
  bytes = await get_bytes(request.query_params["url"])
  return predict_image_from_bytes(bytes)

@app.route("/upload", methods=["POST"])
async def upload(request):
  data = await request.form()
  bytes = await (data["file"].read())
  return predict_image_from_bytes(bytes)

def predict_image_from_bytes(bytes):
  img = open_image(BytesIO(bytes))
  learner = load_learner("./fastai")
  p_class, _, p_outputs = learner.predict(img)
  p_0, p_1, p_2 = top_three_predictions(p_outputs)
  return JSONResponse({
    "prediction": str(p_class),
    "topThree": {
      1: p_0,
      2: p_1,
      3: p_2
    }
  })

def class_names():
  return [ 'affenpinscher', 'afghan_hound', 'african_hunting_dog', 'airedale', 
    'american_staffordshire_terrier', 'appenzeller', 'australian_terrier', 'basenji', 
    'basset', 'beagle', 'bedlington_terrier', 'bernese_mountain_dog', 'black_and_white', 
    'blenheim_spaniel', 'bloodhound', 'bluetick', 'border_collie', 'border_terrier', 
    'borzoi', 'boston_bull', 'bouvier_des_flandres', 'boxer', 'brabancon_griffon', 
    'briard', 'brittany_spaniel', 'bull_mastiff', 'cairn', 'cardigan', 
    'chesapeake_bay_retriever', 'chihuahua', 'chow', 'clumber', 'cocker_spaniel', 
    'collie', 'curly', 'dandie_dinmont', 'dhole', 'dingo', 'doberman', 'english_foxhound', 
    'english_setter', 'english_springer', 'entlebucher', 'eskimo_dog', 'flat', 
    'french_bulldog', 'german_shepherd', 'german_short', 'giant_schnauzer', 
    'golden_retriever', 'gordon_setter', 'great_dane', 'great_pyrenees', 
    'greater_swiss_mountain_dog', 'groenendael', 'ibizan_hound', 'irish_setter', 
    'irish_terrier', 'irish_water_spaniel', 'irish_wolfhound', 'italian_greyhound', 
    'japanese_spaniel', 'keeshond', 'kelpie', 'kerry_blue_terrier', 'komondor', 'kuvasz', 
    'labrador_retriever', 'lakeland_terrier', 'leonberg', 'lhasa', 'malamute', 'malinois', 
    'maltese_dog', 'mexican_hairless', 'miniature_pinscher', 'miniature_poodle', 
    'miniature_schnauzer', 'newfoundland', 'norfolk_terrier', 'norwegian_elkhound', 
    'norwich_terrier', 'old_english_sheepdog', 'otterhound', 'papillon', 'pekinese', 
    'pembroke', 'pomeranian', 'pug', 'redbone', 'rhodesian_ridgeback', 'rottweiler', 
    'saint_bernard', 'saluki', 'samoyed', 'schipperke', 'scotch_terrier', 'scottish_deerhound', 
    'sealyham_terrier', 'shetland_sheepdog', 'shih', 'siberian_husky', 'silky_terrier', 'soft', 
    'staffordshire_bullterrier', 'standard_poodle', 'standard_schnauzer', 'sussex_spaniel', 
    'tibetan_mastiff', 'tibetan_terrier', 'toy_poodle', 'toy_terrier', 'vizsla', 'walker_hound', 
    'weimaraner', 'welsh_springer_spaniel', 'west_highland_white_terrier', 'whippet', 'wire', 
    'yorkshire_terrier' ]

def top_three_predictions(outputs):
  # Zip the classes and predictions together into a single array.
  # `item()` translates the Tensor object (0.009) into an integer.
  classes = [{"name": z[0], "prob": z[-1].item()} for z in zip(class_names(), outputs)]

  sorted_classes = sorted(classes, key=lambda k: k['prob'], reverse=True)
  return sorted_classes[0], sorted_classes[1], sorted_classes[2]

if __name__ == "__main__":
  uvicorn.run(app, host='0.0.0.0', port=5000)
