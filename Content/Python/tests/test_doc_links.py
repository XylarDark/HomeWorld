# test_doc_links.py
# Guards the judgement calls in check_doc_links.py.
#
# The failure this suite exists to prevent is a repair that is confidently
# wrong. A checker that guesses at an ambiguous name, or that counts Unreal
# content paths as broken files, either rewrites a pointer to the wrong
# document or floods the report until the real breaks are invisible. Both are
# worse than doing nothing, so both are pinned here.

import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
_content_python = os.path.normpath(os.path.join(_script_dir, ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)

import check_doc_links as cdl


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def _tree(tmp_path, files):
    for rel, text in files.items():
        _write(os.path.join(str(tmp_path), *rel.split("/")), text)
    return str(tmp_path)


def test_unreal_content_paths_are_not_file_links():
    """/Game/... is an engine reference and must never count as broken.

    This is the check that keeps the reported numbers honest. Unreal paths
    appear constantly in these docs and never resolve to a file on disk, so a
    checker that treats them as links would declare most of the corpus broken
    and teach everyone to ignore the output.
    """
    for target in ("/Game/HomeWorld/Maps/MainMenu.MainMenu",
                   "/Engine/EngineResources/KaiFont",
                   "/Script/HomeWorld.HomeWorldCharacter"):
        assert cdl.classify(target) == "unreal", target


def test_external_and_anchor_targets_are_not_file_links():
    assert cdl.classify("https://example.com/a") == "external"
    assert cdl.classify("mailto:a@b.c") == "external"
    assert cdl.classify("C:/dev/HomeWorld/AGENTS.md") == "external", "drive letters are absolute, not relative"
    assert cdl.classify("#section") == "anchor"
    assert cdl.classify("docs/a.md") is None


def test_a_link_that_resolves_is_not_reported(tmp_path):
    root = _tree(tmp_path, {"docs/guide.md": "see [x](REAL.md)\n", "docs/REAL.md": "# hi\n"})
    index = cdl.build_index(root)
    broken = cdl.check_file(os.path.join(root, "docs", "guide.md"), root, index)
    assert broken == [], "a link pointing at a file that exists must not be reported"


def test_unique_basename_is_rewritten(tmp_path):
    """A directory move is exactly what a unique basename can repair."""
    root = _tree(tmp_path, {
        "docs/guide.md": "see [x](old/DEEP_DIVE.md)\n",
        "docs/Editor/DEEP_DIVE.md": "# hi\n",
    })
    index = cdl.build_index(root)
    changed = cdl.fix_file(os.path.join(root, "docs", "guide.md"), root, index)
    assert changed == 1
    with open(os.path.join(root, "docs", "guide.md"), encoding="utf-8") as handle:
        assert "[x](Editor/DEEP_DIVE.md)" in handle.read()


def test_ambiguous_name_is_reported_and_left_alone(tmp_path):
    """SKILL.md exists in many places; picking one would be fiction."""
    root = _tree(tmp_path, {
        "docs/a.md": "see [s](missing/SKILL.md)\n",
        "skills/one/SKILL.md": "# one\n",
        "skills/two/SKILL.md": "# two\n",
    })
    index = cdl.build_index(root)
    path = os.path.join(root, "docs", "a.md")

    broken = cdl.check_file(path, root, index)
    assert len(broken) == 1 and broken[0].status == "ambiguous"
    assert len(broken[0].candidates) == 2

    assert cdl.fix_file(path, root, index) == 0, "must not repair what it cannot be sure of"
    with open(path, encoding="utf-8") as handle:
        assert "missing/SKILL.md" in handle.read()


def test_gone_name_is_reported_and_left_alone(tmp_path):
    root = _tree(tmp_path, {"docs/a.md": "see [d](DELETED_FOREVER.md)\n"})
    index = cdl.build_index(root)
    path = os.path.join(root, "docs", "a.md")

    broken = cdl.check_file(path, root, index)
    assert len(broken) == 1 and broken[0].status == "gone"
    assert broken[0].candidates == ()
    assert cdl.fix_file(path, root, index) == 0


def test_anchor_survives_the_rewrite(tmp_path):
    root = _tree(tmp_path, {
        "docs/a.md": "[s](old/REF.md#the-part)",
        "docs/REF.md": "# hi\n",
    })
    index = cdl.build_index(root)
    cdl.fix_file(os.path.join(root, "docs", "a.md"), root, index)
    with open(os.path.join(root, "docs", "a.md"), encoding="utf-8") as handle:
        assert "(REF.md#the-part)" in handle.read(), "the anchor is part of the reference, not debris"


def test_sibling_file_is_never_mangled(tmp_path):
    """A link that already works must come through a fix byte-identical."""
    root = _tree(tmp_path, {"docs/a.md": "[ok](B.md)\n", "docs/B.md": "# b\n"})
    index = cdl.build_index(root)
    path = os.path.join(root, "docs", "a.md")
    with open(path, encoding="utf-8") as handle:
        before = handle.read()
    assert cdl.fix_file(path, root, index) == 0
    with open(path, encoding="utf-8") as handle:
        assert handle.read() == before


def test_case_only_difference_is_not_a_break(tmp_path):
    """Docs/ and docs/ are one directory (DEC-0029), so Docs/A.md must not
    report as broken on a case-insensitive filesystem."""
    root = _tree(tmp_path, {"docs/a.md": "[x](Docs/A.md)\n", "docs/A.md": "# a\n"})
    index = cdl.build_index(root)
    broken = cdl.check_file(os.path.join(root, "docs", "a.md"), root, index)
    if os.path.exists(os.path.join(root, "docs", "A.md")) and os.path.exists(os.path.join(root, "docs", "a.md")):
        assert broken == [], "case-insensitive filesystems must not report a false break"
