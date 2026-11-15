from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(5, "★★★★★ (5 - Excellent)"), (4, "★★★★☆ (4 - Good)"), (3, "★★★☆☆ (3 - Average)"), (2, "★★☆☆☆ (2 - Poor)"), (1, "★☆☆☆☆ (1 - Terrible)")],
        widget=forms.Select(attrs={"class": "form-control"}),
        initial=5
    )
    title = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "What's most important to know?"})
    )
    comment = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "What did you like or dislike? How was the performance?"})
    )

    class Meta:
        model = Review
        fields = ["rating", "title", "comment"]
