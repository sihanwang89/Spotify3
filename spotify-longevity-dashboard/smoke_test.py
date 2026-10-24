from streamlit.testing.v1 import AppTest


def run_and_check(at: AppTest) -> None:
    at.run(timeout=30)
    assert not at.exception, [item.value for item in at.exception]
    assert len(at.metric) == 3
    assert len(at.dataframe) == 1


at = AppTest.from_file("app.py")
run_and_check(at)
assert at.metric[0].value == "1,200"
assert at.metric[1].value == "18"
assert at.metric[2].value == "28.7%"

at.sidebar.slider[0].set_value((2020, 2022))
at.sidebar.multiselect[0].set_value(["Rock"])
run_and_check(at)
assert at.metric[0].value != "1,200"

at.sidebar.multiselect[0].set_value([])
at.run(timeout=30)
assert not at.exception, [item.value for item in at.exception]
assert len(at.warning) == 1

print("Dashboard smoke tests passed: default view, filters, and empty selection.")
