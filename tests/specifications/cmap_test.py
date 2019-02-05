import pytest
from fontbakery.checkrunner import (
              DEBUG
            , INFO
            , WARN
            , ERROR
            , SKIP
            , PASS
            , FAIL
            )

from fontTools.ttLib import TTFont

check_statuses = (ERROR, FAIL, SKIP, PASS, WARN, INFO, DEBUG)

mada_fonts = [
  "data/test/mada/Mada-Black.ttf",
  "data/test/mada/Mada-ExtraLight.ttf",
  "data/test/mada/Mada-Medium.ttf",
  "data/test/mada/Mada-SemiBold.ttf",
  "data/test/mada/Mada-Bold.ttf",
  "data/test/mada/Mada-Light.ttf",
  "data/test/mada/Mada-Regular.ttf",
]

@pytest.fixture
def mada_ttFonts():
  return [TTFont(path) for path in mada_fonts]


def test_check_013(mada_ttFonts):
  """ Fonts have equal unicode encodings ? """
  from fontbakery.specifications.cmap import com_google_fonts_check_013 as check
  from fontbakery.constants import WindowsEncodingID

  print('Test PASS with good family.')
  # our reference Mada family is know to be good here.
  status, message = list(check(mada_ttFonts))[-1]
  assert status == PASS

  bad_ttFonts = mada_ttFonts
  # introduce mismatching encodings into the first 2 font files:
  for i, encoding in enumerate([WindowsEncodingID.SYMBOL,
                                WindowsEncodingID.UNICODE_BMP]):
    for table in bad_ttFonts[i]['cmap'].tables:
      if table.format == 4:
        table.platEncID = encoding

  print('Test FAIL with fonts that diverge on unicode encoding.')
  status, message = list(check(bad_ttFonts))[-1]
  assert status == FAIL


def NOT_IMPLEMENTED_test_check_076():
  """ Check glyphs have unique unicode codepoints. """
  # from fontbakery.specifications.googlefonts import com_google_fonts_check_076 as check
  # TODO: Implement-me!
  #
  # code-paths:
  # - FAIL, "Some glyphs carry the same unicode value."
  # - PASS


def test_check_077():
  """ Check all glyphs have codepoints assigned. """
  from fontbakery.specifications.cmap import com_google_fonts_check_077 as check

  print('Test PASS with good font.')
  # our reference Mada SemiBold is know to be good here.
  ttFont = TTFont("data/test/mada/Mada-SemiBold.ttf")
  status, message = list(check(ttFont))[-1]
  assert status == PASS

  # TODO: other code-paths:
  # - FAIL, "A glyph lacks a unicode codepoint assignment."
  # Note: I am not aware of any real-case of a font that FAILs this check.
