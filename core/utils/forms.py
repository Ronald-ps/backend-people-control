import json
from django import forms


class SimpleRequestPostForm(forms.Form):
    """
    Class para lidar com requisições da web.
    Sobrescreve forms.Form para lidarcom requests do tipo post feita por ajax, donde
    os dados são passados no body. Não usar para renderizar formulários.

    Lida bem com dados json. Validação automática do formulário.
    """

    def _parse_b_string_data(self, b_string):
        decoded_string = b_string.decode("utf-8")
        data_dict = json.loads(decoded_string)
        return data_dict

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        data = data or args[0]
        if data and isinstance(data, bytes):
            parsed_data = self._parse_b_string_data(data)
            if kwargs.get("data"):
                kwargs["data"] = parsed_data
            else:
                new_args = (parsed_data,) + args[1:]

            super().__init__(*new_args, **kwargs)
        else:
            super().__init__(*args, **kwargs)
