from pathlib import Path
from shutil import copy

stanfordDogs = Path('./StandfordDogs/n02113799-standard_poodle')
data = Path('./data')

count = len([image for image in stanfordDogs.iterdir()])

for idx, old_dir in enumerate(stanfordDogs.iterdir()):
  _, _, name = old_dir.parts

  # training huskies
  if idx <= (count * 0.6):
    new_dir = data/'train/standard_poodle'
    if not new_dir.exists():
      new_dir.mkdir()
    
    copy(old_dir, new_dir/name)

  # valid huskies
  elif idx > (count * 0.6) and idx <= (count * 0.8):
    new_dir = data/'valid/standard_poodle'
    if not new_dir.exists():
      new_dir.mkdir()
    
    copy(old_dir, new_dir/name)

  # testing huskies
  else:
    new_dir = data/'test/standard_poodle'
    if not new_dir.exists():
      new_dir.mkdir()
    
    copy(old_dir, new_dir/name)
