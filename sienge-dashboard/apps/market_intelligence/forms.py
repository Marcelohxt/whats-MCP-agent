from django import forms

class MaterialQuoteForm(forms.Form):
    name = forms.CharField(
        label='Nome do Material',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Bloco cerâmico 14x19x39'
        })
    )
    report_format = forms.ChoiceField(
        label='Formato do Relatório',
        choices=[
            ('excel', 'Excel'),
            ('pdf', 'PDF')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    generate_report = forms.BooleanField(
        label='Gerar Relatório',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class BulkQuoteForm(forms.Form):
    file = forms.FileField(
        label='Arquivo de Materiais',
        help_text='Aceita arquivos Excel (.xlsx, .xls) ou CSV',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls,.csv'
        })
    )
    report_format = forms.ChoiceField(
        label='Formato do Relatório',
        choices=[
            ('excel', 'Excel'),
            ('pdf', 'PDF')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    ) 