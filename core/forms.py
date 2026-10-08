from django.forms import ModelForm, ValidationError, DateInput, BooleanField

from core.models import Item
from django.utils import timezone


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            "title",
            "description",
            "location",
            "event_date",
            "category",
            "status",
            "image"
        ]
        widgets= {
        "event_date": DateInput(attrs={"type": "date"})
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        description = cleaned_data.get("description", "")

        if not image:
            if not description or len(description.strip()) < 20:
                self.add_error(
                    "description",
                    "به دلیل عدم بارگذاری عکس توضیحات نباید کمتر از 20 کارکتر باشد."
                )
        return cleaned_data

    # def clean_description(self):
    #     description = self.cleaned_data["description"]

    #     if len(description) < 20:
    #         raise ValidationError(
    #             "توضیحات وارد شده نباید کمتر از ۲۰ کارکتر باشد"
    #         )

    #     return description

    def clean_title(self):
        title = self.cleaned_data.get("title" , "")
        crap_words = ["گمشده", "چیز", "وسیله"]

        for word in crap_words:
            if word in title:
                raise ValidationError(
                    f"عنوان <{word}> خیلی عمومی است لطفا عنوان دقیق تری مثل (کلید، ساعت و کوله پشتی) وارد کنید."
                )

        return title

    def clean_event_date(self):
        event_date = self.cleaned_data.get("event_date")
        today = timezone.now().date()

        if event_date and event_date > today:
            raise ValidationError(
                "تاریخ رخداد نمیتواند از آینده باشد. لطفا تاریخی از امروز یا قبل از امروز انتخاب کنید."
            )
        return event_date

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:
            max_mb = 2
            if image.size > max_mb * 1024 * 1024:
                actual_mb = image.size / (1024 * 1024)
                raise ValidationError(
                    f"حجم تصویر {actual_mb:.2f} مگابایت است. حداکثر حجم مجاز 2 مگابایت است."
                )
        return image
