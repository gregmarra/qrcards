import os
import PIL
from PIL import Image
import qrcode

from optparse import OptionParser

CARD_WIDTH_PX = 822
CARD_HEIGHT_PX = 1122

# 36px cut zone, 36px safe zone
CORNER_OFFSET = 96

SUITES = [
  "clubs",
  "diamonds",
  "hearts",
  "spades",
]

NUMBERS = [
  "two",
  "three",
  "four",
  "five",
  "six",
  "seven",
  "eight",
  "nine",
  "ten",
  "jack",
  "queen",
  "king",
  "ace",
]

class CardGenerator(object):
  def __init__(self, save_folder):
    self.save_folder = save_folder
    super(CardGenerator, self).__init__()

  def makeCard(self, number, suite):
    card = Image.new("RGBA", (CARD_WIDTH_PX, CARD_HEIGHT_PX), (255,255,255,255))
    big_qr_code = self.makeQRCode(number, suite, 16)
    small_qr_code = self.makeQRCode(number, suite, 3)
    
    center_offset = (
      card.size[0] / 2 - big_qr_code.size[0] / 2,
      card.size[1] / 2 - big_qr_code.size[1] / 2
    )
    top_left_offset = (
      CORNER_OFFSET,
      CORNER_OFFSET
    )
    bottom_right_offset = (
      card.size[0] - small_qr_code.size[0] - CORNER_OFFSET,
      card.size[1] - small_qr_code.size[1] - CORNER_OFFSET
    )
    card.paste(big_qr_code, center_offset)
    #card.paste(small_qr_code, top_left_offset)
    #card.paste(small_qr_code, bottom_right_offset)

    return card

  def makeQRCode(self, number, suite, box_size):
    qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_L,
      box_size=box_size,
      border=4,
    )
    qr.add_data("{}.of.{}".format(number, suite))
    qr.make(fit=True)
    return qr.make_image()

  def writeCard(self, number, suite):
    filename = "{}.of.{}.png".format(number, suite)
    card = self.makeCard(number, suite)
    card.save(os.path.join(self.save_folder, filename))

  def writeBlank(self):
    card = Image.new("RGBA", (CARD_WIDTH_PX, CARD_HEIGHT_PX), (255,255,255,255))
    card.save(os.path.join(self.save_folder, "blank.card.png"))


def main():
  parser = OptionParser()
  parser.add_option("-s", "--save_folder", type="string", default="cards",
                    help="folder to save output to")
  options, args = parser.parse_args()

  cg = CardGenerator(options.save_folder)
  for suite in SUITES:
    for number in NUMBERS:
      cg.writeCard(number, suite)
  cg.writeBlank()
  print("done.")

if __name__ == '__main__':
    main()
