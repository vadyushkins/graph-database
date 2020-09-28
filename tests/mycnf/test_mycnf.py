from pyformlang.cfg import CFG

from src.MyCNF import MyCNF


def test_from_text(automatic_suite):
    gr = automatic_suite

    cfg = CFG.from_text(gr)

    mycnf = MyCNF.from_text(gr)

    def check():
        for word in cfg.get_words(13):
            if (len(word) == 0) and (mycnf.generate_epsilon() is not True):
                return False
            elif mycnf.contains(word) is not True:
                return False
        return True

    assert check()


def test_from_txt(automatic_suite, tmp_path):
    gr = automatic_suite

    gr_file = tmp_path / 'grammar.txt'
    gr_file.write_text(gr.replace(' ->', ''))

    cfg = CFG.from_text(gr)

    mycnf = MyCNF.from_txt(gr_file)

    def check():
        for word in cfg.get_words(13):
            if (len(word) == 0) and (mycnf.generate_epsilon() is not True):
                return False
            elif mycnf.contains(word) is not True:
                return False
        return True

    assert check()