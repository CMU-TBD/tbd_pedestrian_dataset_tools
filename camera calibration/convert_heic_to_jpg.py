import os
from PIL import Image
import pyheif

SourceFolder="raw_imgs"
TargetFolder="tepper_imgs"

for file in os.listdir(SourceFolder):
  SourceFile=SourceFolder + "/" + file
  TargetFile=TargetFolder + "/" + file.replace(".HEIC",".JPG")

  heif_file = pyheif.read(SourceFile)
  image = Image.frombytes(
      heif_file.mode,
      heif_file.size,
      heif_file.data,
      "raw",
      heif_file.mode,
      heif_file.stride,
      )

  image.save(TargetFile, "JPEG")
