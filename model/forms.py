from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()



class CancerRiskForm(forms.Form):
    age = forms.IntegerField(label="Age", min_value=0)
    family_history = forms.ChoiceField(
        label="Family History", choices=[(1, "Yes"), (0, "No")], widget=forms.RadioSelect
    )
    genetic_mutation = forms.ChoiceField(
        label="Genetic Mutation", choices=[(1, "Yes"), (0, "No")], widget=forms.RadioSelect
    )
    uv_exposure = forms.ChoiceField(
        label="UV Exposure", choices=[(0, "Low"), (1, "Moderate"), (2, "High")], widget=forms.RadioSelect
    )

