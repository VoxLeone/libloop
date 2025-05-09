from libloop.flow import Flow

def test_basic_flow():
    flow = Flow(range(10)).shed(2).sift(lambda x: x % 2).morph(lambda x: x * 10).drip(3)
    assert flow.list() == [30, 50, 70]

