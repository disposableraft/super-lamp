from pathlib import Path
from os import listdir
from shutil import move

# Images in this dataset were organized into a basket of classes:
# ./source/n000123-scottish_Foobar
#
# This script reorganizes them into three folders:
# ./target/train/scottish_foobar
# ./target/valid/scottish_foobar
# ./target/test/scottish_foobar
#
# Usage:
#
# dogs = new Rekennel('./StanfordDogs', './data')
# dogs.move()
#
class Rekennel:
  def __init__(self, source, target):
    # eg, './StanfordDogs'
    self.source = Path(source)
    # eg, './data'
    self.target = Path(target)

  def percent_of(self, value, percent):
    return round(value * (percent/100))

  # Create directories: data/train, data/valid, data/test
  def create_directories(self):
    if not self.target.exists():
      self.target.mkdir()
    for directory in ['train', 'valid', 'test']:
      if not (self.target/directory).exists():
        (self.target/directory).mkdir()

  def move(self):
    count = len([i for i in listdir(self.source)])

    self.create_directories()

    for directory in self.source.iterdir():
      if directory.name == '.DS_Store': continue

      # Stanford dogs has directory names such as n000123-scottish_Foobar
      category = str(directory).split('-')[1].lower()

      # Split the files into directories for /train (60%), /valid (20%) and /test (20%)
      for idx, image in enumerate(directory.iterdir()):
        if idx <= self.percent_of(count, 60):
          destination = self.target/'train'/category
          if not destination.exists(): destination.mkdir()
          move(str(image), destination)
          if idx % 10: print(image, ' -> ', destination)

        elif idx > self.percent_of(count, 60) and idx < self.percent_of(count, 80):
          destination = self.target/'valid'/category
          if not destination.exists(): destination.mkdir()
          move(str(image), destination)
          if idx % 10: print(image, ' -> ', destination)

        else:
          destination = self.target/'test'/category
          if not destination.exists(): destination.mkdir()
          move(str(image), destination)
          if idx % 10: print(image, ' -> ', destination)
