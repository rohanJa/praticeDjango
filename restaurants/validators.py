from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )

def validate_email(self):
    email = self.cleaned_data.get('email')
    if 'edu' in email:
        raise forms.ValidationError('edu mail are not allowed')

CATEGORIES = ['Indian','Chinese','Snacks']

def validate_category(value):
    cat = value.capitalize()
    if not value in CATEGORIES and not cat in CATEGORIES  :
        raise ValidationError(f"{value} is not a valid category")