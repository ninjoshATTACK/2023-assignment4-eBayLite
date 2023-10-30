from django import forms
from .models import Listing, Comment, Bid

# Create your forms here.
class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title', 'description', 'startbid', 'photo_url', 'category')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ('price',)