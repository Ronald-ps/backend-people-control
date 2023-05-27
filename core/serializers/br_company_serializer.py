from rest_framework import serializers
from core.models import Company
from core.utils.str_utils import extract_numbers


class CompanySerializer(serializers.ModelSerializer):
    cnpj = serializers.CharField(max_length=14)
    cep = serializers.CharField(max_length=8)
    state_acronym = serializers.CharField(max_length=2)
    name = serializers.CharField(max_length=100)
    employee_count = serializers.SerializerMethodField()

    def get_employee_count(self, obj):
        # len pra não fazer n+1 aqui (prefetch_related salva)
        return len(obj.employees.all())

    def validate_cnpj(self, value):
        cleaned_cnpj = extract_numbers(value)

        if len(cleaned_cnpj) != 14:
            raise serializers.ValidationError("O CNPJ deve ter exatamente 14 dígitos.")

        return cleaned_cnpj

    def validate_cep(self, value):
        cleaned_cep = extract_numbers(value)

        if len(cleaned_cep) != 8:
            raise serializers.ValidationError("O CEP deve ter exatamente 8 dígitos.")

        return cleaned_cep

    def validate_state_acronym(self, value):
        valid_state_acronyms = [
            "AC",
            "AL",
            "AM",
            "AP",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MG",
            "MS",
            "MT",
            "PA",
            "PB",
            "PE",
            "PI",
            "PR",
            "RJ",
            "RN",
            "RO",
            "RR",
            "RS",
            "SC",
            "SE",
            "SP",
            "TO",
        ]

        if value.upper() not in valid_state_acronyms:
            raise serializers.ValidationError("A sigla do estado não é válida.")

        return value.upper()

    def validate_name(self, value):
        return value.lower()

    class Meta:
        model = Company
        fields = "__all__"
