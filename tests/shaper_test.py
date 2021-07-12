from east_asian_spacing.shaper import InkPartMargin
import pytest

from east_asian_spacing import Font
from east_asian_spacing import InkPart
from east_asian_spacing import GlyphData
from east_asian_spacing import Shaper
from east_asian_spacing import ShapeResult


def test_glyph_data_eq():
    glyph1 = GlyphData(1, 0, 1000, 0)
    glyph2 = GlyphData(1, 0, 1000, 0)
    assert glyph1 == glyph2

    glyph3 = GlyphData(2, 1, 1000, 0)
    glyph4 = GlyphData(2, 1, 1000, 0)
    result1 = ShapeResult((glyph1, glyph3))
    result2 = ShapeResult((glyph2, glyph4))
    assert result1 == result2

    glyph3.advance = 500
    assert glyph1 != glyph3
    assert result1 != result2


def test_compute_ink_part():
    from east_asian_spacing.shaper import _compute_ink_part
    assert _compute_ink_part(0, 499, 0, 1000) == InkPart.LEFT
    assert _compute_ink_part(501, 1000, 0, 1000) == InkPart.RIGHT
    assert _compute_ink_part(251, 749, 0, 1000) == InkPart.MIDDLE


def test_compute_ink_part_margin():
    from east_asian_spacing.shaper import _compute_ink_part
    # Meiryo vertical U+FF5D
    assert _compute_ink_part(-1613, -772, -1798, 250) == InkPart.OTHER
    with InkPartMargin(2):
        assert _compute_ink_part(-1613, -772, -1798, 250) == InkPart.LEFT


@pytest.mark.asyncio
async def test_ink_part(test_font_path):
    font = Font.load(test_font_path)
    shaper = Shaper(font)
    await shaper.compute_fullwidth_advance()
    result = await shaper.shape('\uFF08\uFF09\u30FB\u56DB')
    result.compute_ink_parts(font)
    assert result[0].ink_part == InkPart.RIGHT
    assert result[1].ink_part == InkPart.LEFT
    assert result[2].ink_part == InkPart.MIDDLE
    assert result[3].ink_part == InkPart.OTHER

    font = font.vertical_font
    shaper = Shaper(font, features=['vert'])
    await shaper.compute_fullwidth_advance()
    result = await shaper.shape('\uFF08\uFF09\u30FB\u56DB')
    result.compute_ink_parts(font)
    assert result[0].ink_part == InkPart.RIGHT
    assert result[1].ink_part == InkPart.LEFT
    assert result[2].ink_part == InkPart.MIDDLE
    assert result[3].ink_part == InkPart.OTHER
