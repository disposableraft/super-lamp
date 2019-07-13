from pathlib import Path
from os import listdir
from shutil import move

def percent_of(value, percent):
  return round(value * (percent/100))

def create_directories():
  root = Path('./data')
  if not root.exists():
    root.mkdir()
  # data/train, data/valid, data/test
  for directory in ['train', 'valid', 'test']:
    if not (root/directory).exists():
      (root/directory).mkdir()

stanfordData = Path('./StanfordDogs')
data = Path('./data')
count = len([i for i in listdir(stanfordData)])

create_directories()

for directory in stanfordData.iterdir():
  if directory.name == '.DS_Store': continue

  print('Directory', directory)
  category = str(directory).split('-')[1].lower()
  for idx, image in enumerate(directory.iterdir()):
    if idx <= percent_of(count, 60):
      destination = data/'train'/category
      if not destination.exists(): destination.mkdir()
      move(str(image), destination)
    elif idx > percent_of(count, 60) and idx < percent_of(count, 80):
      destination = data/'valid'/category
      if not destination.exists(): destination.mkdir()
      move(str(image), destination)
    else:
      destination = data/'test'/category
      if not destination.exists(): destination.mkdir()
      move(str(image), destination)
