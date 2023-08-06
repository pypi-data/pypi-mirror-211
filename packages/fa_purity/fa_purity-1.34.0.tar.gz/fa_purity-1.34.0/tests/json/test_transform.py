from fa_purity.json_2.value import (
    JsonValueFactory,
    Unfolder,
)

test_data = (
    JsonValueFactory.from_any({"foo": {"nested": ["hi", 99]}})
    .bind(Unfolder.to_json)
    .unwrap()
)


def test_dumps() -> None:
    assert Unfolder.dumps(test_data).replace(
        " ", ""
    ) == '{"foo": {"nested": ["hi", 99]} }'.replace(" ", "")
