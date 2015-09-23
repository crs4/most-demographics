
class DAO(object):
    def __init__(self):
        self._patients = [{
            "DATETIME_OF_BIRTH": "19650322",
            "SURNAME": "BIANCHI",
            "NAME": "PAOLO",
            "IDENTIFIER": "100001",
            "BIRTH_PLACE": "CAGLIARI",
            "ACCOUNT_NUMBER": "BNCPLA65C22L781B",
            "ADMINISTRATIVE_SEX": "M"
        }, {
            "DATETIME_OF_BIRTH": "19221212",
            "SURNAME": "BERRY",
            "NAME": "BLUE",
            "IDENTIFIER": "100002",
            "BIRTH_PLACE": "SASSARI",
            "ACCOUNT_NUMBER": "BLUBRY25T12D585X",
            "ADMINISTRATIVE_SEX": "M"
        }, {
            "DATETIME_OF_BIRTH": "19721213",
            "SURNAME": "MIMI'",
            "NAME": "HAIUARA",
            "IDENTIFIER": "100003",
            "BIRTH_PLACE": "GENOVA",
            "ACCOUNT_NUMBER": "HRAMMI72T53B354K",
            "ADMINISTRATIVE_SEX": "F"
        }, {
            "DATETIME_OF_BIRTH": "19571217",
            "SURNAME": "JONATHAN",
            "NAME": "STEELE",
            "IDENTIFIER": "100004",
            "BIRTH_PLACE": "ROMA",
            "ACCOUNT_NUMBER": "JNTSTL57T17F979P",
            "ADMINISTRATIVE_SEX": "M"
        }]

    def get_data(self, params):
        return [p for p in self._patients if
                params.get("IDENTIFIER").lower() == p.get("IDENTIFIER").lower() and
                params.get("IDENTIFIER") is not None]
