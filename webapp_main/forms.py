from django import forms

class SearchForm(forms.Form):
    q=forms.CharField(max_length=100, label='')

    #update the widget(html code rendered on the page) with specific values. 
    q.widget.attrs.update(
        {
            'autocomplete':'off',
            'placeholder':'Search Articles',
            'class': 'form-control'
        }
    )

class DateForm(forms.Form):
    q=forms.DateField(
        widget = forms.DateInput(
            attrs = {
                'type':'date'
            }
        ),
        label=''
    )

    q.widget.attrs.update(
        {
            'class': 'form-control'
        }
    )
