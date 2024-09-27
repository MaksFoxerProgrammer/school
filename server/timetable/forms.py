from django import forms
from timetable.models import Subjects, Organization, Specialization


class FormCreateSubject(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = "__all__"


class FormCreateOrganization(forms.ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"


class FormCreateSpecialization(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = "__all__"


# class FormCreateStudent(forms.Form):
#     name = forms.CharField("User name", initial="UserName",
#                            error_messages={"required": "Please enter your"
#                                            " avialable email"})
#     email = forms.EmailField(initial="admin@admin.com", error_messages={
#         'required': 'Please enter your available email'})
#     password = forms.CharField(max_length=20, min_length=10,
#                                required=False,
#                                widget=forms.PasswordInput())
#     age = forms.IntegerField(required=False, initial="45",
#                              help_text="Enter your current age")