from django import forms
from authuser.models import Profile


# Update Profile Form
class UpdateProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder':'Full Name'}), required=False)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder':'Bio'}), required=False)
    # address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder':'Address'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder':'Phone Number'}), required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control rounded', 'placeholder':'image'}), required=False)

    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'phone', 'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control" # and the is the border around the input
        
