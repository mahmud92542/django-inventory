from django import forms

from .models import *

# Input form


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [

            'category',
            'item_name',
            'quantity'

        ]

# form validation & prevent duplicate item
    '''def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        
        for instance in Stock.objects.all():
            if instance.category == category:
                raise forms.ValidationError(str(category) + ' is already created.')
        return category'''

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        for instance in Stock.objects.all():
            if instance.item_name == item_name:
                raise forms.ValidationError(
                    str(item_name) + ' is already exists')
        return item_name


# search form
class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = [

            'category',
            'item_name'

        ]


'''class OrderSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    class Meta:
        model = Stock
        fields = [

            'item_name'

        ]'''


# date search form

class OrderHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    class Meta:
        model = StockHistory
        fields = [

            'item_name',
            'start_date',
            'end_date'

        ]


# product update form
class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [

            'category',
            'item_name',
            'quantity'

        ]


# updating-stock-level-issuing

class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [

            'issue_quantity',
            'issue_to',
            'issue_price'

        ]

# receiving-stock


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [

            'receive_quantity',
            'receive_by'

        ]

# updating the reorder level


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']
