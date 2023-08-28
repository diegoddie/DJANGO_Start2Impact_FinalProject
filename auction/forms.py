from django import forms

class BidForm(forms.Form):
    amount = forms.IntegerField(label='ENTER YOUR BID', min_value=0, widget=forms.TextInput(attrs={'class': 'submit-btn'}))

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        if amount is None:
            raise forms.ValidationError('Please enter a valid bid amount.')

        return amount