from libloop import Loop

def test_map_and_print(capsys):
    Loop(1, 3).map(lambda x: x * 2).print()
    captured = capsys.readouterr()
    assert captured.out == "2\n4\n"
