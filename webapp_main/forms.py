from django import forms

class SearchForm(forms.Form):
    q=forms.CharField(label='Search', max_length=100)

    #update the widget(html code rendered on the page) with specific values. 
    q.widget.attrs.update({'autocomplete':'off'})

class DateForm(forms.Form):
    q=forms.DateField(widget = forms.DateInput(attrs={'type':'date'}))