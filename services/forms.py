from django import forms

from users.models import Company


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    price_hour = forms.DecimalField(decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices="", **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # adding choices to fields
        if choices:
            self.fields["field"].choices = choices
        # adding placeholders to form fields
        self.fields["name"].widget.attrs["placeholder"] = "Enter Service Name"
        self.fields["description"].widget.attrs["placeholder"] = "Enter Description"
        self.fields["price_hour"].widget.attrs["placeholder"] = "Enter Price per Hour"

        self.fields["name"].widget.attrs["autocomplete"] = "off"


class RequestServiceForm(forms.Form):
    request_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Request Date",
        required=True
    )
    address = forms.CharField(
        max_length=255,
        label="Service Address",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 123 Main St, Nairobi'})
    )
    duration_hours = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Duration (hours)",
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Duration in hours'})
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Additional notes (optional)'}),
        required=False,
        label="Notes"
    )
