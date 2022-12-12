from django import forms

from pma_apps.auctions.models import Auction, Bid, Comment, Image


class AuctionForm(forms.ModelForm):
    """
    A ModelForm class za kreiranje novog zahteva.
    """

    class Meta:
        model = Auction
        fields = [
            "title",
            "description",
            "category",
        ]
        labels = {
            "title": "Naslov Zahteva",
            "description": "Opis Zahteva",
            "category": "Kategorija Zahteva",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        self.fields["title"].error_messages = {"required": "custom required message"}


class ImageForm(forms.ModelForm):
    """
    A ModelForm class for adding an image to the auction
    """

    class Meta:
        model = Image
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].label = ""
        self.visible_fields()[0].field.widget.attrs["class"] = "form-control"


class CommentForm(forms.ModelForm):
    """
    A ModelForm class for adding a new comment to the auction
    """

    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add a comment",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].label = ""
        self.visible_fields()[0].field.widget.attrs["class"] = "form-control w-75 h-75"


class BidForm(forms.ModelForm):
    """
    A ModelForm class for placing a bid
    """

    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "comment": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            )
        }
